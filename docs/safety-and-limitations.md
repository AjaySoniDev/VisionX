# Intended use and limitations

This is controlled offline route-memory research. Use it for inspectable software demonstrations and experiments. It does not establish a certified mobility aid, medical device, collision-avoidance system, safe independent navigation or replacement for existing mobility tools.

The core uses completed local videos and one junction/two taught branches. Event locations depend on temporal search priors; query windows use future portions of completed journeys. Horizontal flipping does not synthesize reverse camera observations. BACKTRACK is stored but not directly classified. Thresholds, quality labels and confidence are uncalibrated heuristics.

Passing tests and cached/vector benchmarks establish the exercised software behavior. They do not establish generalization across physical routes, users, days, cameras, lighting, crowds or hazards. Unknown-route metrics are unavailable on the two-query fixture. The generated stress dataset is simulated. No physical/mobile/user result is invented.

The current PPT's Pi/Android YOLOv8s detection test and approximately one-hour run are team-reported. This repository does not contain Pi/app source or reproduce that bench session. VL53L0X is the current named distance sensor; the component photo is not proof of wiring. IMU fusion, live VXN route inference and physical turn/fault policy remain future or unvalidated integration.

For future user-facing work: keep route, proximity and system-fault outputs separate; require fresh supported route state for route cues; cancel stale speech; provide accessible stop/unavailable/recovery behavior; evaluate real direction/progress/timing, resources and fault injection before supervised intended-user testing. A distance reading never proves path clearance.

Local processing does not itself prove privacy compliance. Before participant collection, define consent, bystander minimization, access, retention, export and deletion. The local Streamlit UI is not a public authenticated service. No cost, market, safety, clinical or environmental outcome is claimed.
