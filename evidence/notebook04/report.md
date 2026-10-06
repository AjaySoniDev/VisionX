# Executed VXN-RAMNet evaluation

Dataset: **notebook04-regression**. Purpose: **regression**.

Regression and synthetic diagnostics establish reproducible software behavior. They do not establish held-out route accuracy, mobile speed, safe navigation or user benefit.

Generated at: 2026-10-01T10:12:08.779957+00:00. Source SHA-256: `f2dac1f0de9a06c9ea8b712fcb5c59ffabbfa2c7a440c078fbc8c47cbeac6257`.

All numbers below come from this run. Null means an undefined denominator or an unsupported measurement.

| Method | Accepted / journeys | Accepted errors | Correct known / known | Known macro F1 | Unknown false accepts / unknown | Query median ms | Query p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| vxn_default | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 7.492 | 8.794 |
| vxn_reference_windows | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 86.165 | 88.919 |
| vxn_disjoint_best | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 7.991 | 9.760 |
| vxn_legacy | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 8.457 | 9.075 |
| vxn_original_only | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 7.949 | 8.673 |
| vxn_no_temporal_prior | 1 / 2 | 0 | 1 / 2 | 0.5000 | 0 / 0 | 8.329 | 9.350 |
| fixed_branch_a | 2 / 2 | 1 | 1 / 2 | 0.3333 | 0 / 0 | 0.001 | 0.002 |
| global_centroid | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 0.065 | 0.079 |
| last_frame_nn | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 0.571 | 0.959 |
| mean_frame_nn | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 2.164 | 2.941 |
| dtw_suffix | 2 / 2 | 0 | 2 / 2 | 1.0000 | 0 / 0 | 17.742 | 18.166 |

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
| default | 60 | 134 | 193 | 0.0 |
| legacy | 60 | 134 | 193 | 0.0 |
| original_only | 60 | 134 | 191 | 0.6666666666666666 |
| no_temporal_prior | 32 | 135 | 191 | 10.333333333333334 |

## Reproduce

`vxn-ramnet evaluate --manifest benchmarks/manifests/notebook04.json --output evidence/reproduced-notebook04-regression --repeats 5 --warmups 1`

Inspect `report.json`, `decisions.csv`, `timings.csv`, `threshold-sweep.csv`, `manifest.snapshot.json` and `checksums.json` together.
