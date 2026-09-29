# VisionX — Business, Revenue and Deployment Model

**Decision date:** 30 September 2026 (IST). **Maturity:** proposed commercial model around an implemented offline research core. No customer demand, pilot, partnership, selling price, revenue or commercial viability has been validated in the supplied evidence.

## Recommended model

Start with **institution-supported evaluation**, then consider a **wearable kit plus enrollment, training and ongoing support** for selected taught routes. A campus accessibility unit, rehabilitation organization or NGO can coordinate recruitment, supervised use and maintenance. This is a proposed B2B2C service: an organization may pay while a blind or low-vision traveler uses the aid.

The first offer should be a bounded research/evaluation engagement, with a route scope, named devices, failure-handling protocol and evidence report. Sell a supported assistive product only after engineering and user-evaluation gates pass. Initially provide route confirmation/status; do not sell independent turn-by-turn navigation that the core cannot yet supply.

This recommendation is an inference from VisionX's integration and support needs, not proof of institutional buying interest. WHO identifies provision, cost and workforce barriers in assistive technology (R10). User research supports checking actual navigation needs and preferences before assuming familiar-route assistance is useful (R15). References and direct URLs appear in `VisionX_Research_References.md`.

## Evidence labels

| Label | Meaning in this model |
|---|---|
| SOURCED VALUE | A fact supported by an identified external primary source or supplied technical evidence |
| ESTIMATE | A calculation with explicit inputs; no numerical commercial estimate is offered because cost and demand inputs are missing |
| ASSUMPTION | A proposition to test, such as institutional willingness to fund enrollment/support |
| TARGET | Intended behavior, operating condition or commercial milestone |
| UNKNOWN | Missing evidence, including price, margins, acquisition cost, demand, retention and field reliability |

## Users, buyers and initial use case

| Stakeholder | Role / value sought | Evidence status |
|---|---|---|
| Blind or low-vision traveler with a specific unresolved route need | Consenting user and co-designer; understandable route confirmation alongside their usual mobility aid | TARGET segment; size and willingness to use UNKNOWN |
| Campus disability/accessibility unit | Possible first sponsor or purchaser; coordinated access to selected recurring routes | ASSUMPTION; no commitment supplied |
| Rehabilitation or educational organization | Co-design, orientation-and-mobility expertise, training and supervised evaluation | Potential collaborator; no partnership exists in the evidence |
| NGO or CSR funder | May fund access, loan equipment or evaluation costs | Potential payer, not product-demand validation |
| Facilities team | Route permissions, notice of layout changes, route retirement and re-enrollment | TARGET operational role |
| Team Synexis | Core development, integration, traceable evaluation, support and incident review | Work allocation proposal, not proof of a staffed support operation |
| Hardware/assembly provider | Reliable parts, safe enclosure/power integration, repair and quality checks | Prospective supplier, unselected |
| Government/procurement body | Possible later channel after eligibility, certification and evidence review | Future option, not a current customer |

**Initial setting:** a controlled campus route with one junction and two taught branches, where a specific user still wants confirmation despite existing mobility skills. Match the actual camera-only core's topology. Hospitals are a possible later institutional setting, but busy clinical corridors, changing obstructions and unfamiliar visitors exceed the first scope. Exclude street crossing, evacuation, emergency guidance and arbitrary destinations.

**Customer discovery must permit a “no.”** If normal orientation skills, a simple phone aid or an existing product solves the task better, narrow or stop the wearable proposal. Do not make disability itself a proxy for product need.

## Value proposition and alternatives

The proposed value is **personal branch-memory assistance with inspectable evidence and explicit uncertainty**, provisioned for a small taught route set. Its prospective advantages are route-specific enrollment and phone-side computation. Both require measured comparisons before becoming selling claims.

