<h1 align="center">VisionX</h1>

<p align="center">
  <strong>Assistive wearable vision concept with a verifiable offline visual route-memory research core</strong><br>
  A judge-facing SIH 2026 evidence website that clearly separates the intended VisionX product from what is currently implemented and experimentally validated.
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-research%20%2B%20judge%20build-blue">
  <img alt="Core" src="https://img.shields.io/badge/core-VXN--RAMNet-purple">
  <img alt="Frontend" src="https://img.shields.io/badge/site-static%20Node.js-success">
  <img alt="Testing" src="https://img.shields.io/badge/testing-Node%20%2B%20Playwright-orange">
  <img alt="Deploy" src="https://img.shields.io/badge/deploy-Vercel-black">
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#what-this-repo-contains">Contents</a> ·
  <a href="#implemented-pages">Pages</a> ·
  <a href="#features">Features</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#deployment">Deployment</a>
</p>

---

## Overview

**VisionX** is the intended assistive wearable product concept.

The current repository is the compact, deployment-ready **SIH 2026 judge/evidence website** used to present the product, architecture, research evidence, reproducibility material, and implementation boundaries.

The most important distinction is:

```text
VisionX
= intended assistive product / wearable system

VXN-RAMNet
= currently implemented offline camera-only route-memory research core
```

The repository does **not** claim that the full wearable route-guidance stack has been validated end to end. It intentionally exposes what is implemented, what is experimental, what is team-reported, and what remains target/future integration.

---

## What This Repo Contains

| Area | What is included |
|---|---|
| Judge-facing website | Product, problem, architecture, evidence, business, references, and reproduction pages. |
| VisionX visual assets | Canonical product and architecture visuals used in the presentation website. |
| VXN-RAMNet source snapshot | The Python research-core source bound to the release evidence package. |
| Executed evidence | Benchmark summaries, timing data, threshold sweeps, decision outputs, plots, verification summaries, and selected logs. |
| Claim traceability | Documentation linking presentation claims to source/evidence and identifying implementation boundaries. |
| Reproduction guidance | Steps for reproducing the bounded VXN-RAMNet evidence path. |
| Static-site build | Node-based generation/check pipeline for a small Vercel deployment. |
| Browser verification | Playwright viewport/accessibility checks for the judge-facing site. |
| Demo redirect | `/demo` redirects judges to the configured VisionX YouTube demonstration video. |

---

## Implemented Pages

| Page | Purpose |
|---|---|
| `/` | High-level VisionX problem/solution presentation. |
| `/architecture.html` | Current vs target architecture and system boundaries. |
| `/source.html` | Source evidence behind implementation claims. |
| `/evidence.html` | Executed benchmark/verification evidence. |
| `/reproduce.html` | Reproduction workflow for the bounded research core. |
| Business / references / research pages | Supporting product, research, and citation material. |
| `/demo` | Immediate redirect to the configured YouTube judge/demo video. |
| `docs/claim-evidence-matrix.md` | Claim-to-evidence traceability. |

---

## Features

| Area | Current Implementation |
|---|---|
| Compact judge deployment | High-volume generated/raw evidence is excluded from deploy source while compact verifiable evidence remains available. |
| VXN-RAMNet source evidence | The implemented Python visual route-memory core is included as source/evidence material. |
| Reproducibility | Benchmark manifests, reports, hashes, source snapshots, and reproduction documentation support technical review. |
| Claim boundaries | Implemented, experimental, team-reported, target, and unvalidated capabilities are kept distinct. |
| Evidence integrity | Judge-pack metadata records hashes and provenance for compact and archived evidence packages. |
| Static deployment | Vercel-ready static site generated from repository source. |
| Responsive review | Judge-facing pages are built for desktop/tablet/mobile review. |
| Accessibility checks | Playwright/axe-oriented browser verification is part of the repository workflow. |
| Demo routing | Centralized demo configuration redirects `/demo` to the selected YouTube video. |
| Source-file budget | Build checks enforce a compact source tree suitable for clean hackathon deployment. |

---

## User / Judge Flow

```text
Open VisionX site
  ↓
Understand the assistive-use problem
  ↓
Review proposed VisionX solution
  ↓
Inspect current vs target architecture
  ↓
Inspect VXN-RAMNet source + evidence
  ↓
Review benchmark/reproduction limits
  ↓
Open demo video
  ↓
Trace claims through the evidence matrix
```

The judge-facing experience is intentionally evidence-first: the site should make it difficult to confuse a proposed wearable component with a validated implementation.

---

## Architecture

### Current evidence boundary

