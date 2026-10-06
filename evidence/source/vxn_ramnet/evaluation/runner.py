from __future__ import annotations

import csv
import io
import time
from datetime import datetime, timezone
from pathlib import Path

from vxn_ramnet.algorithms.decision import AggregatedScores, decide
from vxn_ramnet.config.models import DecisionSettings
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.io.atomic import atomic_write_json, atomic_write_text
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.io.npz import save_npz
from vxn_ramnet.io.schema import validate_schema
from vxn_ramnet.memory.store import RouteMemoryStore
from vxn_ramnet.observability.manifest import build_run_manifest
from vxn_ramnet.recognition import RouteRecognizer, learn_route_memory
from vxn_ramnet.reporting.sanitize import csv_cell

from .baselines import classify_baseline
from .manifest import load_dataset
from .metrics import summarize_decisions, timing_summary

METHODS = (
    "vxn_default",
    "vxn_reference_windows",
    "vxn_disjoint_best",
    "vxn_legacy",
    "vxn_original_only",
    "vxn_no_temporal_prior",
    "fixed_branch_a",
    "global_centroid",
    "last_frame_nn",
    "mean_frame_nn",
    "dtw_suffix",
)


def _write_csv(path: Path, rows: list[dict]) -> None:
    stream = io.StringIO(newline="")
    fields = sorted({key for row in rows for key in row})
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: csv_cell(value) for key, value in row.items()})
    atomic_write_text(path, stream.getvalue())


def _original_only(sequence: EncodedSequence) -> EncodedSequence:
    return EncodedSequence(sequence.sequence_id, sequence.embeddings, sequence.embeddings, (), sequence.metadata)


def threshold_sweep(rows: list[dict]) -> list[dict]:
    output = []
    for score_threshold in (0.54, 0.58, 0.62, 0.66, 0.70, 0.74, 0.78):
        for gap_threshold in (0.02, 0.04, 0.08, 0.12):
            settings = DecisionSettings(
                minimum_branch_score=score_threshold,
                strong_branch_score=max(0.72, score_threshold),
                minimum_branch_gap=gap_threshold,
                strong_branch_gap=max(0.07, gap_threshold),
            )
            decisions = []
            for row in rows:
                a, b = row["branch_a_score"], row["branch_b_score"]
                scores = AggregatedScores(
                    a, b, abs(a - b), max(a, b), row.get("common_score", 0), row.get("junction_score", 0)
                )
                decision = decide(scores, settings, "BRANCH_A", "BRANCH_B", {})
                updated = {**row, "decision_kind": decision.kind.value, "branch_id": decision.branch_id}
                if row.get("graph_degraded"):
                    updated.update(decision_kind="uncertain", branch_id=None)
                decisions.append(updated)
            metrics = summarize_decisions(decisions)
            output.append(
                {
                    "minimum_branch_score": score_threshold,
                    "minimum_branch_gap": gap_threshold,
                    **{
                        k: metrics[k]
                        for k in (
                            "accepted",
                            "accepted_errors",
                            "coverage",
                            "selective_risk",
                            "unknown_false_acceptance_rate",
                        )
                    },
                }
            )
    return output


