# Research and component references

External sources support context, established methods and component APIs. They never establish VisionX accuracy, safety, battery life, user benefit, pricing or market superiority.

| Presentation topic | Primary source | Role / limit |
|---|---|---|
| Vision impairment | [WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment) | General accessibility context; global prevalence is not the target market |
| Indoor navigation needs | [Plikynas et al., Sensors 2020](https://www.mdpi.com/1424-8220/20/3/636) | User needs and existing approaches; not a VisionX evaluation |
| Recorded-route retracing | [OCCaM Lab Clew](https://github.com/occamLab/Clew) | Direct prior art; current app behavior not independently tested here |
| Sequence visual recognition | [Milford & Wyeth, SeqSLAM, ICRA 2012](https://ieeexplore.ieee.org/document/6224623/) | Sequence matching predates this project; the implemented DTW baseline is not SeqSLAM |
| Selective classification | [Geifman & El-Yaniv, 2017](https://arxiv.org/abs/1705.08500) | Risk and coverage motivation; no guarantee transferred to this heuristic |
| EfficientNetB0 | [Keras API](https://keras.io/api/applications/efficientnet/efficientnet_models/) | Frozen encoder/preprocessing reference; no route-performance transfer |
| Pi capture node | [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) | Hardware interfaces and capture/transport feasibility, not achieved speed |
| Offline voices | [Android Voice API](https://developer.android.com/reference/android/speech/tts/Voice) | Network-required voice flag; provision and test the actual voice |
| Mobile runtime option | [LiteRT for Android](https://developers.google.com/edge/litert/android) | Target deployment option, not a validated VXN mobile export |

The actual ImageNet/local-weight graph discrepancy was inspected in the installed official Keras implementation and corrected with a tested scaling-layer restoration. Both outputs use the same frozen weights. This release does not claim mobile export parity.

The current upstream source URL is [AjaySoniDev/VXN-RAMNet](https://github.com/AjaySoniDev/VXN-RAMNet). The supplied ZIP is the audited input and the final ZIP is the upgraded local release. No new remote commit or deployment is claimed.

The judging demo route `/demo` redirects to the project video supplied for review: [VisionX demonstration video](https://www.youtube.com/watch?v=c-RgSsNwhqw). The video is a presentation/demo artifact; implementation and validation claims remain bounded by the code and evidence packaged with this site.

Historical extensive prior-art and business research is preserved under `assets/presentation/` with a source-material notice. The current status, claim matrix and execution evidence supersede its earlier hardware/status assumptions.
