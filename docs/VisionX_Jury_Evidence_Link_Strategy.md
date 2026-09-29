# VisionX — Jury Clickable-Evidence Strategy

**Prepared:** 30 September 2026 (IST). **Goal:** let a judge verify the implemented core quickly, then inspect limitations and the proposed deployment path.

## Decision

Replace **LIVE PROTOTYPE** with **CORE EVIDENCE** on Slides 2 and 3. Keep the two small call-to-action elements as **Open Pack** on Slide 2 and **View Code** on Slide 3. Link the Slide 4 business-model label to the proposed model.

A recorded execution of the offline core is valuable, but it must say **Offline Core Demo** and identify the actual computer used. Do not label a completed-video run as live navigation, a system walkthrough as execution, or an Android screen mock-up as an integrated wearable prototype.

No functioning demo, video, repository snapshot, evaluation dataset or public team-owned evidence URL was supplied with this request. This work creates the five requested refinement documents/graphic, not a new VXN-RAMNet execution or deployment. The destination plan below is exact about required contents and readiness; missing URLs are not fabricated.

## Recommended link destinations

| PPT label | Slide placement | Destination | What judges see | Why it matters | Evidence provided | Claim boundary | Priority |
|---|---|---|---|---|---|---|---|
| CORE EVIDENCE / Open Pack | Existing Slide 2 prototype label and button | One published, read-only evidence index. Host URL: NOT PROVIDED. Recommended document title: `VisionX — Core Evidence` | A maturity statement, a short real offline execution clip if available, sample outputs, a source link and a current limitations box | Gives the strongest evidence without making the judge search folders | Traceable core behavior if the team supplies it; otherwise documentation only | Product integration remains proposed. Explicitly state when the pack contains no execution evidence | P1 |
| CORE EVIDENCE / View Code | Existing Slide 3 prototype label and button | Team's verified source repository, preferably a commit-pinned README/evidence index | Core entry point, config, memory schema, decision code, tests and run instructions | Connects the diagram to implementation | Inspectable source at a declared version | Repository presence or passing tests does not prove route accuracy, safety or mobile integration | P1 |
| PROPOSED BUSINESS MODEL | Existing Slide 4 business label | Published read-only rendering of `VisionX_Business_Revenue_Model.md`; public URL NOT PROVIDED | Institutional entry model, customer/user split, conditional revenue, costs, stage gates and unknowns | Demonstrates practical deployment thinking | Researched proposal and validation plan | No traction, sales, partnerships, price or funding entitlement is claimed | P2 |
| Nine short source labels | Existing Slide 6 reference groups | Exact official/paper URLs in the final text and research register | The primary sources supporting need, prior art, components and abstention | Makes consequential claims checkable | External context and feasibility evidence | External research cannot validate VisionX | P1, as source citations |
| Working Core Demo | Inside the evidence index, not a new PPT box | Reproducible local-run instructions or a maintained demo endpoint ONLY after tested; no endpoint supplied | Actual file selection, enrollment, query processing and decision output | Lets technical reviewers reproduce the narrow task | Executable core behavior on disclosed hardware | Rename `Offline Core Demo` if it is a recording. Never call it a live wearable system | P2 conditional |
| Evaluation Evidence | Inside the index, or Slide 4 only after real results exist | Versioned report with trial-level results, config and inputs | Held-out session design, baselines, accepted errors, coverage, unknown false acceptance and failures | Distinguishes a selected demo from scientific evidence | Product-specific evaluation if actually conducted | A roadmap is not an evaluation result; currently publish `Validation Roadmap` instead | P1 when available |
| System Walkthrough | Inside the index, after execution evidence | Narrated architecture video or readable diagram with maturity labels | Sensor/phone split, enrollment/query paths, target output and missing contracts | Helps non-specialist judges understand the plan | Design explanation | Animation and target architecture are not implementation evidence | P3 |

### Repository destination: evidence and limit

Current public search indexed Ajay Soni's GitHub profile with VXN-RAMNet as a pinned public project: [AjaySoni-Dev](https://github.com/AjaySoni-Dev). The candidate repository is [AjaySoni-Dev/VXN-RAMNet](https://github.com/AjaySoni-Dev/VXN-RAMNet), but direct retrieval was blocked in this session. Treat it as a **candidate to open and verify**, not a tested destination or freshly audited codebase.

The supplied master report cites audit commit `762c20abf78dd5c5411671fbe680c0b26c232405`. Do not construct a commit URL and assume it exists; verify that revision in the actual repository. If the current code differs, record the newer revision and regenerate matching outputs. Preserve source authorship, licenses and collaborators.

## Strongest configuration with a hard link limit

The counts below refer to external hyperlink destinations. Source names and years should remain visible even when they are not clickable. If the limit includes reference hyperlinks, put the full external reference links inside the evidence index and keep Slide 6 labels as plain text.

| Allowed destinations | Configuration | Reason |
|---|---|---|
| 1 | A single evidence index, reused from Slides 2–4 if multiple clickable objects are allowed | One entry gives core evidence first, with source, validation roadmap, business model and references beneath it |
| 2 | Evidence index on Slide 2 + verified commit-pinned source on Slide 3 | Combines immediate comprehension with inspectable implementation. Keep the business document in the index |
| 3 | Evidence index + verified source snapshot + actual evaluation report if one exists | Execution, code and measurement make the strongest case |
| 3, with no evaluation yet | Evidence index + verified source snapshot + proposed business model | Fits the current evidence. The index visibly states that a held-out benchmark is pending |

