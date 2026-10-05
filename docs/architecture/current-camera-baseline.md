# Implemented offline core architecture

The executable flow is completed learning video → deterministic sampling → frozen EfficientNetB0 descriptors → constrained revisit/turnaround inference → five-component memory; completed query video → descriptors → multi-window evidence → known / uncertain / unknown.

## Modules

| Responsibility | Code |
|---|---|
| Configurations and relative path resolution | `config/models.py`, `config/loader.py` |
| Video validation / deterministic unique sampling | `io/video.py` |
| Frozen encoder / RGB preparation / descriptor validation | `vision/`, `algorithms/similarity.py` |
| Shared learning and recognition API | `recognition.py` |
| Revisit, turnaround and segmentation | `algorithms/junction.py`, `turnaround.py`, `segmentation.py` |
| Component evidence / window selection / decisions | `algorithms/scoring.py`, `decision.py` |
| Versioned paired memory and artifact validation | `memory/`, `io/npz.py`, `io/json.py`, `io/schema.py` |
| Stage orchestration, signatures and invalidation | `pipeline/` |
| Source/model/environment provenance and local logs | `observability/` |
| Scalar reports and sanitized text/CSV | `reporting/` |
| Declared dataset, baselines, metrics, timing, evidence | `evaluation/` |

## Numerical definition

Embeddings have unit L2 norm. Flip-aware similarity is the maximum dot product across original/original, flip/original, original/flip and flip/flip pairs. Invalid, nonfinite, empty or nonunit descriptors are rejected. Chunking bounds temporary blocks, while the output enrollment matrix still occupies O(N²) memory.

Near-diagonal similarity is suppressed. Junction search compares same/reverse-order windows in configured early/later ranges and applies the documented temporal plausibility prior. Turnaround search compares sampled outward evidence with reversed backtrack evidence between the inferred junction visits. These are appearance heuristics, not physical turn sensors.

Disjoint segmentation is the default; legacy overlap is retained for historical regression. Components are common_path, junction, branch_a, backtrack and branch_b. Branch labels reflect exploration order. BACKTRACK is not directly scored in final query classification.

Per-frame component evidence = 0.50 × best memory similarity + 0.30 × mean of the strongest three matches + 0.20 × centroid similarity. Window quality = best branch + 0.70 × branch gap − 0.25 × strongest common/junction evidence + 0.03 × start/N. Diverse top-k aggregation is default; best-window behavior remains an explicit comparison.

Default decision checks are ordered: both branch scores weak (`best < 0.54`) → unknown; inadequate separation (`gap < 0.04`) → uncertain; best below recognition threshold (`best < 0.58`) → unknown; otherwise known branch. Strong thresholds affect the explanation, not a different decision class. Confidence is a bounded heuristic, not calibrated probability. A graph explicitly labeled low-quality withholds acceptance.

## Reproducibility and evidence

The same pure API runs inside video orchestration and evaluation. Artifacts bind source, inputs, configuration, relevant dependencies and encoder identity; stage output hashes are checked before resume. Sample metadata preserves source indices and nominal `index/FPS` times. No camera acquisition timestamp is claimed.

Actual Keras loaded weights are content-hashed. The local-weight path restores Keras ImageNet's additional weight-conditioned scaling layer; otherwise identical arrays produce different descriptors. A real ImageNet/local-file parity test protects this behavior. No mobile model conversion has been validated.

CLI and Streamlit are local research entry points. Streamlit uses isolated per-session data, unique run IDs, bounded uploads and persistent downloads. It has no authenticated hosted-service contract.

See [evaluation](/docs/evaluation-plan.md), [artifact contract](/docs/artifact-contract.md), [reproduction](/docs/reproduction.md) and [limits](/docs/safety-and-limitations.md). The supplied system SVG covers the broader product and keeps team-reported detection separate from this offline core.

Per-frame component evidence is reused across overlapping windows by default. An explicit window-recomputation path preserves the reference arithmetic for parity and runtime diagnostics. Fixture tests compare decisions and all window qualities within 2e-6; this changes computational reuse, not thresholds, route scope or physical guidance.
