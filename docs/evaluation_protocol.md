# Evaluation protocol

The research used a gated workflow: register comparisons, select on validation, obtain human approval, freeze code/configuration/weights, and execute the locked test once. Reporting and review follow the freeze; they do not optimise test thresholds. The curated release preserves those algorithms and reports stored outcomes rather than generating a new benchmark.

## Data separation

Weapon evaluation holds out a camera from USRT Mock Attack. Actors, building and the knife appearance are shared across its camera split, so this tests camera transfer rather than entirely new people or objects. Only sequential movement frames were released. Timing is **nominal 2 fps sequence time** and breaks at gaps. Positive sequences do not supply negative camera-hours.

MEVA validation and test use separate sites. The held-out school site is unseen in threshold selection; hard-negative mining came from the bus site. Normal NWPU Campus footage is an independent negative test source. Its published training split is used as held-out negative exposure for this project, not as project training data. No test annotations are redistributed.

Falls use eligible staged and synthetic training data, subject/scene-separated event tuning, and OF-In-the-Wild for the locked assessment. Annotation-only eligibility is fixed before testing: sufficient fallen duration OR the required consecutive fall-labelled sampled timestamps. Low confidence, missing detections and truncated bodies never exclude events from eligibility.

## Matching and exposure

An alert can match at most one event in each evaluation. The frozen person/assigned-subject matching window is [onset−1 s, end+2 s]. Overlap uses intersection over the smaller box area (IoMin), not detection AP's IoU. Weapon subtype event sets can overlap and have distinct segmentations; their counts must not be added.

A qualifying continuation can be an UPDATE. UPDATEs can recover event recall, while only NEW counts towards false-alert rates. The fixed weapon cooldown is 60 seconds; falls use 120 seconds. False alerts per camera-hour are total unmatched negative-set NEW notices divided by the sum of camera exposures. This denominator is not elapsed wall-clock time when cameras run together.

Recall has a Wilson 95% interval. Rate certification uses the exact one-sided 95% Poisson upper bound, chi-square(0.95, 2n+2)/(2H), with n NEW notices and H camera-hours. Empirical success under the revised criterion is distinct from upper-bound certification. Short negative exposure cannot certify arbitrarily low false-alert budgets even when no alert appears.

## Criteria and chronology

**Weapons, Original pre-registered ≤0.1 criterion: NOT MET. Revised ≤5 criterion: MET, post-hoc revision on 6 October 2026, after weapons locked results were known.** A frozen rule needs at least half the weapon incidents at an actual MEVA-test rate within the limit. q0.1/q0.25/q0.5/q1 qualify for the revised limit; q2/q5 do not.

**Falls, revised primary ≤5 criterion (pre-test amendment 2, 6 October 2026): NOT MET. Original pre-registered ≤0.1, superseded but retained: NOT MET.** The revision was registered before the falls locked run, with the frozen eligible-event denominator. No frozen rule reaches at least half the eligible events while staying within the actual rate ceiling.

## Review and diagnostics

Model predictions, one-word assistant observations and human decisions are separate fields. Negative-set labels are incomplete. Only the declared census and samples were reviewed; all other views are outside sample. Human-confirmed weapons support a secondary rate table, while original rates remain headline. No reviewer decision enters training or the frozen ground truth.

Weapons review covers all 421 lower-q negative notices, a seed-0 sample of 300 unique tier views, 114 unmatched positive-set notices and 12 q2 misses. The random list was saved before inspection. This covers 570 unique views; 2,352 tier notices remain outside individual review. Falls review covers 828 lower-q notices, 150 upper-q views and 50 q2 misses, totalling 973 unique views. Keyframes do not establish full-video absence of an incident. Review Wilson intervals describe their sampling unit and do not account for camera clustering. Sampled views cannot be treated as a complete independent alert population; the additional outside-sample counts and diagnostic boundaries remain in [failure analysis](failure_analysis.md#additional-interpretation-boundaries).

A secondary localisation metric requires a score-generating detection to overlap the ground-truth object at IoMin ≥0.3. This does not replace person-level primary matching. Frame AP and macro-F1 are also secondary.

## Latency

Source-time detection delay is distinct from paced delivery latency. The combined validation test included queueing, repeated onsets, resource telemetry, schema checks and preservation probes. Fallbacks were ordered: batch across feeds, separate the verifier, then reduce feeds. **Combined real-time test: not passed.** No number of simultaneous feeds was shown to meet the alert-delay limit. The frozen notices were preserved, but falls delivery was too slow and the partial two-feed run failed. See [results](results.md).
