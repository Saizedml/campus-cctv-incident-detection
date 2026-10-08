# Weapon detector and cascade model card

**Intended use:** research CCTV evidence triage with human confirmation. The FT-HNF detector is RF-DETR-L with person/hand crops, hard-negative mining and restored firearm training examples. YOLO26 pose and BoT-SORT provide the shared front end. A frozen Qwen3-VL verifier conditionally checks candidates. No weights are distributed.

**Output:** generic weapon notices with optional subtype model guesses, source time and track evidence. Scores are model confidence, not probabilities. Subtype guesses are unreliable and must not replace object review.

**Locked headline:** 36/48 incidents at both q2 and q5, 75.00% recall (Wilson 95% 61.22–85.08%). MEVA-test FA/h is 12.7556/27.5428; NWPU is 16.3861/40.0087. **Original pre-registered ≤0.1 criterion: NOT MET. Revised ≤5 criterion: MET, post-hoc revision (Max, 6 Oct), after weapons locked results were known.** q0.1/q0.25/q0.5/q1 meet the revised empirical criterion; the dashboard tiers do not.

**Limits:** shared actors/scenes and nominal timing; one seed; close-up training-domain mismatch; uncalibrated scores; hand-held look-alikes; person-level matching; incomplete negative annotations; sampled visual review; imperfect object localisation; large site-transfer false-alert gap. At q2, 610 of 643 MEVA bypassed NEW alerts have saved `not_weapon` answers. This is post-hoc evidence, not a counterfactual rerun. Secondary human-adjusted rates do not replace originals.

**Capacity:** GI FAIL; no passing combined feed count established. Dashboard playback and source-time delay are not paced inference claims.

**Future versions only:** evaluate V on every alert, per-site burn-in calibration, broader look-alike training, crop padding and score calibration. None changed the frozen model. Full [results](../results.md), [verifier card](verifier.md), [limitations](../failure_analysis.md) and [data terms](../data.md) apply.

**Public-release verification scope:** CPU rule/feature parity and stored-notice evaluation were checked. No model inference, pixel-to-notice runtime equivalence or optional inference-environment installation was tested during curation. Frozen research results do not certify a new hardware/software environment.
