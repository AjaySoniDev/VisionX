# VisionX system boundary and integration target

![Presentation system architecture](/assets/presentation/VisionX_02_System_Architecture.svg)

The supplied current PPT/SVGs distinguish three paths:

1. **Team-reported working detection test:** camera + VL53L0X → Pi Zero 2 W hotspot → Java/XML Android receive/connection verification → YOLOv8s → phone TTS/headphones. The approximately one-hour report is not an independent resource or navigation benchmark.
2. **Implemented offline research:** Python VXN-RAMNet builds and compares constrained route memories from completed videos.
3. **In-progress / planned integration:** VXN on Android, causal route inference and the complete route/proximity/fault output policy. Pi-connected IMU turn/backtrack fusion is planned.

Pi/app source, named phone/runtime, packet logs, frame freshness, latency, battery and thermal records were not supplied. This release does not invent those implementations. The earlier JPEGs in `assets/architecture/` are historical target designs, not current integration evidence.

## Contracts still required

- A selected route/destination, topological progress, incoming approach and intended outgoing edge before physical turn guidance.
- Acquisition/session/sequence identity, clock semantics, bounded buffering, packet loss/reorder/stale detection and explicit reconnect behavior.
- Desktop/mobile descriptor and ranking parity under the exact preprocessing/runtime.
- Separate output rules for route status, proximity warning and system fault; cancellation of stale route speech and accessible manual stop/recovery.
- Independent IMU calibration and event evaluation before a visual/inertial ablation.
- Measured power, enclosure, sustained resources, accessibility and supervised intended-user outcomes.

The distance observation is limited proximity evidence, not path clearance or universal obstacle detection. Local Wi-Fi remains necessary for the reported capture link even if internet-independent trip processing is the target. A frozen model, installed route memory and provisioned offline voice still require setup.

No clinical benefit, safe independent navigation, all-day battery, arbitrary graph routing or general physical left/right instruction is established. The current offline core has three semantic outcomes; it does not implement the complete phone unavailable/fault state machine.