| Alternative | Relevant existing capability | Implication for VisionX |
|---|---|---|
| Existing mobility skills, cane and orientation support | User's established strategy | Primary baseline for usefulness; retain these during evaluation |
| Clew | Developer documentation describes indoor path recording/retracing using ARKit (R03) | Personal route recording is established. Compare task and enrollment burden honestly |
| GoodMaps | Prepared venue models support camera-based positioning; self-scanning is also offered (R11) | Do not claim competitors always need expensive installed hardware. VisionX offers much narrower route coverage |
| NaviLens | Installed visual codes provide accessible information/navigation in documented sites (R12) | No installed marker is an operating distinction, not proof that natural-scene matching is more reliable |
| IIT Delhi SmartCane | Ultrasonic ranging and tactile obstacle information (R13) | Proximity sensing addresses a different layer; VisionX is not a replacement or proven superior aid |
| SHG Smart Vision Glasses | Vendor describes phone-connected visual assistance and offline subfunctions (R14) | Wearable-to-phone assistance is not unique; compete on the route task only |

The sustainable asset, if demonstrated, would be reliable enrollment tools, a well-evaluated decision method, accessible interaction and maintainable provisioning. No patent moat, scientific novelty, exclusive dataset or established network effect is claimed. Any future licensing must first verify the team's rights to code, weights, data and third-party components and preserve authorship/upstream notices.

## Route-to-market options

| Model | Fit now | Decision and trade-off |
|---|---|---|
| Direct B2C device sale | Low | Defer: transfers setup/support burden to users before usefulness, reliability and cost are known |
| Institutional supported deployment | Best candidate after evaluation | Recommended initial commercial direction: concentrates training and route maintenance; procurement and support can still be slow/expensive |
| NGO/CSR-supported access | Useful enabling channel | Pursue only with a funded maintenance plan and user choice. Sponsorship is not recurring product revenue |
| B2G procurement | Later | Certification, approved categories, procurement terms and service capacity require checking; no access to a scheme is established |
| Hardware-only sales | Poor | Route enrollment, software updates and user support are integral; a box of parts is not a deployable aid |
| Software-only licensing | Later experiment | A simpler phone-only version may be preferable. License the core only when integration contracts, performance and support boundaries are stable |
| Subscription per navigation use | Poor | Avoid monetizing every trip or withholding essential fault/status functions. It conflicts with the target of dependable local use |

## Adoption path and commercial gates

| Stage | Work / deliverable | Evidence to progress | Commercial treatment |
|---|---|---|---|
| 0. Reproduce core | Freeze code/config/weights and reproduce local learning/query runs | Actual run logs, data provenance, known and refusal cases, resolution of reported CI/cache issues | Research activity; no product offer |
| 1. Validate decision task | Independent-session queries; unknowns; baseline/ablation comparison | Accepted error with coverage, unknown false acceptance, variability and failures | Research funding or explicit evaluation agreement only |
| 2. Mobile integration | Named Android phone, exact preprocessing parity, causal query design and local speech | Conversion/ranking parity; sustained timing, memory, heat and power; no-internet restart test | Engineering evaluation; no real-time promise before measurement |
| 3. Wearable integration | Pi capture/transport, bounded queues, session IDs, freshness and watchdogs | Link-loss, stale-frame, restart and audio-output failure tests; safe power/enclosure review | Supervised demonstrator, with route/status assistance only |
| 4. User co-design | Accessible recruitment and consent; mobility specialist oversight; user's normal aid retained | Comprehension, wrong turns, interventions, workload, preference, enrollment burden and withdrawals | Supported study; no efficacy or independence claim |
| 5. Limited deployment | Defined routes/conditions, trained support owner, service scope and rollback | Evidence that intended users benefit and the organization can support total cost | First conditional kit/service offer |
| 6. Replication | Repeat the same validated scope at another setting | New-site results and repeatable setup/support cost | Scale only where evidence transfers |

These are gates, not promised dates. Optional IMU verification, proximity sensing and a custom battery assembly must not block the minimum camera-to-phone route-status demonstrator. Add them only with hardware, calibration, failure tests and measured value. Full turn guidance needs a separate progress/direction/timing contract and cannot be unlocked merely by passing a branch benchmark.

## Revenue model

