# Actual benchmark results

These tables are generated from the executed reports in evidence/. Regression and simulated vectors are not held-out field accuracy or mobile guidance evidence.

## notebook04-regression

Regression and synthetic diagnostics establish reproducible software behavior. They do not establish held-out route accuracy, mobile speed, safe navigation or user benefit.

Source SHA-256: `f2dac1f0de9a06c9ea8b712fcb5c59ffabbfa2c7a440c078fbc8c47cbeac6257`. Hardware: {"cpu_model": "Snapdragon(R) X Plus - X1P42100 - Qualcomm(R) Oryon(TM) CPU", "logical_processors": 8, "process_architecture": "AMD64", "host_architecture": "ARM64", "architecture_mismatch": true, "note": "Architecture mismatch may indicate emulation; timings are specific to this environment."}.

| Method | Accepted / total | Errors among accepted | Correct known / known | Known macro F1 | Unknown false accepts / unknown | Median ms | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| vxn_default | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 7.492 | 8.794 |
| vxn_reference_windows | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 86.165 | 88.919 |
| vxn_disjoint_best | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 7.991 | 9.760 |
| vxn_legacy | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 8.457 | 9.075 |
| vxn_original_only | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 7.949 | 8.673 |
| vxn_no_temporal_prior | 1 / 2 | 0 | 1 / 2 | 0.5000 | undefined | 8.329 | 9.350 |
| fixed_branch_a | 2 / 2 | 1 | 1 / 2 | 0.3333 | undefined | 0.001 | 0.002 |
| global_centroid | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 0.065 | 0.079 |
| last_frame_nn | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 0.571 | 0.959 |
| mean_frame_nn | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 2.164 | 2.941 |
| dtw_suffix | 2 / 2 | 0 | 2 / 2 | 1.0000 | undefined | 17.742 | 18.166 |

[notebook04 report](/evidence/notebook04/report.json) · [decisions](/evidence/notebook04/decisions.csv) · [raw timings](/evidence/notebook04/timings.csv) · [checksums](/evidence/notebook04/checksums.json)

![Executed cached classifier runtime](/evidence/notebook04/figures/classifier-runtime.png)

## synthetic-stress-v1

Regression and synthetic diagnostics establish reproducible software behavior. They do not establish held-out route accuracy, mobile speed, safe navigation or user benefit.

Source SHA-256: `f2dac1f0de9a06c9ea8b712fcb5c59ffabbfa2c7a440c078fbc8c47cbeac6257`. Hardware: {"cpu_model": "Snapdragon(R) X Plus - X1P42100 - Qualcomm(R) Oryon(TM) CPU", "logical_processors": 8, "process_architecture": "AMD64", "host_architecture": "ARM64", "architecture_mismatch": true, "note": "Architecture mismatch may indicate emulation; timings are specific to this environment."}.

| Method | Accepted / total | Errors among accepted | Correct known / known | Known macro F1 | Unknown false accepts / unknown | Median ms | p95 ms |
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

[synthetic report](/evidence/synthetic/report.json) · [decisions](/evidence/synthetic/decisions.csv) · [raw timings](/evidence/synthetic/timings.csv) · [checksums](/evidence/synthetic/checksums.json)

![Executed cached classifier runtime](/evidence/synthetic/figures/classifier-runtime.png)

## Interpretation

Classification timing excludes capture, image decoding, EfficientNet, mobile, transport, buffering and speech. Warm-up samples are excluded; measured repeats do not create extra journeys. The same heuristic thresholds on different score distributions do not establish fair calibrated superiority. Null/undefined risk is retained when a method abstains on every query.

The precomputed-frame-score path is compared with explicit window recomputation using the same arithmetic and learned memory. Fixture parity tests compare decisions and all window scores within 2e-6. This is an engineering reuse optimization, not a new recognition model or field efficacy result.

Memory arrays and self-similarity for every enrollment variant are retained under each evidence/memory folder with paired metadata/checksums. Figures use actual data; scripts/plot_evidence.py records plotting/version/source provenance. These bytes do not establish process peak RAM.