If “only one link” means one clickable object, place it on Slide 2 and remove redundant link controls from other slides. Removed controls have zero characters and therefore do not violate the supplied budgets. Do not leave `View Code` visible without a working destination.

## Evidence-index layout

Make the first screen readable in roughly half a minute:

1. **VisionX: proposed product. VXN-RAMNet: offline camera-only research core.** Date and evidence/code revision immediately below.
2. **Offline Core Demo**, if recorded from actual execution. Otherwise a visible “Execution recording not yet supplied” status and the implementation documentation.
3. **What exists:** constrained route components, completed-video queries and Known/Uncertain/Unknown outputs, with links to actual evidence.
4. **What remains:** causal streaming, mobile integration, physical turn contract, optional sensors, representative benchmark and supervised user validation.
5. **Inspect:** source snapshot, sample run/report, validation roadmap, architecture, proposed business model and curated references.

Prefer a static, no-login page or read-only document over an unstable public Streamlit instance that needs cold-start model downloads. A hosted research UI adds availability, file-upload, resource and privacy risks; it should supplement a reliable static evidence package only after those issues are addressed. No site or repository is published by this deliverable.

## What to attach in the pack

| Suggested file or section | Minimum contents | Status in this request |
|---|---|---|
| `Core_Demo.mp4` | Genuine offline execution, actual hardware, source revision/config and inputs; show a known branch and a refusal case | NOT SUPPLIED; team must record |
| `Run_Manifest.json` | Version/config/model identity, input IDs, parameters, timestamps and actual run status | NOT SUPPLIED; retain actual fields, do not invent absent provenance |
| `Sample_Decisions.json` or core's actual output format | Actual decision, branch scores/separation, selected evidence windows and state for the shown runs | NOT SUPPLIED |
| `Route_Memory_Example` | Actual persisted components and their provenance, sanitized for public review | NOT SUPPLIED |
| `Evaluation_Evidence` | Complete held-out results with failures and denominators | MISSING; substitute a labeled validation roadmap until produced |
| `Validation_Roadmap` | Data splits, baseline/ablation plan, unknown cases, mobile parity/runtime and supervised usability gates | Covered by final text and business-model documents |
| `System_Architecture.svg` | Supplied approved Slide 3 architecture with target labels intact | SUPPLIED design evidence |
| `VisionX_Business_Revenue_Model.md` | Conditional deployment and revenue model, cost drivers and unknowns | CREATED by this refinement |
| `VisionX_Research_References.md` | Curated sources with supported claims and limits | CREATED by this refinement |

Use consented, non-sensitive journey footage. Redact faces, private rooms, identifiers and sensitive metadata where necessary. A sanitized public subset should still identify which outputs came from which input and code version. Do not publish a token, secret, private route or participant identity to make the evidence link work.

## Suggested actual-demo recording

**Target duration: 90–120 seconds**, a presentation recommendation rather than an achieved asset.

| Segment | Show | State explicitly |
|---|---|---|
| Opening | Version and device, local files, core entry point | “Offline VXN-RAMNet core processing completed videos” |
| Enrollment | One structured teaching journey and saved common path/junction/branches/backtrack | The route topology is constrained; enrollment builds memory rather than retraining a new neural network |
| Recognition | Independent query recordings for the taught branches, actual outputs and evidence | Branch A/B are route labels, not left/right instructions |
| Refusal | A real uncertain or unknown result with its input and output | Thresholds are heuristic; a single demonstration is not an accuracy benchmark |
| Closing | Current/target comparison and validation next steps | Android streaming, live guidance and user impact remain unvalidated |

Trim dead waiting only if clearly disclosed. Do not replace model outputs, hard-code refusal, splice unrelated successes into a continuous-run claim or hide laptop computation behind an Android screen. If a desired refusal case does not occur, report the failure and investigate it; do not stage the result.

## Character-budget-safe link labels

| Existing element | Original characters | Final label | New characters | Result |
|---|---:|---|---:|---|
| Slide 2: LIVE PROTOTYPE | 14 | CORE EVIDENCE | 13 | PASS |
| Slide 2: Click Here | 10 | Open Pack | 9 | PASS |
| Slide 3: LIVE PROTOTYPE | 14 | CORE EVIDENCE | 13 | PASS |
| Slide 3: Click Here | 10 | View Code | 9 | PASS |
| Slide 4: PROPOSED BUSINESS AND REVENUE MODEL | 35 | PROPOSED BUSINESS MODEL | 23 | PASS |

Counts above include the exact source extraction's characters as normalized in the final text audit; use that audit as the authoritative count record. Do not expand the existing button to `Working Core Demo` without a new layout/budget decision. The longer label belongs inside the destination page.

## Final link checks before submission

- Open every team-owned destination while signed out, on another device and from the exported presentation/PDF. A local `sandbox:` link is for downloading these deliverables, not a public jury destination.
- Verify that the destination title, code revision and demo outputs agree with the deck. Freeze a reviewable snapshot and retain the original evidence.
- Use read-only access. Avoid request-access walls, editable shares, expiring signed links and folder structures that require the judge to hunt for files.
- Confirm videos play without downloading a large archive. Provide captions and a transcript, and make source/evidence text selectable.
- Verify each paper title against the destination. The old erroneous Visual Teach and Repeat and selective-classification links must not survive. The selected abstention destination is `https://arxiv.org/abs/1705.08500`.
- Remove a button if the destination is not ready. A plainly labeled documentation pack is better evidence than a promised demo that cannot be opened.

**Remaining publishing work:** supply actual execution evidence if available, verify the source destination, publish the index and business/research documents with suitable access, then insert and test the final URLs. No credentials or account changes are needed merely to read the recommended evidence.
