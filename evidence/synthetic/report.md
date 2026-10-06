# Executed VXN-RAMNet evaluation

Dataset: **synthetic-stress-v1**. Purpose: **synthetic**.

Regression and synthetic diagnostics establish reproducible software behavior. They do not establish held-out route accuracy, mobile speed, safe navigation or user benefit.

Generated at: 2026-10-01T10:12:37.028162+00:00. Source SHA-256: `f2dac1f0de9a06c9ea8b712fcb5c59ffabbfa2c7a440c078fbc8c47cbeac6257`.

All numbers below come from this run. Null means an undefined denominator or an unsupported measurement.

| Method | Accepted / journeys | Accepted errors | Correct known / known | Known macro F1 | Unknown false accepts / unknown | Query median ms | Query p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| vxn_default | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 1.975 | 2.665 |
| vxn_reference_windows | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 23.818 | 26.052 |
| vxn_disjoint_best | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 1.999 | 2.919 |
| vxn_legacy | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 1.977 | 2.893 |
| vxn_original_only | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 2.011 | 2.970 |
| vxn_no_temporal_prior | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 1.991 | 2.724 |
| fixed_branch_a | 84 / 84 | 60 | 24 / 48 | 0.3333 | 24 / 24 | 0.001 | 0.001 |
| global_centroid | 0 / 84 | 0 | 0 / 48 | 0.0000 | 0 / 24 | 0.031 | 0.040 |
| last_frame_nn | 58 / 84 | 10 | 48 / 48 | 1.0000 | 0 / 24 | 0.300 | 0.553 |
| mean_frame_nn | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 0.385 | 0.712 |
| dtw_suffix | 48 / 84 | 0 | 48 / 48 | 1.0000 | 0 / 24 | 3.222 | 3.977 |

## Interpretation

- Cached descriptors only: capture, video decoding, EfficientNet inference, Android, Wi-Fi and audible output are excluded from classifier timing.
- Timing samples repeat the same journeys; repetitions do not increase dataset size. p95 uses NumPy linear interpolation.
- Regression labels/event anchors come from the supplied expectations, not independently annotated ground truth. Original source-video/session/model-weight provenance was not supplied.
- Synthetic vectors exercise decision mechanisms; they do not model real camera, corridor, participant or mobile distributions.
- Fixed-A is a predeclared forced-choice baseline. Other baselines share default heuristic thresholds with differing score distributions; comparison is diagnostic, not calibrated superiority evidence.
- Threshold sweeps describe these cases only. No threshold selection or probability calibration is performed. Unknown AUROC/AP is undefined without known and unknown journeys.
- Memory bytes cover named NumPy arrays, not process peak RSS or complete deployment memory. One-junction/two-branch scope remains.
- Known accuracy and macro F1 include abstentions as missed known labels. Ambiguous cases are excluded from unknown ranking metrics.

## Enrollment events

Indices refer to sampled embeddings, not source-video frames or seconds.

| Variant | First junction | Turnaround | Revisit | Anchor mean absolute error (frames) |
|---|---:|---:|---:|---:|
| default | 25 | 51 | 76 | 0.3333333333333333 |
| legacy | 25 | 51 | 76 | 0.3333333333333333 |
| original_only | 25 | 51 | 76 | 0.3333333333333333 |
| no_temporal_prior | 25 | 51 | 76 | 0.3333333333333333 |

## Reproduce

`vxn-ramnet evaluate --manifest data/synthetic/manifest.json --output evidence/reproduced-synthetic-stress-v1 --repeats 5 --warmups 1`

Inspect `report.json`, `decisions.csv`, `timings.csv`, `threshold-sweep.csv`, `manifest.snapshot.json` and `checksums.json` together.
