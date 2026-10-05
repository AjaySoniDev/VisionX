# VisionX SIH deployment checklist

## Before importing to Vercel

- Keep `package.json`, `vercel.json`, `scripts/`, `assets/`, `docs/`, `evidence/` and the root CSS/JS files unchanged.
- Do not commit `public/`, `node_modules/`, `validation/`, Playwright output or Vercel local state.
- Keep `archive/visionx-full-evidence-2026-10-01.zip` in the repository/package for offline provenance; `.vercelignore` prevents it from being uploaded to Vercel.
- Run `npm run build` and `npm test`.
- If network access is available, run `npm ci`, install Chromium and run `npm run test:e2e`.

## Vercel settings

No manual overrides are required when `vercel.json` is honored:

- Framework: Other / static
- Build: `npm run build`
- Output: `public`
- Environment variables: none
- Production package install: skipped by `installCommand`

## SIH judge check

Open these routes after deployment:

- `/`
- `/architecture.html`
- `/evidence.html`
- `/source.html`
- `/reproduce.html`
- `/demo.html`

Confirm the demo page still states that the current external video is a placeholder unless the team has replaced it with a real VisionX recording.

## Claim discipline

Do not present cached/synthetic benchmark results as held-out field accuracy, the team-reported Pi/Android test as independently reproduced evidence, or target mobile route assistance as implemented. The site intentionally labels these boundaries for technical credibility.