def report_markdown(report: dict) -> str:
    lines = [
        "# Executed VXN-RAMNet evaluation",
        "",
        f"Dataset: **{report['dataset_id']}**. Purpose: **{report['purpose']}**.",
        "",
        report["evidence_boundary"],
        "",
        f"Generated at: {report['generated_at']}. Source SHA-256: `{report['environment']['source']['sha256']}`.",
        "",
        "All numbers below come from this run. Null means an undefined denominator or an unsupported measurement.",
        "",
        "| Method | Accepted / journeys | Accepted errors | Correct known / known | Known macro F1 | Unknown false accepts / unknown | Query median ms | Query p95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method, entry in report["methods"].items():
        m, t = entry["metrics"], entry["classification_timing"]
        f1 = "undefined" if m["known_macro_f1"] is None else f"{m['known_macro_f1']:.4f}"
        lines.append(
            f"| {method} | {m['accepted']} / {m['journeys']} | {m['accepted_errors']} | {m['correct_known']} / {m['known_journeys']} | {f1} | {m['unknown_false_accepts']} / {m['unknown_journeys']} | {t['median_ms']:.3f} | {t['p95_ms']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            *[f"- {note}" for note in report["limitations"]],
            "",
            "## Enrollment events",
            "",
            "Indices refer to sampled embeddings, not source-video frames or seconds.",
            "",
            "| Variant | First junction | Turnaround | Revisit | Anchor mean absolute error (frames) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for variant, entry in report["enrollment"].items():
        e = entry["events"]
        lines.append(
            f"| {variant} | {e['first_junction_index']} | {e['turnaround_index']} | {e['return_junction_index']} | {entry['event_mean_absolute_error_frames']} |"
        )
    lines += [
        "",
        "## Reproduce",
        "",
        f"`vxn-ramnet evaluate --manifest {report['reproduction_manifest']} --output evidence/reproduced-{report['dataset_id']} --repeats {report['repeats']} --warmups {report['warmups']}`",
        "",
        "Inspect `report.json`, `decisions.csv`, `timings.csv`, `threshold-sweep.csv`, `manifest.snapshot.json` and `checksums.json` together.",
        "",
    ]
    return "\n".join(lines)


def run_evaluation(manifest_path: Path, output: Path, *, repeats: int = 5, warmups: int = 1) -> dict:
    if not 1 <= repeats <= 100 or not 0 <= warmups <= 20:
        raise ValueError("repeats must be 1..100 and warmups 0..20")
    started = time.perf_counter()
    manifest, learning, queries = load_dataset(manifest_path)
    if output.exists():
        raise FileExistsError("Evaluation output already exists; select a fresh directory")
    environment = build_run_manifest(
        "evaluation-" + manifest.dataset_id, {}, {"provenance": manifest.encoder_provenance}
    )
    output.mkdir(parents=True)
    atomic_write_text(output / ".vxn-evaluation", "Managed evaluation evidence\n")
    settings = DecisionSettings()
    detection = manifest.detection
    memories, enrollment, timing_rows = {}, {}, []
    variants = {
        "default": (learning, detection),
        "legacy": (learning, detection.model_copy(update={"segment_policy": "legacy_overlap"})),
        "original_only": (_original_only(learning), detection),
        "no_temporal_prior": (learning, detection.model_copy(update={"plausibility_weight": 0.0})),
    }
    for variant, (sequence, detector_settings) in variants.items():
        learning_times = []
        for repetition in range(warmups + repeats):
            tick = time.perf_counter_ns()
            memory, similarity = learn_route_memory(sequence, detector_settings)
            elapsed = (time.perf_counter_ns() - tick) / 1e6
            if repetition >= warmups:
                learning_times.append(elapsed)
                timing_rows.append(
                    {
                        "method": variant,
                        "stage": "enrollment",
                        "query_id": "",
                        "repetition": repetition - warmups,
                        "elapsed_ms": elapsed,
                    }
                )
        memories[variant] = memory
        RouteMemoryStore.save(
            memory, output / "memory" / variant / "route-memory.npz", output / "memory" / variant / "route-memory.json"
        )
        save_npz(output / "memory" / variant / "self-similarity.npz", {"self_similarity": similarity})
        events = memory.metadata["events"]
        error = None
        if manifest.expected_events:
            anchors = manifest.expected_events.model_dump(exclude={"provenance"})
            error = sum(abs(events[k] - anchors[k]) for k in anchors) / len(anchors)
        enrollment[variant] = {
            "events": events,
            "quality": memory.metadata["quality"],
            "segment_policy": detector_settings.segment_policy,
            "event_mean_absolute_error_frames": error,
            "timing": timing_summary(learning_times),
            "memory_numeric_array_bytes": sum(
                c.embeddings.nbytes + c.flipped_embeddings.nbytes + c.centroid.nbytes + c.source_indices.nbytes
                for c in memory.components.values()
            ),
            "self_similarity_array_bytes": similarity.nbytes,
        }
    all_decisions: list[dict] = []
    methods: dict = {}
    sweeps: list[dict] = []
    for method in METHODS:
        variant = {
            "vxn_legacy": "legacy",
            "vxn_original_only": "original_only",
            "vxn_no_temporal_prior": "no_temporal_prior",
        }.get(method, "default")
        memory = memories[variant]
        decision_settings = (
            settings.model_copy(update={"window_selection": "legacy_best"})
            if method in {"vxn_legacy", "vxn_disjoint_best"}
            else settings
        )
        recognizer = RouteRecognizer(decision_settings, detection)
        rows, timings = [], []
        for record in manifest.queries:
            query = _original_only(queries[record.id]) if method == "vxn_original_only" else queries[record.id]
            previous_identity = None
            for repetition in range(warmups + repeats):
                tick = time.perf_counter_ns()
                try:
                    decision = (
                        recognizer.classify(query, memory, cache_frame_scores=method != "vxn_reference_windows")
                        if method.startswith("vxn_")
                        else classify_baseline(method, query, memory, settings)
                    )
                except Exception as exc:
                    decision = {
                        "query_id": record.id,
                        "decision_kind": "error",
                        "branch_id": None,
                        "confidence": None,
                        "reason": f"Classifier failed: {type(exc).__name__}",
                        "best_branch_score": None,
                    }
                elapsed = (time.perf_counter_ns() - tick) / 1e6
                identity = (decision["decision_kind"], decision["branch_id"])
                if previous_identity is not None and identity != previous_identity:
                    raise RuntimeError("Repeated classification changed outcome; evaluation is not deterministic")
                previous_identity = identity
                if repetition >= warmups:
                    timings.append(elapsed)
                    timing_rows.append(
                        {
                            "method": method,
                            "stage": "classification",
                            "query_id": record.id,
                            "repetition": repetition - warmups,
                            "elapsed_ms": elapsed,
                        }
                    )
            if "best_branch_score" not in decision:
                decision["best_branch_score"] = max(decision["branch_a_score"], decision["branch_b_score"])
            evidence = decision.pop("evidence", {})
            # Preserve the complete window evidence separately; CSV stays scalar.
            if evidence:
                atomic_write_json(output / "window-evidence" / method / f"{record.id}.json", evidence)
            row = {
                **decision,
                "method": method,
                "expected_label": record.expected_label,
                "session_id": record.session_id,
                "graph_degraded": evidence.get("graph_degraded", False),
            }
            rows.append(row)
        methods[method] = {"metrics": summarize_decisions(rows), "classification_timing": timing_summary(timings)}
        all_decisions.extend(rows)
        if all(r.get("branch_a_score") is not None for r in rows):
            sweeps.extend({"method": method, **r} for r in threshold_sweep(rows))
    report = {
        "schema_version": "1.0.0",
        "dataset_id": manifest.dataset_id,
        "purpose": manifest.purpose,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repeats": repeats,
        "warmups": warmups,
        "evidence_boundary": "Regression and synthetic diagnostics establish reproducible software behavior. They do not establish held-out route accuracy, mobile speed, safe navigation or user benefit."
        if manifest.purpose != "held_out"
        else "Independent-session cached-embedding evaluation for the declared route set. Scope and provenance are limited to the supplied manifest; no mobile or user-benefit claim follows.",
        "environment": environment,
        "dataset_manifest_sha256": sha256_file(manifest_path),
        "dataset": manifest.model_dump(mode="json"),
        "decision_settings": settings.model_dump(mode="json"),
        "enrollment": enrollment,
        "methods": methods,
        "evaluation_elapsed_seconds_before_report_writes": time.perf_counter() - started,
        "reproduction_manifest": manifest_path.as_posix(),
        "limitations": [
            "Cached descriptors only: capture, video decoding, EfficientNet inference, Android, Wi-Fi and audible output are excluded from classifier timing.",
            "Timing samples repeat the same journeys; repetitions do not increase dataset size. p95 uses NumPy linear interpolation.",
            "Regression labels/event anchors come from the supplied expectations, not independently annotated ground truth. Original source-video/session/model-weight provenance was not supplied.",
            "Synthetic vectors exercise decision mechanisms; they do not model real camera, corridor, participant or mobile distributions.",
            "Fixed-A is a predeclared forced-choice baseline. Other baselines share default heuristic thresholds with differing score distributions; comparison is diagnostic, not calibrated superiority evidence.",
            "Threshold sweeps describe these cases only. No threshold selection or probability calibration is performed. Unknown AUROC/AP is undefined without known and unknown journeys.",
            "Memory bytes cover named NumPy arrays, not process peak RSS or complete deployment memory. One-junction/two-branch scope remains.",
            "Known accuracy and macro F1 include abstentions as missed known labels. Ambiguous cases are excluded from unknown ranking metrics.",
        ],
    }
    validate_schema("benchmark-report.schema.json", report)
    atomic_write_json(output / "manifest.snapshot.json", manifest.model_dump(mode="json"))
    atomic_write_json(output / "report.json", report)
    atomic_write_text(output / "report.md", report_markdown(report))
    _write_csv(output / "decisions.csv", all_decisions)
    _write_csv(output / "timings.csv", timing_rows)
    _write_csv(output / "threshold-sweep.csv", sweeps)
    atomic_write_json(
        output / "checksums.json",
        {p.relative_to(output).as_posix(): sha256_file(p) for p in sorted(output.rglob("*")) if p.is_file()},
    )
    if any(entry["metrics"]["error_count"] for entry in methods.values()):
        raise RuntimeError("Evaluation recorded classifier failures; inspect retained report and fix before publishing")
    return report
