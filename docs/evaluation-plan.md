# Executable evaluation methodology and research protocol

## Available evidence

The evaluator is implemented in `src/vxn_ramnet/evaluation/` and calls the shared learning/recognition API. Published reports are actual runs with source/input checksums, configuration, environment, per-journey outcomes, window evidence, repeated timing samples, sweeps and artifact hashes.

| Dataset | Unit and size | Provenance | Valid inference |
|---|---|---|---|
| notebook04-regression | One 270×1280 enrollment pair; two 120×1280 query pairs | Supplied cached NPZs and inherited event/label expectations. Original recordings, sessions, independent annotations and original weights incomplete | Software regression fidelity, default/legacy diagnostic comparison and local cached runtime |
| synthetic-stress-v1 | 100×64 enrollment; 84 queries of 60×64 vectors: 48 known, 24 unknown, 12 ambiguous | Disclosed NumPy generator, seed 2026, equal original/flip vectors, fresh vector perturbations | Mechanism diagnostics, metric/test correctness and local runtime; no physical camera generalization |

Timing repetitions do not increase journey count. The fixed generator does not prove robustness to real blur, lighting, camera/head motion or similar corridors. Event indices in the fixture are regression anchors rather than independent ground truth. Vector junction/turnaround anchors describe generator geometry.

## Dataset manifest contract

JSON manifest fields include purpose (`regression`, `synthetic`, `held_out`), declared root, provenance, encoder provenance, learning record, query records, IDs, pinned NPZ SHA-256, acquisition/session IDs, splits and predeclared truth (BRANCH_A, BRANCH_B, UNKNOWN, AMBIGUOUS). Optional ordered event annotations include provenance.

The loader checks hashes, contained/distinct paths, duplicate file/content, unit normalized finite embedding pairs, frame/dimension bounds and total memory budget. Held-out purpose requires enrollment/test split roles and different enrollment/query session IDs. These checks cannot independently prove that a claimed acquisition record is honest, detect every near-duplicate or replace a collection/consent protocol. Exact encoder/collection provenance must accompany a real study.

Limits: at most 2,000 enrollment frames, 1,000 frames per query, 8,192 descriptor dimensions and the explicit total embedding budget (512 MB default). NPZ expanded size and JSON bytes are independently bounded. The current research topology remains one junction and two branches.

## Comparisons

All methods use the same automatically learned branch memory for the applicable ablation:

- Fixed Branch A is predeclared and forced-choice; it is not picked from query frequencies.
- Global centroid compares the suffix's descriptor/centroid evidence.
- Last-frame nearest neighbor uses one predetermined last frame.
- Mean frame nearest neighbor uses mean strongest memory match over the last 55% of the query.
- DTW suffix uses global dynamic-time-warp alignment and at most 64 samples per sequence. It is not SeqSLAM or a scientific replication of that paper.
- VXN default, disjoint best-window, legacy overlap/best-window, original-only and no-temporal-prior policies use the same public core.

Default heuristic acceptance thresholds are shared across methods with different score distributions. This is a diagnostic comparison, not calibrated superiority evidence. No threshold is tuned by the evaluator or selected from the final cases. Synthetic original/flip descriptors are equal, so that suite cannot measure benefit from flipping.

## Metrics and denominators

- **Coverage:** accepted known-branch outcomes / all declared journeys.
- **Selective risk:** incorrect accepted decisions / accepted decisions, including false acceptance on unknown or ambiguous cases. Null if none accepted.
- **Known decision accuracy:** correct accepted known-branch labels / known journeys. Abstentions count as missed decisions.
- **Known macro F1:** fixed two-branch macro average over known queries, treating abstentions as false negatives. Open-set failures are separately counted in accepted error and unknown metrics.
- **Unknown false acceptance:** unknown journeys accepted as either branch / unknown journeys. Null when no unknown journeys exist.
- **Unknown rejection:** explicit unknown_route outcomes / unknown journeys; uncertainty is separately abstention rather than identical rejection.
- **Ambiguous abstention:** uncertain/unknown outcomes / ambiguous journeys.
- **Unknown AUROC / average precision:** rank `-best_branch_score` on known versus unknown queries, excluding ambiguous cases. Tie handling is explicit and tested. Null without both populations or numeric scores; fixed-A has no ranking score.
- **Event mean absolute error:** predicted sampled-embedding index versus disclosed anchor, where supplied. No source-video time metric is inferred.
- **Failures:** retained in the confusion matrix and total denominator; classifier failures cause a nonzero run outcome after evidence retention.

Confidence remains a heuristic. No ECE, Brier score, calibrated probability, confidence interval about field risk or formal selective-classification guarantee is fabricated.

## Runtime measurement

Use `perf_counter_ns` around actual enrollment/classification calls. Record each measured repeat and warm-up policy. Median/p95 are computed with NumPy's ordinary linear percentile interpolation. Input loading, provenance collection, image decoding, EfficientNet, Wi-Fi, Android, queues and speech are excluded from the cached classifier measurement. Warm-up samples are omitted from timing aggregates, not from declared journey outcomes.

The environment identifies Python, installed libraries, CPU, OS, process/host architecture and threading variables. This review's Windows ARM host runs x64 Python under emulation; the observed hardware profile accompanies the evidence. No mobile performance, capture-to-audible latency or peak-process RAM is inferred. Memory byte fields count named NumPy arrays, not complete RSS/deployment memory.

## Required independent physical study

Define the task, operating conditions, annotations, baselines, error/coverage operating points and exclusions before seeing final outcomes. Keep development, calibration and final test acquisitions separate; use route/session/participant grouping as applicable. Nearby frames are not independent samples. Same physical taught route may recur across independent acquisitions, but claims about new layouts/participants require corresponding held-out splits.

Collect both branches, unknown lookalikes, common-path-only ambiguity, different lighting/viewpoints/speeds and partial/reverse traversal as explicitly different conditions. Ground truth needs annotation guidance and review. Retain corrupt/excluded records and reasons. Calibration uses only calibration data; final thresholds freeze before test evaluation. Compare baselines with appropriate calibration budgets, report failures and availability, then test causal decision timing separately from this completed-query core.

Mobile conversion/parity, real IMU ablations, stream faults and supervised user outcomes are separate future studies. No result in another publication or hardware component page transfers to this project. Reproduction commands are in [the guide](/docs/reproduction.md).

The eleventh method is explicit reference window recomputation, measured beside default precomputed-frame evidence. Paired fixture regression tests protect numerical/decision parity. Every enrollment variant also saves route memory and self-similarity with checksums. Optional scientific figures use `scripts/plot_evidence.py`; plotting versions and report/script hashes accompany them.