| Possible revenue stream | Payer / charging unit | What would be delivered | Preconditions and status |
|---|---|---|---|
| Bounded evaluation service | Institution or research sponsor, per agreed study | Integration work, setup, transparent measurements and limitations report | Written scope and adequate supervision; PROPOSED, not booked revenue |
| Kit sale or managed loan | Institution, per supported device | Tested camera node, mount, regulated power, required accessories and compatible software | Validated bill of materials, quality checks, warranty/support capability; TARGET |
| Initial enrollment and training | Institution, per deployment with defined route/user scope | Route recording, checks, accessible training and handover | Demonstrated enrollment workflow and staff competency; TARGET |
| Support / maintenance agreement | Institution, per term and agreed service scope | Updates, troubleshooting, route revalidation, repairs/replacements as specified | Real ongoing service and transparent inclusions; TARGET |
| Core/SDK licensing | Integrator, per agreed integration | Versioned interface and documented evidence boundary | Stable API, reproducibility, IP/dependency review and demand; DEFER |

Do not charge twice for the same setup work under kit and enrollment line items. Clearly separate research grants/donations from customer revenue. An annual fee is justified only by actual recurring maintenance and support, not simply because subscriptions appear attractive. Base local functionality, accessible stop and fault communication should remain usable under the purchased/loaned product terms without trip-by-trip billing.

## Cost model and affordability

No credible rupee price can be inferred from a Pi board price. Obtain dated Indian supplier quotations, confirm availability and taxes, and measure integration/support effort before publishing price ranges.

| Cost layer | Required inputs | Present status |
|---|---|---|
| Device bill of materials | Pi, camera, correct cable, storage, mount, enclosure, safe regulated power, charging parts, audio interface; optional sensors separately | UNKNOWN full landed cost |
| Smartphone | Supported handset/OS, available memory and storage, runtime compatibility and replacement/loan needs | UNKNOWN device floor; borrowed phone is not economically free |
| Manufacturing / quality | Assembly, testing, power/enclosure review, defective units, calibration where relevant, packaging | UNKNOWN |
| Provisioning | Staff minutes for enrollment, verification, training, accessibility accommodation and data handling | UNKNOWN; measure in pilots |
| Recurring service | Support hours, route changes, software updates, warranty/repair reserve, spares and logistics | UNKNOWN |
| Development / assurance | Dataset collection, participant compensation, engineering, secure storage, documentation and relevant independent reviews | UNKNOWN |
| Distribution / administration | Travel, channel effort, payment delays, institutional procurement, accounting and contract costs | UNKNOWN |
| End-of-life | Repair, data erasure, collection and responsible electronics/battery disposal | TARGET process; cost UNKNOWN |

**Calculation framework, not a forecast:**

- Delivered kit cost = parts + assembly/test + packaging/logistics + applicable charges + expected warranty cost.
- Deployment cost = kits + phone provision if required + enrollment/training + site setup + support over the stated term.
- Contribution = collected revenue − attributable delivery, support, channel and warranty costs.
- Break-even deployment volume = fixed operating cost ÷ positive contribution per deployment. If contribution is negative, scaling increases loss.

Do not insert assumed zero support cost or ignore donated hardware. Keep cash expenditure and total economic cost separate. Quantify phone-only versus wearable total ownership cost for equivalent route/status functionality.

**Affordability targets:** institution-owned loan kits, reuse of compatible phones, optional rather than mandatory sensor upgrades, repairable modules and subsidized access where a sponsor commits. Reuse between participants requires fit, hygiene, re-enrollment and data separation. Basic access should not depend on uploading identifiable route videos or accepting advertising. All affordability measures remain proposals until actual terms and costs exist.

## Distribution, partnerships and Indian context

Start with a small number of consenting users and a named accessibility/rehabilitation contact. Provide an accessible quick-start, supported-device list, clearly bounded route scope and a reachable support owner. Record route changes and remove obsolete route memories before reuse. Facilities teams maintain physical accessibility; VisionX should not become a substitute for accessible infrastructure.

