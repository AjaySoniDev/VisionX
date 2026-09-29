# VisionX — Research and References

**Research checked:** 30 September 2026 (IST). **Purpose:** substantiate specific claims in the six-slide submission and its deployment/evidence documents. External sources establish context, prior art and component feasibility; they do not establish VisionX performance.

## Research conclusion

The defensible opportunity is a **constrained, personally taught branch-memory workflow**. Existing research and products already cover route retracing, sequence recognition, visual localization, marker-assisted guidance and abstention. VisionX's advantage remains a question to evaluate, not an established market gap with no competitors.

The proposed Pi-capture/Android-compute split uses established components, but transferring the core requires preprocessing and descriptor parity, a mobile implementation of the route logic, causal query processing and measured sustained resources. Neither an encoder API nor a mobile runtime proves the complete pipeline works on a phone.

Institution-supported evaluation is the recommended entry model because enrollment, training and maintenance are still material unknowns. That recommendation is an inference from the supplied project state and the provisioning/user-needs sources below. It is not a sourced finding that institutions will buy VisionX.

## Sources selected for Slide 6

Use exactly these nine short linked labels, organized into the three groups in the final text file. Keep detailed explanations here.

| ID | Title | Organization / Authors | Direct URL | Supported Claim | Relevant Slide | Why Included |
|---|---|---|---|---|---|---|
| R01 | Blindness and vision impairment, 10 February 2026 | World Health Organization | https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment | At least 2.2 billion people globally have near or distance vision impairment | 5; broad context for 1 | Corrects the statistic's definition. It is neither blindness prevalence nor VisionX's addressable market |
| R02 | Indoor Navigation Systems for Visually Impaired Persons: Mapping the Features of Existing Technologies to User Needs (2020) | Darius Plikynas, Arūnas Žvironas, Andrius Budrionis, Marius Gudauskis; Sensors 20(3), 636 | https://www.mdpi.com/1424-8220/20/3/636 | Indoor navigation/orientation needs and alternatives to GPS; user requirements matter | 1, 2, 5 | Grounds the bounded accessibility task. The reviewed need does not prove demand for this exact device |
| R03 | Clew: repository and project documentation | OCCaM Lab | https://github.com/occamLab/Clew | Indoor recorded-path retracing using ARKit is documented prior art | 2; jury differentiation | Prevents a false first-ever/personal-route-recording claim. Project documentation is not a current-version efficacy test |
| R04 | SeqSLAM: Visual route-based navigation for sunny summer days and stormy winter nights (ICRA 2012) | Michael Milford and Gordon Wyeth | https://ieeexplore.ieee.org/document/6224623/ | Sequence-based visual route recognition predates VXN-RAMNet | 2, 3, 4 | Establishes temporal-matching prior art and motivates a sequence baseline; no performance transfer |
| R05 | Selective Classification for Deep Neural Networks (2017) | Yonatan Geifman and Ran El-Yaniv | https://arxiv.org/abs/1705.08500 | Selective prediction trades coverage for accepted-prediction risk | 2, 4, 5 | Supports evaluating errors together with abstention/coverage. VXN-RAMNet has not implemented this paper's guarantees |
| R06 | EfficientNet models / EfficientNetB0 API | Keras | https://keras.io/api/applications/efficientnet/efficientnet_models/ | Official pretrained EfficientNetB0 interface and preprocessing behavior | 3, 4 | Supports the reported encoder choice and exact mobile-parity checks, not route accuracy |
| R07 | Raspberry Pi Zero 2 W: official specification | Raspberry Pi | https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/ | 512 MB RAM, 2.4 GHz Wi-Fi and CSI camera interface are available | 3, 4 | Grounds the capture/transport role. The architecture allocation is an engineering inference, not an application benchmark |
| R08 | LiteRT for Android | Google AI Edge | https://developers.google.com/edge/litert/android | Android on-device inference has an established runtime path | 3, 4 | Supports proposed deployment work only. The current VXN-RAMNet route logic, model conversion and resources still need validation |
| R09 | Voice API: isNetworkConnectionRequired | Android Developers / Google | https://developer.android.com/reference/android/speech/tts/Voice | Android exposes whether a selected speech voice requires network access | 3, 4 | Makes the proposed offline speech condition explicit: provision and test the actual offline voice |

