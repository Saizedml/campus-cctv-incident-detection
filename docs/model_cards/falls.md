# Falls FB0 model card

**Intended use:** research person-down triage with human review, not medical diagnosis. The causal geometry-only FB0 head consumes person tracks. R4 combines persistent down evidence with a fall-peak trigger and a per-operating-point border policy. Notices say **person down**. No weights are distributed.

**Locked headline:** q2 detects 321/914 (35.12%; Wilson 95% 32.09–38.27%), q5 556/914 (60.83%; 57.63–63.94%). MEVA-test FA/h is 9.4252/34.8865; NWPU is 32.0236/67.7071. **Revised primary ≤5 criterion (pre-test amendment 2, Max, 6 Oct): NOT MET. Original pre-registered ≤0.1, superseded but retained: NOT MET.** Neither the ≤2 nor ≤0.5 alternative passes.

Eligibility is annotation-only and fixed before testing. Missing people and truncation do not remove events. The largest-foreground-box continuity assignment is ambiguous in 342/914 events. Repeated selection reused 101 tuning falls; validation performance is optimistic. Prone-person detector failures, occlusion, clip censoring and frame-edge geometry artefacts limit recall. Sitting, riding and walking produce false alerts. The border veto is off at the dashboard tiers; border occurrence does not imply a border-veto miss.

Reused negative perception caches lack execution-linked historical runtime/package identity. Payload hashes and three short current-runtime checks match, but this does not recover provenance or establish identity over complete datasets. This gap was explicitly accepted before the locked run.

Scores are model confidence, not probabilities. One seed was evaluated; no calibration, appearance/video ablation or separate slow-collapse result exists. **GI FAIL:** no passing combined feed count was established, despite short source-time detection delays. No campus deployment or medical reliability is claimed.

Post-hoc suggestions are a prone-person detector, fixed-camera border filtering with recall costs, per-site calibration and cyclist/sitting hard negatives. None changed the frozen model. Full [results](../results.md), [limitations](../failure_analysis.md) and [data terms](../data.md) apply.

**Public-release verification scope:** CPU rule/feature parity and stored-notice evaluation were checked. No model inference, pixel-to-notice runtime equivalence or optional inference-environment installation was tested during curation. Frozen research results do not certify a new hardware/software environment.
