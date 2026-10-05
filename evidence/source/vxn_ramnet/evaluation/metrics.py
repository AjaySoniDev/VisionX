"""Journey-level metrics with explicit abstention and undefined denominators."""

from __future__ import annotations

import numpy as np

BRANCHES = ("BRANCH_A", "BRANCH_B")


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def ranking_metrics(truth_unknown: list[bool], unknown_scores: list[float]) -> dict:
    y = np.asarray(truth_unknown, dtype=bool)
    scores = np.asarray(unknown_scores, dtype=float)
    if y.shape != scores.shape or not np.isfinite(scores).all():
        raise ValueError("Invalid ranking inputs")
    positives, negatives = int(y.sum()), int((~y).sum())
    if not positives or not negatives:
        return {"unknown_auroc": None, "unknown_average_precision": None}
    # Pairwise AUC gives half credit to ties. AP groups equal-score thresholds.
    comparisons = scores[y, None] - scores[~y][None, :]
    auc = float(np.mean((comparisons > 0) + 0.5 * (comparisons == 0)))
    ap, previous_recall = 0.0, 0.0
    for threshold in sorted(set(scores.tolist()), reverse=True):
        selected = scores >= threshold
        tp = int((selected & y).sum())
        recall = tp / positives
        precision = tp / int(selected.sum())
        ap += (recall - previous_recall) * precision
        previous_recall = recall
    return {"unknown_auroc": auc, "unknown_average_precision": float(ap)}


def summarize_decisions(rows: list[dict]) -> dict:
    if not rows or len({r["query_id"] for r in rows}) != len(rows):
        raise ValueError("Metrics require nonempty unique journey records")
    n = len(rows)
    accepted = [r for r in rows if r["decision_kind"] == "known_branch"]
    known = [r for r in rows if r["expected_label"] in BRANCHES]
    unknown = [r for r in rows if r["expected_label"] == "UNKNOWN"]
    ambiguous = [r for r in rows if r["expected_label"] == "AMBIGUOUS"]
    for r in accepted:
        if r["branch_id"] not in BRANCHES:
            raise ValueError("Accepted branch must have a valid branch label")
    errors = sum(r["branch_id"] != r["expected_label"] for r in accepted)
    correct_known = sum(r["branch_id"] == r["expected_label"] and r["decision_kind"] == "known_branch" for r in known)
    confusion = {
        truth: {prediction: 0 for prediction in (*BRANCHES, "ABSTAIN", "ERROR")}
        for truth in (*BRANCHES, "UNKNOWN", "AMBIGUOUS")
    }
    for r in rows:
        prediction = (
            r["branch_id"]
            if r["decision_kind"] == "known_branch"
            else "ERROR"
            if r["decision_kind"] == "error"
            else "ABSTAIN"
        )
        confusion[r["expected_label"]][prediction] += 1
    f1 = []
    for branch in BRANCHES:
        tp = sum(
            r["expected_label"] == branch and r["branch_id"] == branch and r["decision_kind"] == "known_branch"
            for r in known
        )
        fp = sum(
            r["expected_label"] != branch and r["branch_id"] == branch and r["decision_kind"] == "known_branch"
            for r in known
        )
        fn = sum(
            r["expected_label"] == branch and not (r["branch_id"] == branch and r["decision_kind"] == "known_branch")
            for r in known
        )
        f1.append(2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0)
    rank_rows = [r for r in rows if r["expected_label"] != "AMBIGUOUS"]
    rank = (
        ranking_metrics(
            [r["expected_label"] == "UNKNOWN" for r in rank_rows],
            [-r["best_branch_score"] for r in rank_rows],
        )
        if rank_rows and all(r.get("best_branch_score") is not None for r in rank_rows)
        else {"unknown_auroc": None, "unknown_average_precision": None}
    )
    return {
        "journeys": n,
        "known_journeys": len(known),
        "unknown_journeys": len(unknown),
        "ambiguous_journeys": len(ambiguous),
        "accepted": len(accepted),
        "accepted_errors": errors,
        "correct_known": correct_known,
        "coverage": len(accepted) / n,
        "selective_risk": _ratio(errors, len(accepted)),
        "known_decision_accuracy": _ratio(correct_known, len(known)),
        "known_macro_f1": float(np.mean(f1)) if known else None,
        "known_coverage": _ratio(sum(r["decision_kind"] == "known_branch" for r in known), len(known)),
        "unknown_false_accepts": sum(r["decision_kind"] == "known_branch" for r in unknown),
        "unknown_false_acceptance_rate": _ratio(
            sum(r["decision_kind"] == "known_branch" for r in unknown), len(unknown)
        ),
        "unknown_rejection_rate": _ratio(sum(r["decision_kind"] == "unknown_route" for r in unknown), len(unknown)),
        "ambiguous_abstention_rate": _ratio(
            sum(r["decision_kind"] in {"uncertain", "unknown_route"} for r in ambiguous), len(ambiguous)
        ),
        "error_count": sum(r["decision_kind"] == "error" for r in rows),
        "confusion_matrix": confusion,
        **rank,
    }


def timing_summary(values_ms: list[float]) -> dict:
    if not values_ms or any(not np.isfinite(v) or v < 0 for v in values_ms):
        raise ValueError("Timings must be nonempty, finite and nonnegative")
    return {
        "samples": len(values_ms),
        "median_ms": float(np.median(values_ms)),
        "p95_ms": float(np.percentile(values_ms, 95)),
        "min_ms": min(values_ms),
        "max_ms": max(values_ms),
    }