**Slide labels:** WHO: vision impairment (2026); Indoor navigation needs (2020); Clew: recorded-route retracing; SeqSLAM (2012); Selective classification (2017); Keras EfficientNetB0; Raspberry Pi Zero 2 W; LiteRT for Android; Android speech: offline voices.

## Supporting references used only where they change a decision

These belong in supporting documents and jury preparation, not as twelve more links crowded onto Slide 6.

| ID | Title | Organization / Authors | Direct URL | Supported Claim | Relevant Slide | Why Included |
|---|---|---|---|---|---|---|
| R10 | Assistive technology, 2 January 2024 | World Health Organization | https://www.who.int/news-room/fact-sheets/detail/assistive-technology | Provisioning, workforce, cost and user participation are part of assistive-technology access | 4, 5; business model | Supports an evaluated service/support model rather than equating low component prices with affordability |
| R11 | GoodMaps Scan & Go | GoodMaps | https://goodmaps.com/scanandgo/ | The vendor offers smartphone-based venue scanning, processed into maps for its navigation platform | 2, 4; business alternatives | Corrects an outdated blanket claim that mapped services always require expensive site hardware or a professional surveyor. Venue preparation still exists |
| R12 | Accessible clinic in Nijmegen: Radboudumc + NaviLens | NaviLens, official case-study documentation | https://www.navilens.com/en/case-studies/radboud-umc-nijmegen | The documented deployment places visual codes at route decision points and room/entrance locations | 2, 5; business alternatives | Gives a concrete marker-based comparator; no claim that VisionX is more reliable or cheaper |
| R13 | SmartCane | IIT Delhi Assistive Technology Group | https://assistech.iitd.ac.in/smartcane.php | Cane-mounted ultrasonic ranging conveys obstacle distance through vibration | 2, 3; business alternatives | Distinguishes proximity information from route recognition and acknowledges Indian prior art |
| R14 | Smart Vision Glasses | SHG Technologies | https://shgtechnologies.com/products/smart-vision-glasses | Vendor describes phone-connected visual assistance and specific offline functions | 2, 4; business alternatives | Rules out wearable/phone/offline functionality as an exclusive VisionX proposition. Vendor documentation is not independent efficacy evidence |
| R15 | Exploring the use of smartphone applications during navigation-based tasks for individuals who are blind or who have low vision: future directions and priorities (online 2025; issue 2026) | Disability and Rehabilitation: Assistive Technology; primary indexed article/publisher record | https://pubmed.ncbi.nlm.nih.gov/40854009/ | Navigation-app choice depends on task and user needs; the study investigates adoption factors and gaps | 1, 4, 5; business discovery | Supports discovery and co-design rather than assuming all familiar-route travelers need the same aid. Abstract-level evidence, not an India-specific demand study |
| R16 | On the Estimation of Image-matching Uncertainty in Visual Place Recognition (CVPR 2024) | Mubariz Zaffar, Liangliang Nan, Julian F. P. Kooij | https://openaccess.thecvf.com/content/CVPR2024/html/Zaffar_On_the_Estimation_of_Image-matching_Uncertainty_in_Visual_Place_Recognition_CVPR_2024_paper.html | Match uncertainty is already a research topic within visual place recognition | 2, 4; jury challenge | Directly challenges generic novelty claims about confidence. It is not a component used by the supplied core |
| R17 | Visual Teach and Repeat for Long-Range Rover Autonomy (2010) | Paul Furgale and Timothy Barfoot | https://doi.org/10.1002/rob.20342 | Visual route teaching/repeating is established robotics research | 2, 3; prior-art boundary | Corrects the original wrong hyperlink and prevents overclaiming the teach-and-repeat concept. Rover results do not validate pedestrian assistance |
| R18 | Test your app's accessibility (Views) | Android Developers / Google | https://developer.android.com/guide/topics/ui/accessibility/views/testing-views | Manual and automated accessibility checks are needed for Android Views | 3, 4; deployment gates | Matches Java/XML app development. Calling a screen “accessible” is insufficient without runtime and user testing |
| R19 | ADIP scheme | Department of Empowerment of Persons with Disabilities, Government of India | https://depwd.gov.in/en/adip/ | ADIP supports aids/appliances and requires due certification for devices supplied under the scheme | 4; business/government possibilities | Makes scheme access conditional. No VisionX category eligibility, subsidy or endorsement has been established |
| R20 | Artificial Limbs Manufacturing Corporation of India | DEPwD, Government of India | https://depwd.gov.in/en/artificial-limbs-manufacturing-corporation-of-india/ | ALIMCO has assistive-device provision roles through ADIP and CSR-related channels | 4; business distribution | Establishes a real institutional ecosystem to investigate; it is not a partnership or purchase commitment |
| R21 | ISO 14040:2006 — Environmental management: Life cycle assessment: Principles and framework | International Organization for Standardization | https://www.iso.org/standard/37456.html | Environmental assessment needs an explicit lifecycle scope and inventory/impact methodology | 5; sustainability model | Supports measuring added electronics, energy and disposal before claiming environmental benefit; no conformity claim |

