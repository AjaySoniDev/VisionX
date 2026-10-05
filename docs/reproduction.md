# Reproduction guide

Run commands from the extracted repository root using Python 3.11 or 3.12. The provided ZIP is the release source; the upstream repository is not automatically updated by this delivery.

## Core environment

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements/core-dev.lock
python -m pip install --no-deps -e .
python -m ruff check src tests scripts apps
python -m ruff format --check src tests scripts apps
python -m mypy src/vxn_ramnet
python -m pytest -m "not vision" --cov=vxn_ramnet
python -m build
```

The core works without TensorFlow or Streamlit. Optional UI tests skip if Streamlit is absent. Coverage has no package-file omissions and enforces an 80% statement/branch threshold.

## Cached fixture

```bash
vxn-ramnet evaluate --manifest benchmarks/manifests/notebook04.json --output evidence/reproduced-notebook04 --repeats 5 --warmups 1
```

This validates source/input hashes, learns the memory, compares ten methods and retains all declared queries. Use a fresh output directory. The two labels are inherited regression expectations: historical RIGHT_BRANCH maps to exploration-order BRANCH_B and LEFT_BRANCH to BRANCH_A. They are not physical direction annotations.

## Vector stress suite

```bash
vxn-ramnet generate-synthetic --output data/synthetic --seed 2026
vxn-ramnet evaluate --manifest data/synthetic/manifest.json --output evidence/reproduced-synthetic --repeats 5 --warmups 1
```

Generation produces 100 enrollment vectors and 84 queries of 60 vectors. These are simulated descriptors, not camera observations or independent human sessions. The generated data directory is omitted from the release ZIP so the command can create it. The evidence includes the complete manifest snapshot and generation protocol.

## Full encoder and UI

```bash
python -m pip install -r requirements/vision-ui.lock
python -m pip install --no-deps -e .
# PowerShell: $env:VISIONX_TEST_IMAGENET='1'
# POSIX: export VISIONX_TEST_IMAGENET=1
python -m pytest -m vision
streamlit run apps/streamlit_app.py
```

The explicit encoder smoke test resolves ImageNet weights and tests normalization plus local-weight descriptor parity. It uses a generated test image and does not evaluate navigation. Keras/TensorFlow can emit an upstream NumPy conversion deprecation warning during weight serialization; the evidence records it rather than treating it as a classifier failure.

## Your own completed videos

Place trusted, appropriately collected learning and query videos outside managed output directories. Copy `configs/camera_baseline.yaml`, change paths and keep the one-junction/two-branch enrollment script.

```bash
vxn-ramnet validate-config --config configs/camera_baseline.yaml
vxn-ramnet run --config configs/camera_baseline.yaml
```

The configuration's relative project root resolves from its file location; the shipped root is `..` relative to `configs/`. Relative local weights resolve inside that project root. For network-independent model resolution, set `weights: local`, provide an approved `.weights.h5` checkpoint, choose the correct `local_preprocessing` and set `allow_remote_weight_resolution: false`. The default local preprocessing matches Keras's ImageNet graph, including its weight-dependent scaling layer. `keras_untrained` is an explicit alternative for checkpoints created without that scaling.

No raw videos, approved model-weight file, Android app or Pi acquisition code was supplied or added. The optional UI is a local research interface, with isolated session storage, bounded uploads, persistent result downloads and explicit deletion.

## Artifact inspection and resume

Read the configuration, input manifest, sampling provenance, paired NPZ/JSON memory, raw windows, reports, stage states and logs together. Nominal sampling timestamps are `frame_index / reported_FPS`, not hardware acquisition times.

Resume requires the same run ID, meaningful configuration, input bytes, encoder identity, source content and relevant dependency versions. Output checksums must also pass. Legacy runs without this identity are explicitly rejected; choose a new run ID. Changes never silently reuse stale results. Recomputed stages invalidate downstream caches.

Decision and event identities are reproducible under the pinned environment. Timings and serialized evaluation timestamps/process IDs vary. Verify each report's own checksums, then compare semantic outcomes rather than demanding byte-identical reports from separate executions.