```text
Completed video input
  ↓
Frame validation + deterministic sampling
  ↓
Visual descriptors
  ↓
Constrained route-memory construction
  ↓
Branch / revisit / turnaround evidence
  ↓
Known / uncertain / unknown decision
  ↓
Versioned reports + benchmark evidence
```

### VisionX target product path

```text
Wearable camera / sensors
  ↓
Embedded/mobile perception
  ↓
Visual route memory + context
  ↓
Assistive decision logic
  ↓
Audio / haptic user feedback
```

The second flow is the **target product architecture**. The current repository does not establish full end-to-end implementation or safety validation of that target path.

---

## Key Product / Research Differentiators

- **GPS-free visual route-memory direction** for constrained learned-route scenarios.
- **Offline research core** that can be inspected and reproduced without a cloud inference dependency.
- **Abstention / uncertainty behavior** instead of forcing a confident route label for every query.
- **Evidence-first hackathon presentation** that separates implementation from future product architecture.
- **Reproducibility artifacts** linking code, configuration, hashes, reports, and benchmark outputs.
- **Compact judge build** designed to stay reviewable rather than shipping generated dependency/evidence noise.

These are project differentiators. They are not a claim that VisionX is a certified mobility aid or that the current experiment generalizes to arbitrary navigation.

---

## Current vs Target Capability

| Layer | Current status | Boundary |
|---|---|---|
| VXN-RAMNet offline visual route memory | Implemented research core | Constrained one-junction/two-branch experiment; requires enrollment. |
| VXN uncertainty/abstention | Implemented experimental logic | Thresholds are not a clinically/safety calibrated probability model. |
| Cached/vector benchmark evidence | Implemented evidence | Diagnostic, not representative field accuracy proof. |
| Pi + camera + ToF + Android + object-detection path | Team-reported / presentation evidence | Device/session/source completeness varies; do not present as fully audited VXN integration. |
| Mobile VXN route integration | In progress / target | Not yet established as validated live route guidance. |
| IMU / ultrasonic fusion / full wearable guidance | Proposed/target | Not implemented by the VXN-RAMNet repository baseline. |
| Certified assistive navigation | Not claimed | Requires extensive safety, field, human-factor, and device validation. |

---

## Structure

```text
VisionX/
├── assets/
├── docs/
├── evidence/
├── scripts/
├── tests/
│   └── unit/
├── site.config.json
├── package.json
├── vercel.json
├── README.md
└── generated public/ output during build
```

Generated/dependency-heavy directories such as `node_modules/`, build output, Playwright reports, and bulky archived evidence are intentionally excluded from the deploy source.

---

## Local Verification

```bash
npm run build
npm test
npm run dev
```

For full browser/accessibility regression:

```bash
npm ci
npx playwright install chromium
npm run test:e2e
```

The build verifies repository integrity, local page/assets, evidence references, security-sensitive markup, source identity, compact evidence constraints, and the configured source-file budget.

---

## Demo Configuration

The judge route is centralized in `site.config.json`.

```bash
npm run set:demo -- "https://www.youtube.com/watch?v=VIDEO_ID" "VisionX recording title" "Recording owner"
npm run build
```

`/demo` is generated as an immediate, standards-based redirect with a fallback link.

---

## Deployment

The repository is designed as a static Vercel site.

Typical deployment:

```text
Framework Preset: Other / static build
Build Command: npm run build
Output Directory: public
Root Directory: repository root
```

No live database, backend API, or model-download step is required for the judge-facing static site.

---

## Validation & Research Limits

The repository provides meaningful **engineering and reproducibility evidence** for the website and VXN-RAMNet snapshot. That is different from scientific or safety validation of the full VisionX product.

Current evidence does not establish:

- arbitrary-route navigation;
- physical left/right semantic understanding from Branch A/B labels;
- held-out city-scale generalization;
- calibrated probability of navigation correctness;
- validated live wearable route timing;
- validated mobile parity;
- certified safety for visually impaired users.

Those require dedicated field protocols, independent labels, failure-case analysis, calibration, human-factor testing, hardware telemetry, and safety evaluation.

---

## Important Notes

- Branch A/B represent exploration order, not guaranteed physical left/right.
- VXN-RAMNet uses no GPS input, but it requires prior route enrollment.
- Cached/synthetic benchmark timing excludes parts of a real wearable pipeline such as capture, decoding, networking, Android, and speech.
- Proposed architecture must not be presented as already implemented.
- Preserve project/source provenance when reusing the evidence package.

---

## License & Provenance

Use the repository’s included licensing and attribution files as the authoritative source.

The project deliberately preserves the distinction between **VisionX product concept**, **current VXN-RAMNet implementation**, **team-reported hardware/app evidence**, and **future integration scope**.