R15's author list was not exposed in the accessible excerpts used in this run; the exact title, journal and DOI `10.1080/17483107.2025.2544942` identify the work without inventing authors. Publisher record: https://www.tandfonline.com/doi/abs/10.1080/17483107.2025.2544942.

## Administrative source, kept off the research slide

| Title | Organization | Direct URL | Supported claim | Relevant slide | Why included / limit |
|---|---|---|---|---|---|
| Themes of Smart India Hackathon | Smart India Hackathon / Government of India | https://www.sih.gov.in/SIH_Themes | The MedTech/BioTech/HealthTech theme description matches the generic wording in the supplied cover | 1 | Used to distinguish the official theme from the project's own problem statement. Does not verify SIH26215, team ID, category, deadline or the 2026 guidelines |

The supplied 2026 guideline PDF could not be retrieved and the exact PS entry was not independently established. No eligibility, judging-criteria or submission-rule claim depends on that inaccessible PDF. Preserve the team's registered values and compare them with the authenticated portal/SPOC record before submission.

## Retrieval and cross-check log

| References | What was available during this research | How the evidence was limited |
|---|---|---|
| R01, R10 | Official WHO pages opened | Definitions/date verified directly; no inference from global prevalence to VisionX users or TAM |
| R02 | Primary publisher, PubMed and PMC indexed excerpts agreed on title/DOI/authors and indoor-navigation scope; direct full-page retrieval was restricted | Used for broad problem/user-needs framing, not detailed quantitative effectiveness |
| R03 | Repository documentation opened | Prior-art workflow only; no hands-on app test or latest-release guarantee |
| R04 | IEEE publication and paper indexed records located | Foundational sequence-matching context only; no borrowed performance metric |
| R05 | Author paper abstract opened | Reject-option principle and risk/coverage; no guarantee transferred |
| R06, R08 | Official API/runtime indexed documentation located; direct retrieval was restricted on some paths | Component feasibility only, not VisionX implementation or performance |
| R07, R09 | Official pages opened and relevant specification/API entries inspected | Hardware features and speech voice network flag, not achieved sustained runtime |
| R11–R14 | Official vendor/institution indexed pages retrieved; some direct opens were restricted | Documented mechanisms only, no superiority, pricing, availability or effectiveness comparison |
| R15 | Primary indexed abstract and publisher record | Task/adoption relevance only; full article not independently reviewed |
| R16, R17 | Primary conference/author/publisher records cross-checked | Prior art only. R16 author version: https://arxiv.org/abs/2404.00546. R17 author paper: https://furgalep.github.io/sbib/furgale_jfr10.pdf |
| R18, R21 | Official documentation/standard-scope excerpts | Validation/assessment methods only; not compliance certification |
| R19, R20 | Official department pages opened | Institutional context only; current programme eligibility must be checked separately |

