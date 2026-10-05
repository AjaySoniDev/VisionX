# Executable evaluation

The benchmark entry point is `vxn-ramnet evaluate`. It runs the same `learn_route_memory` and `RouteRecognizer` API used by the video pipeline. It never substitutes a prewritten result table.

- `manifests/notebook04.json` pins the supplied cached fixture and its inherited regression labels.
- `vxn-ramnet generate-synthetic` creates the explicitly simulated vector stress cases.
- `evidence/notebook04` and `evidence/synthetic` contain actual executed results, per-journey decisions, windows, timings, sweeps and checksums.
- A new physical study must declare `purpose: held_out`, separate acquisition sessions and frozen query labels, then use its own manifest. See the dataset and methodology contract in [evaluation plan](../docs/evaluation-plan.md).

The supplied fixture and synthetic diagnostics do not establish representative route accuracy or mobile performance. No threshold tuning is performed by the evaluator. Use a fresh output path on each run.
