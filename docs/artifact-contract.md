# Artifact and resume contract

Each run lives in a marked `artifacts/runs/<run-id>/` directory. Replacement requires the marker and a contained path. All input preflight and encoder initialization precede managed replacement; inputs cannot live in managed output roots.

```
<run-id>/
  .vxn-run
  config.snapshot.json
  resume-identity.json
  manifest.json
  inputs/preflight.json
  inputs/frame-extraction.json
  frames/                    # optional retention
  embeddings/learning/ and queries/  # paired NPZ/JSON
  memory/route-memory.npz and route-memory.json
  reports/queries/, query-decisions.json, summary.json, query-results.csv, report.md
  logs/pipeline.jsonl
  stages/*.json
```

Frame provenance remains under `inputs/` when frame images are deleted. Source indices and nominal `index/FPS` times do not claim true acquisition timestamps or perfect OpenCV seek fidelity.

NPZ forbids pickle/object arrays, rejects invalid numerics/duplicates and bounds expanded size. JSON input rejects duplicate fields, nonstandard numbers and oversized content. Writes are atomic; output JSON rejects NaN/Infinity. Memory metadata schemas are checked on read and write; dimensions, integer labels/indices, component order/counts and normalized descriptors must match. Array/metadata pairs carry a SHA-256 binding; this detects accidental mismatch, not malicious authorship or authenticated signing.

Resume identity includes meaningful configuration, input bytes, encoder manifest, source content hash and relevant dependency versions. Resume/overwrite flags do not change scientific identity. Changed inputs/configuration/source/model/environment or legacy absent identity explicitly reject resume without rewriting cached evidence. Stage completion requires declared output hashes. Recomputing a stage invalidates later states. Removed frames can be bypassed only while matching embedding outputs remain valid.

Stage records retain status, elapsed seconds, output hashes and redacted failure type/reason. Detailed diagnostics are an explicit local option. Reports sanitize CSV formula prefixes and Markdown fields. Software exceptions are not converted into physical route instructions.

Artifact schema remains 1.0.0 with additive provenance/checksum fields; old valid memory arrays can still be read, while legacy run-resume identity is explicitly unsupported. Paths now resolve relative to the configuration file; the baseline configuration uses `project_root: ..`.

Evaluation uses a fresh output directory and retains `report.json`, `report.md`, `manifest.snapshot.json`, `decisions.csv`, `timings.csv`, `threshold-sweep.csv`, per-query window evidence and `checksums.json`. Each fresh run has its own timestamp/environment. Verify its hashes and compare semantic decisions/indices; runtime fields need not be byte-identical.