An indexed primary result is weaker access than a fully opened article and is labeled accordingly. Retrieval restrictions do not establish that a URL is broken for judges. Team-owned evidence URLs still need signed-out testing; this research did not produce a public demo link.

## Consequential claim cross-checks

| Claim | Evidence chain | Final decision |
|---|---|---|
| Vision impairment is a substantial accessibility context | R01 definition + R02 indoor-navigation needs | Retain the exact WHO definition, explicitly exclude market-size interpretation |
| Indoor assistance has an unmet task worth investigating | R02/R15 + specific institutional route proposal | Present a bounded user-need hypothesis, not “no solution exists” |
| Personal route recording and sequence matching are novel | R03/R04/R17 show prior art | Remove broad novelty; focus on the implemented component-memory workflow |
| Known/Uncertain/Unknown makes the system safe | R05/R16 establish selective/uncertainty research; no VisionX field result | Retain explicit states, require accepted-error/coverage and failure testing |
| Smartphone inference is technically plausible | R06/R08 plus target architecture; R07 supports sensor-node interfaces | Retain as proposed integration; require parity, causal logic, latency, battery and thermal evidence |
| Audio can work without internet after setup | R09 + provisioned local assets and cold-start test | Keep as target condition, not a verified blanket property |
| Institutional channels could support access | R10/R19/R20 + identified support needs | Recommend investigation, with no partnership/funding implication |
| Reusing a phone yields net environmental benefit | R21 methodology + full lifecycle/cost unknowns | Remove outcome claim; retain measurement of energy, reuse and repairability |

## What was deliberately removed or kept off-slide

- Duplicate LiteRT overview/conversion/performance links: one runtime reference is sufficient on-slide; exact implementation docs belong with the eventual build.
- Generic Streamlit/Android Studio links: their existence is not the key feasibility question. The stack visual already names the tools.
- A second global assistive-technology population statistic: it adds little and risks looking like another market estimate.
- Patent comparisons and expansive competitor tables: unnecessary for this six-slide story. No patentability or freedom-to-operate claim is made.
- Generic metric-library links: a concrete independent-session evaluation plan is more useful than citing an API for F1.
- Unverified 2026 SIH PDF/PS claims: administrative verification remains explicit.
- The incorrect `arXiv:1610.01990` abstention link and IEEE `6630534` teach-and-repeat link: neither belongs in the presentation.

## Internal evidence and precedence

| Supplied artifact | Role in this refinement | Limit |
|---|---|---|
| `VisionX_Deep_Report(2).md` | Primary implementation/status account; cites audit commit `762c20abf78dd5c5411671fbe680c0b26c232405` | Secondary audit narrative supplied by the team, not a fresh execution in this session |
| `Defensibility_Research(2).md` | Prior-art challenge, design risks and proposed evaluations | Earlier diagram-based assessment; superseded by the technical report for reported implementation details |
| `SIH_PPT_All_Slide_Text(2).md` | Existing six-slide structure and independent text budgets | Slide 6 is an expanded reference document; actual PPT object layout is unavailable |
| `Slide_2_Image_1(2).svg` | Approved user/workflow visual | Shows completed-video core and target assistance, not end-to-end execution |
| `Slide_3_Image_1(2).svg` | Approved system partition and typed data/control/power paths | Target design, with core-status labels |
| `Slide_3_Image_2(2).svg` | Approved development/research-stack context | Technology logos do not prove runtime integration |
| `Silde_5_Image_1(2).svg` | Original benefits visual inspected before replacement | Overly broad benefits are replaced with maturity-labeled capability chains |

All three Markdown files were read completely and all four SVGs were rendered and inspected. No VXN-RAMNet performance number, cost, test-pass count, user trial or commercial result has been invented. Fresh code/test evidence, if supplied later, should supersede the dated audit narrative.
