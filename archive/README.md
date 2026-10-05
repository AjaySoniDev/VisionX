# VisionX full evidence archive

`visionx-full-evidence-2026-10-01.zip` preserves the complete pre-consolidation `evidence/` tree used for the 1 October 2026 release, including NPZ memories/fixtures and per-query window-evidence JSON.

It is intentionally excluded from Vercel by `.vercelignore`. The deployed site uses the curated `evidence/` judge pack, whose `judge-pack.json` records this archive SHA-256 and hashes every deployed evidence file.

Restore for offline inspection with:

```bash
unzip archive/visionx-full-evidence-2026-10-01.zip -d restored-full-evidence
```

Do not interpret archival retention as new scientific validation; the same regression/synthetic evidence boundaries remain in force.
