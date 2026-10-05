# VisionX — SIH 2026 Vercel judge build

This repository is the compact, deployment-ready VisionX presentation/evidence website for Smart India Hackathon 2026. It is intentionally structured for fast Vercel builds, low repository noise, and technical judge traceability.

## What is deployed

The Vercel build publishes:

- the VisionX project, architecture, research, evidence, demo, reproduction, business, references and source-review pages;
- the canonical presentation SVGs and wearable media used by the UI;
- executed benchmark summary JSON/Markdown, decision CSVs, timing CSVs, threshold sweeps and plots;
- recorded verification summaries, JUnit output, coverage data and selected raw check logs;
- the complete `vxn_ramnet` Python package source snapshot bound to the release SHA-256;
- readable Python test source and evaluation/configuration manifests;
- claim/evidence, safety, architecture, evaluation and audit documentation.

The deployed website does **not** claim live validated navigation. VXN-RAMNet remains an offline bounded route-memory research core; the Pi/Android object-detection path is team-reported; mobile route integration remains in progress.

## Why the repository is compact

The original evidence export contained hundreds of per-query synthetic JSON files plus binary NPZ memories and fixture arrays. Those files are valuable for forensic/research retention but add little value to a Vercel judge review.

They are therefore preserved once in:

`archive/visionx-full-evidence-2026-10-01.zip`

That archive is excluded from Vercel through `.vercelignore`. Its SHA-256, byte size and original file count are recorded in `evidence/judge-pack.json`. The same manifest hashes every evidence file that is deployed.

The repository enforces a hard **300 source-file budget** during `npm run build`; generated folders such as `public/`, `validation/` and dependency folders are excluded from that count.

## Local verification

Production generation uses Node.js built-ins only; no runtime npm dependency is required.

```bash
npm run build
npm test
npm run dev
```

`npm run build` regenerates `public/` and verifies:

- local pages, fragments, images and documentation links;
- CSP-sensitive HTML/SVG conditions;
- benchmark/source/judge-pack checksums;
- release source identity;
- absence of high-volume evidence trees from deploy source;
- the <=300 source-file constraint.

For full browser/accessibility regression in a network-enabled development/CI environment:

```bash
npm ci
npx playwright install chromium
npm run test:e2e
```

The GitHub Actions workflow performs build, unit tests, Playwright viewport checks and automated WCAG scanning.

## Vercel deployment

Import the repository with its root set to this folder. `vercel.json` defines:

- build command: `npm run build`
- output directory: `public`
- production dependency install: skipped, because the production build uses Node built-ins only
- security headers: CSP, `X-Content-Type-Options`, frame denial, referrer policy and permissions policy

No environment variables, database, backend service or model download are required for this static SIH site.

The canonical configured URL is `https://visionxassistive.vercel.app`.

## Judge review path

1. `/` — problem framing and implementation boundaries
2. `/architecture.html` — current vs target system paths
3. `/source.html` — exact release code behind key claims
4. `/evidence.html` — executed results, denominators, checks and judge-pack integrity
5. `/reproduce.html` — reproduction procedure and scope limits
6. `/docs/claim-evidence-matrix.md` — presentation claim traceability

## Full evidence archive

The archive is for offline inspection and is intentionally not part of the hosted site:

```bash
unzip archive/visionx-full-evidence-2026-10-01.zip -d restored-full-evidence
```

Archival retention does not strengthen the scientific claims. The regression fixture and generated-vector suite are software/research evidence, not a held-out field-navigation benchmark, safety certification, or user-benefit validation.

## Demo configuration

The current demo link is explicitly marked as a temporary external placeholder. Replace it with the actual VisionX recording before final judging when available:

```bash
npm run set:demo -- "https://www.youtube.com/watch?v=VIDEO_ID" "VisionX recording title" "Recording owner"
npm run build
```

`set:demo` accepts only a specific HTTPS YouTube video URL and never converts an external video into implementation evidence by itself.

## License and provenance

The software license and third-party attribution files remain intact. Upstream/source provenance is preserved; proposed architecture is not represented as implemented capability.
