# VisionX SIH deployment checklist

## Before importing to Vercel

- Keep `package.json`, `vercel.json`, `scripts/`, `assets/`, `docs/`, `evidence/` and the root CSS/JS files unchanged.
- Do not commit `public/`, `node_modules/`, `validation/`, Playwright output or Vercel local state; `.gitignore` and `.vercelignore` enforce this packaging boundary.
- The bulky full-evidence archive is intentionally omitted from the lightweight deployable source; its original identity is retained in `evidence/judge-pack.json`.
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
- `/demo` — immediate redirect to the configured VisionX YouTube demo

## Claim discipline

Do not present cached/synthetic benchmark results as held-out field accuracy, the team-reported Pi/Android test as independently reproduced evidence, or target mobile route assistance as implemented. The site intentionally labels these boundaries for technical credibility.
