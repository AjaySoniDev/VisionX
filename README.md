# VisionX SIH Core Evidence — Vercel-ready static site

This package reconstructs the VisionX SIH26215 core-evidence website as a dependency-light static deployment.

## Evidence boundary

- **VisionX** is the proposed assistive product.
- **VXN-RAMNet** is the implemented offline camera/video route-memory research core described by the supplied 29 Sep 2026 evidence.
- Wearable capture, Android streaming/inference, optional sensors, live turn timing/direction, representative held-out accuracy and supervised user benefit remain target/unvalidated unless newer evidence is added.

## Routes

- `/` — core evidence index
- `/business.html` — proposed business/revenue/deployment model
- `/references.html` — curated research and claim-to-source register
- `/docs/*` — source Markdown documents used by the site

## Deploy on Vercel

### Dashboard
1. Create a new Vercel project from this folder/repository.
2. Framework preset: **Other**.
3. Root directory: repository root.
4. Build command: leave empty.
5. Output directory: leave empty.
6. Deploy.

### CLI
```bash
npx vercel
npx vercel --prod
```

No environment variables are required.

## Local verification

```bash
npm run check
npx serve . -l 3000
```

Then open `http://localhost:3000`.

## Updating evidence

Do not convert planned/target architecture into implemented claims. Update the snapshot date/revision and attach matching run manifests, outputs and evaluation evidence when they actually exist.