**Potential collaborations:** accessibility cells for needs discovery; orientation-and-mobility professionals for trial design; rehabilitation organizations for training; hardware specialists for enclosure/power review; NGOs or CSR sponsors for access and support funding. These are target roles, not partner logos to place in the PPT.

**SOURCED VALUE:** the official DEPwD ADIP page describes assistance for obtaining aids/appliances and states that supplied devices need due certification (R19). The department describes ALIMCO's ADIP and CSR-related distribution roles (R20). **UNKNOWN:** whether a future VisionX device fits an approved category, is eligible, meets relevant certification requirements or could be procured. Confirm the then-current scheme documents, category and procurement route before making any funding assumption. No government endorsement, reimbursement, subsidy or purchase order is implied.

Keep government access as a later possibility. The initial business case must remain viable without an assumed ADIP approval or CSR award.

## Sustainability and scalability

**Financial:** assess support burden and repeatable enrollment before adding sites. A broad Android compatibility promise would multiply testing and support costs; start with named supported hardware. Revenue must fund maintenance and defect response, not only initial assembly.

**Operational:** retain versioned memories, device/config records, rollback to the last tested build, an incident log and a route-retirement policy. No remote administrator should be able to silently change a user's active route policy. Planned updates need regression and calibration checks.

**Technical:** the current five-component core is not a multi-junction graph engine. Scaling the number of deployments is different from extending route topology. Longer journeys, larger databases and general routing require new bounded-memory, indexing and causal-state designs. Run separate science and resource evaluations for such changes.

**Environmental:** reuse of a phone and modular repair are design targets. Added electronics, batteries, charging and replacement may offset any avoided infrastructure. Measure energy over the same task and service life, track repairs and include device manufacture/disposal in any later life-cycle comparison. ISO 14040 provides a relevant assessment framework (R21); no net environmental saving or compliance claim is made.

## Principal risks and decisions they trigger

| Risk / assumption | Validation | Decision if unsupported |
|---|---|---|
| Users do not need confirmation on the chosen familiar route | Interviews and observed tasks | Select a documented unmet task or stop that deployment |
| Wearable adds less value than a phone-only setup | Matched task/usability comparison | Use the simpler configuration; do not defend hardware for its own sake |
| Unknown routes produce accepted matches | Frozen unseen-route testing | Tighten scope/policy and report reduced coverage; do not issue turn cues |
| Mobile conversion or timing changes decisions | Desktop/mobile parity and causal event tests | Retain a research demo until the mobile gate passes |
| Failures leave stale speech queued | Disconnect, freeze, app-stop and output-failure tests | Block participant deployment until recovery policy is reliable |
| Support/route upkeep makes the product unaffordable | Staff-time and total-cost records | Redesign enrollment, narrow scope or reject the model |
| Institutional/CSR interest fails to convert | Buyer interviews and concrete budget discussions | Do not forecast revenue; reassess channel |
| Camera data exposes private spaces or bystanders | Data minimization, consent, retention/deletion, pairing/access controls | Limit collection and halt inappropriate deployments |
| Component or handset variability | Supported configuration and repeated bench tests | Restrict compatibility until measured |

## Minimum evidence before commercialization

1. A reproducible core version and honest benchmark with independent journeys, unknowns and fair baselines.
2. Named mobile/wearable hardware with parity, causal timing, thermal, power and failure/recovery evidence.
3. Accessible enrollment, selection, stop and status flows tested with intended users and relevant expertise.
4. Demonstrated usefulness relative to existing strategies, with failures, withdrawals and limitations retained.
5. Dated complete cost model, support workload, repair plan and a buyer willing to pay for the stated scope.
6. Rights/dependency review, data-handling controls and a confirmed applicable product/procurement compliance path.

**PPT line:** “Supervised campus evaluation → Institutional pilot → Kit + enrollment/training + support, if validated.”

**Jury answer:** “We propose institution-supported evaluation first. If users benefit and the full cost is supportable, revenue could come from the kit, enrollment/training and maintenance. We have not validated pricing, paying demand or government eligibility.”
