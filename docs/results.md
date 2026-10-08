# Results

This is the public aggregate view of the final research results. The original rates remain headline; human-adjusted weapon rates are secondary. No test event, camera identifier, annotation or image is included. q is a validation false-alert budget label, not a promised rate on new footage. NEW alerts alone count towards false alerts per camera-hour; UPDATEs may credit recall.

**Weapons: Original pre-registered ≤0.1 criterion: NOT MET. Revised ≤5 criterion: MET, post-hoc revision on 6 October 2026, after weapons locked results were known.** The qualifying frozen rules are q0.1/q0.25/q0.5/q1; neither dashboard tier qualifies.

**Falls: revised primary ≤5 criterion (pre-test amendment 2, 6 October 2026): NOT MET; original pre-registered ≤0.1, superseded but retained: NOT MET.** The ≤2 and ≤0.5 alternatives also fail. Human acceptance of the research deliverable does not change these outcomes.

**Combined real-time test (gate GI): not passed.** No number of simultaneous feeds was shown to meet the alert-delay limit. Scores are model confidence, not probabilities.

## Locked headlines

| Task / locked positives | q | Detected / recall (Wilson 95%) | MEVA-test FA/h | NWPU FA/h |
|---|---|---|---:|---:|
| WEAPON / Held-out camera | 2 | 36/48 · 75.00% (61.22–85.08%) | 12.7556 | 16.3861 |
| WEAPON / Held-out camera | 5 | 36/48 · 75.00% (61.22–85.08%) | 27.5428 | 40.0087 |
| Falls / OF-In-the-Wild | 2 | 321/914 · 35.12% (32.09–38.27%) | 9.4252 | 32.0236 |
| Falls / OF-In-the-Wild | 5 | 556/914 · 60.83% (57.63–63.94%) | 34.8865 | 67.7071 |

## Weapons: original and revised criteria

| Actual MEVA-test limit NEW/h | Result | Qualifying frozen q rules |
|---|---|---|
| ≤5 | MET | 0.1, 0.25, 0.5, 1 |
| ≤2 | MET | 0.1, 0.25, 0.5 |
| ≤0.5 | MET | 0.1 |
| ≤0.1 (original) | NOT MET | none |

| Frozen q | Held-out camera detected / recall | Wilson 95% | Original MEVA-test FA/h | Original NWPU FA/h |
|---|---|---|---|---|
| 0.1 | 24/48 / 50.00% | 36.39–63.61% | 0.466263 | 0.332713 |
| 0.25 | 28/48 / 58.33% | 44.28–71.15% | 0.732699 | 0.665426 |
| 0.5 | 29/48 / 60.42% | 46.31–72.98% | 1.398789 | 1.580386 |
| 1.0 | 33/48 / 68.75% | 54.67–80.05% | 3.097319 | 3.992555 |

## Weapons: validation-to-test false-alert transfer

| q | Validation FA/h | MEVA-test FA/h | Test / val | NWPU FA/h | NWPU / val |
|---|---|---|---|---|---|
| 0.1 | 0.0833 | 0.4663 | 5.60× | 0.3327 | 3.99× |
| 0.25 | 0.1666 | 0.7327 | 4.40× | 0.6654 | 3.99× |
| 0.5 | 0.3831 | 1.3988 | 3.65× | 1.5804 | 4.12× |
| 1.0 | 0.7829 | 3.0973 | 3.96× | 3.9926 | 5.10× |
| 2.0 | 1.8990 | 12.7556 | 6.72× | 16.3861 | 8.63× |
| 5.0 | 4.5977 | 27.5428 | 5.99× | 40.0087 | 8.70× |

## Validation recall used in the figure

The two plotted series are **validation (tuning footage)** and **locked test (unseen site)**. The unseen site refers to the MEVA negative footage used to measure false alerts. Positive recall is measured on a held-out weapon camera or the independent falls collection, not on those MEVA clips. The frozen validation points below come only from the registered gate reports. They describe tuning footage and can be optimistic, particularly after repeated falls rule selection. Lines connect the six selected rules; they do not imply that the falls rules are nested thresholds or that intermediate points were measured.

Each value has its source report beside it. Exact hit counts and denominators are retained; figure percentages are calculated from these fractions. Validation false-alert rates remain those in the transfer tables above and below.

| Frozen q | Weapons validation detected / total | Falls validation detected / total |
|---|---|---|
| 0.1 | 28/64 ([V gate report](#weapons-validation-source), q=0.1) | 26/101 ([GF amendment 2 report](#falls-validation-source), q=0.1) |
| 0.25 | 30/64 ([V gate report](#weapons-validation-source), q=0.25) | 42/101 ([GF amendment 2 report](#falls-validation-source), q=0.25) |
| 0.5 | 34/64 ([V gate report](#weapons-validation-source), q=0.5) | 53/101 ([GF amendment 2 report](#falls-validation-source), q=0.5) |
| 1 | 37/64 ([V gate report](#weapons-validation-source), q=1) | 60/101 ([GF amendment 2 report](#falls-validation-source), q=1) |
| 2 | 40/64 ([V gate report](#weapons-validation-source), q=2) | 71/101 ([GF amendment 2 report](#falls-validation-source), q=2) |
| 5 | 43/64 ([V gate report](#weapons-validation-source), q=5) | 88/101 ([GF amendment 2 report](#falls-validation-source), q=5) |

### Weapons validation source

Source report: `V_FTHNF_retuned_1610_20261004.md`, “FT-HNF V: 4 October 16:10 correction”, selected retuned six-point table, rows q=0.1 through q=5, EXP-158. The report records the verifier KEEP decision before freezing. The experiment registry's EXP-161 row records that the locked pass used those unchanged six retuned rules. `GD1_2026-10-05_playlist.md` independently reproduces the validation counts at the two dashboard tiers. This citation contains aggregate provenance only.

### Falls validation source

Source report: `GF_amend2_20261006.md`, “Falls GF amendment 2: 6 October 2026”, “Selected six points”, rows q=0.1 through q=5, EXP-197. It is the detailed report cited by `GF-amend2_2026-10-06.md`. The experiment registry confirms the amendment's selected family, the two dashboard-tier counts and the enabled lowest-budget rule. All validation rows use the report's full event denominator; no validation event was dropped for missing detections.

## Frozen weapon rules

| q | tau_a | tau_hi / bypass | Tier |
|---|---|---|---|
| 0.1 | 0.8308733105659485 | 1.000001 |  |
| 0.25 | 0.7476891279220581 | 1.000001 |  |
| 0.5 | 0.5453240275382996 | 1.000001 |  |
| 1.0 | 0.20413830876350403 | 1.000001 |  |
| 2.0 | 0.20413830876350403 | 0.6111111111111112 | **ALERT NOW** |
| 5.0 | 0.20413830876350403 | 0.2222222222222222 | **CHECK WHEN FREE** |

All rules use best-score pooling, k=1 and W=2 seconds. The verifier vetoes explicit `not_weapon` answers only below the high-score bypass threshold. Same-track continuation uses the fixed 60-second cooldown. These rules remain frozen.

## Weapons: primary event recall and source-time delay

The same class-agnostic WEAPON notices are evaluated against each category. Knife and firearm intervals overlap and have different segmentation; their denominators must not be added. One notice matches at most one event within an evaluation. Timing is **nominal 2 fps sequence time**, not paced incident-to-delivery latency.

| GT category | q | Detected / total | Recall | Wilson 95% | <=10s | Late | Duplicates | Delay median / p95 s |
|---|---|---|---|---|---|---|---|---|
| weapon | 0.1 | 24/48 | 0.5000 | 0.3639–0.6361 | 23 | 1 | 252 | 2.2500 / 7.8500 |
| weapon | 0.25 | 28/48 | 0.5833 | 0.4428–0.7115 | 28 | 0 | 398 | 2.0000 / 6.6500 |
| weapon | 0.5 | 29/48 | 0.6042 | 0.4631–0.7298 | 29 | 0 | 535 | 2.0000 / 4.8000 |
| weapon | 1.0 | 33/48 | 0.6875 | 0.5467–0.8005 | 33 | 0 | 744 | 1.0000 / 4.5000 |
| weapon | **2.0** | 36/48 | 0.7500 | 0.6122–0.8508 | 36 | 0 | 854 | 1.0000 / 4.5000 |
| weapon | **5.0** | 36/48 | 0.7500 | 0.6122–0.8508 | 36 | 0 | 946 | 1.0000 / 4.5000 |
| knife | 0.1 | 9/23 | 0.3913 | 0.2216–0.5921 | 8 | 1 | 68 | 1.5000 / 11.8000 |
| knife | 0.25 | 13/23 | 0.5652 | 0.3681–0.7437 | 12 | 1 | 103 | 1.0000 / 10.7000 |
| knife | 0.5 | 16/23 | 0.6957 | 0.4913–0.8440 | 15 | 1 | 120 | 0.5000 / 7.2500 |
| knife | 1.0 | 18/23 | 0.7826 | 0.5810–0.9034 | 17 | 1 | 150 | 0.2500 / 5.0750 |
| knife | **2.0** | 18/23 | 0.7826 | 0.5810–0.9034 | 17 | 1 | 164 | 0.2500 / 5.0750 |
| knife | **5.0** | 18/23 | 0.7826 | 0.5810–0.9034 | 17 | 1 | 186 | 0.0000 / 5.0750 |
| firearm | 0.1 | 25/49 | 0.5102 | 0.3747–0.6442 | 24 | 1 | 249 | 2.0000 / 7.8000 |
| firearm | 0.25 | 29/49 | 0.5918 | 0.4525–0.7178 | 29 | 0 | 395 | 2.0000 / 6.6000 |
| firearm | 0.5 | 30/49 | 0.6122 | 0.4725–0.7357 | 30 | 0 | 532 | 1.7500 / 4.7750 |
| firearm | 1.0 | 34/49 | 0.6939 | 0.5547–0.8048 | 34 | 0 | 741 | 1.0000 / 4.5000 |
| firearm | **2.0** | 37/49 | 0.7551 | 0.6191–0.8540 | 37 | 0 | 851 | 1.0000 / 4.5000 |
| firearm | **5.0** | 37/49 | 0.7551 | 0.6191–0.8540 | 37 | 0 | 939 | 1.0000 / 4.5000 |

## Weapons: class-filtered secondary results

These independent subtype replays are secondary, not the alert headline.

| GT category | q | Detected / total | Recall | Wilson 95% | <=10s | Late | Duplicates | Delay median / p95 s |
|---|---|---|---|---|---|---|---|---|
| weapon | 0.1 | 24/48 | 0.5000 | 0.3639–0.6361 | 23 | 1 | 252 | 2.2500 / 7.8500 |
| weapon | 0.25 | 28/48 | 0.5833 | 0.4428–0.7115 | 28 | 0 | 398 | 2.0000 / 6.6500 |
| weapon | 0.5 | 29/48 | 0.6042 | 0.4631–0.7298 | 29 | 0 | 535 | 2.0000 / 4.8000 |
| weapon | 1.0 | 33/48 | 0.6875 | 0.5467–0.8005 | 33 | 0 | 744 | 1.0000 / 4.5000 |
| weapon | **2.0** | 36/48 | 0.7500 | 0.6122–0.8508 | 36 | 0 | 854 | 1.0000 / 4.5000 |
| weapon | **5.0** | 36/48 | 0.7500 | 0.6122–0.8508 | 36 | 0 | 946 | 1.0000 / 4.5000 |
| knife | 0.1 | 9/23 | 0.3913 | 0.2216–0.5921 | 8 | 1 | 68 | 1.5000 / 11.8000 |
| knife | 0.25 | 12/23 | 0.5217 | 0.3296–0.7076 | 11 | 1 | 95 | 1.0000 / 10.9750 |
| knife | 0.5 | 14/23 | 0.6087 | 0.4079–0.7784 | 13 | 1 | 109 | 0.7500 / 10.4250 |
| knife | 1.0 | 16/23 | 0.6957 | 0.4913–0.8440 | 15 | 1 | 132 | 0.5000 / 6.1250 |
| knife | **2.0** | 16/23 | 0.6957 | 0.4913–0.8440 | 15 | 1 | 142 | 0.5000 / 6.1250 |
| knife | **5.0** | 17/23 | 0.7391 | 0.5353–0.8745 | 16 | 1 | 155 | 0.5000 / 5.6000 |
| firearm | 0.1 | 18/49 | 0.3673 | 0.2467–0.5073 | 13 | 5 | 101 | 4.2500 / 32.4500 |
| firearm | 0.25 | 20/49 | 0.4082 | 0.2822–0.5475 | 15 | 5 | 171 | 4.2500 / 29.3000 |
| firearm | 0.5 | 21/49 | 0.4286 | 0.3002–0.5673 | 17 | 4 | 255 | 4.0000 / 17.0000 |
| firearm | 1.0 | 29/49 | 0.5918 | 0.4525–0.7178 | 25 | 4 | 390 | 3.5000 / 13.2000 |
| firearm | **2.0** | 29/49 | 0.5918 | 0.4525–0.7178 | 25 | 4 | 408 | 3.5000 / 13.2000 |
| firearm | **5.0** | 29/49 | 0.5918 | 0.4525–0.7178 | 25 | 4 | 436 | 3.5000 / 13.0000 |

## Weapons: negative exposure and exact one-sided bounds

No point is certified at its q budget on either test set by the exact one-sided 95% Poisson bound.

| Dataset | Category | q | NEW FA | Hours | FA/h | Exact upper95 |
|---|---|---|---|---|---|---|
| MEVA-test | weapon | 0.1 | 28 | 60.0519 | 0.4663 | 0.6393 |
| MEVA-test | weapon | 0.25 | 44 | 60.0519 | 0.7327 | 0.9421 |
| MEVA-test | weapon | 0.5 | 84 | 60.0519 | 1.3988 | 1.6771 |
| MEVA-test | weapon | 1.0 | 186 | 60.0519 | 3.0973 | 3.4978 |
| MEVA-test | weapon | **2.0** | 766 | 60.0519 | 12.7556 | 13.5402 |
| MEVA-test | weapon | **5.0** | 1654 | 60.0519 | 27.5428 | 28.6832 |
| MEVA-test | knife | 0.1 | 22 | 60.0519 | 0.3663 | 0.5231 |
| MEVA-test | knife | 0.25 | 35 | 60.0519 | 0.5828 | 0.7727 |
| MEVA-test | knife | 0.5 | 61 | 60.0519 | 1.0158 | 1.2572 |
| MEVA-test | knife | 1.0 | 116 | 60.0519 | 1.9317 | 2.2537 |
| MEVA-test | knife | **2.0** | 537 | 60.0519 | 8.9423 | 9.6036 |
| MEVA-test | knife | **5.0** | 1098 | 60.0519 | 18.2842 | 19.2182 |
| MEVA-test | firearm | 0.1 | 6 | 60.0519 | 0.0999 | 0.1972 |
| MEVA-test | firearm | 0.25 | 9 | 60.0519 | 0.1499 | 0.2615 |
| MEVA-test | firearm | 0.5 | 23 | 60.0519 | 0.3830 | 0.5426 |
| MEVA-test | firearm | 1.0 | 82 | 60.0519 | 1.3655 | 1.6408 |
| MEVA-test | firearm | **2.0** | 252 | 60.0519 | 4.1964 | 4.6580 |
| MEVA-test | firearm | **5.0** | 672 | 60.0519 | 11.1903 | 11.9269 |
| NWPU-normal | weapon | 0.1 | 4 | 12.0224 | 0.3327 | 0.7614 |
| NWPU-normal | weapon | 0.25 | 8 | 12.0224 | 0.6654 | 1.2006 |
| NWPU-normal | weapon | 0.5 | 19 | 12.0224 | 1.5804 | 2.3189 |
| NWPU-normal | weapon | 1.0 | 48 | 12.0224 | 3.9926 | 5.0784 |
| NWPU-normal | weapon | **2.0** | 197 | 12.0224 | 16.3861 | 18.4406 |
| NWPU-normal | weapon | **5.0** | 481 | 12.0224 | 40.0087 | 43.1422 |
| NWPU-normal | knife | 0.1 | 3 | 12.0224 | 0.2495 | 0.6449 |
| NWPU-normal | knife | 0.25 | 5 | 12.0224 | 0.4159 | 0.8745 |
| NWPU-normal | knife | 0.5 | 9 | 12.0224 | 0.7486 | 1.3063 |
| NWPU-normal | knife | 1.0 | 18 | 12.0224 | 1.4972 | 2.2202 |
| NWPU-normal | knife | **2.0** | 123 | 12.0224 | 10.2309 | 11.8834 |
| NWPU-normal | knife | **5.0** | 297 | 12.0224 | 24.7039 | 27.1953 |
| NWPU-normal | firearm | 0.1 | 1 | 12.0224 | 0.0832 | 0.3946 |
| NWPU-normal | firearm | 0.25 | 3 | 12.0224 | 0.2495 | 0.6449 |
| NWPU-normal | firearm | 0.5 | 11 | 12.0224 | 0.9150 | 1.5145 |
| NWPU-normal | firearm | 1.0 | 32 | 12.0224 | 2.6617 | 3.5752 |
| NWPU-normal | firearm | **2.0** | 78 | 12.0224 | 6.4879 | 7.8325 |
| NWPU-normal | firearm | **5.0** | 210 | 12.0224 | 17.4674 | 19.5841 |

## Weapons: frame-level diagnostics

COCO-style bounding-box IoU metrics are distinct from event-level IoMin matching.

| Held-out camera category | AP50 | mAP50–95 |
|---|---|---|
| weapon | 0.1687 | 0.0581 |
| knife | 0.0842 | 0.0334 |
| firearm | 0.1590 | 0.0531 |

## Original Dangerous Items grouped test

These are the original full-frame models, distinct from the frozen weapon cascade. No reference event-level rerun was made.

| Model | Images | View | AP50 | mAP50–95 |
|---|---|---|---|---|
| yolo11m | 1222 | original five classes | 0.8293 | 0.5647 |
| yolo11m | 1222 | pooled superclasses (secondary) | 0.8549 | 0.5930 |
| yolo26m | 1222 | original five classes | 0.8800 | 0.6211 |
| yolo26m | 1222 | pooled superclasses (secondary) | 0.8949 | 0.6368 |

## Weapons: unmatched notices

These positive-set notices supply no negative camera-hours.

| q | Unmatched NEW | Unmatched NEW+UPDATE |
|---|---|---|
| 0.1 | 2 | 5 |
| 0.25 | 2 | 5 |
| 0.5 | 3 | 8 |
| 1.0 | 4 | 13 |
| 2.0 | 10 | 46 |
| 5.0 | 14 | 68 |

## Weapons: secondary box-localised recall

At least one score-generating alert detection overlaps the ground-truth box at IoMin ≥0.3 within the matching window. This descriptive coverage check does not replace the exclusive primary matching rule.

| q | Box-localised / 48 | Recall | Wilson 95% |
|---|---|---|---|
| 0.1 | 21/48 | 43.75% | 30.70–57.72% |
| 0.25 | 27/48 | 56.25% | 42.28–69.30% |
| 0.5 | 27/48 | 56.25% | 42.28–69.30% |
| 1.0 | 31/48 | 64.58% | 50.44–76.57% |
| 2.0 | 33/48 | 68.75% | 54.67–80.05% |
| 5.0 | 33/48 | 68.75% | 54.67–80.05% |

## Weapons: secondary rates after human review

Human-confirmed weapon views in nominally negative footage exclude two notices per rule in this secondary table. No uncertainty or outside-sample view was excluded. Original rates remain headline; no label or threshold changed.

| q | Original NEW | Excluded | Secondary NEW | Original FA/h | Secondary FA/h |
|---|---|---|---|---|---|
| 0.1 | 28 | 2 | 26 | 0.466263 | 0.432959 |
| 0.25 | 44 | 2 | 42 | 0.732699 | 0.699395 |
| 0.5 | 84 | 2 | 82 | 1.398789 | 1.365485 |
| 1.0 | 186 | 2 | 184 | 3.097319 | 3.064015 |
| 2.0 | 766 | 2 | 764 | 12.755628 | 12.722323 |
| 5.0 | 1654 | 2 | 1652 | 27.542830 | 27.509526 |

## Falls: event recall and source-time delay

Eligibility uses annotation duration only: fallen duration at least the frozen persistence time OR the required consecutive analysed fall timestamps. Missing subjects, borders and low confidence never remove events. All-event denominators are retained alongside eligible rows. Delays are source time, not paced latency.

| q | Denominator | Detected / events | Recall | Wilson95 | <=10s | Late | Duplicates | Delay median/p95 s |
|---|---|---|---|---|---|---|---|---|
| 0.1 | eligible | 140/912 | 0.1535 | 0.1316–0.1784 | 139 | 1 | 391 | 1.2716/4.1559 |
| 0.1 | all_events | 140/914 | 0.1532 | 0.1313–0.1780 | 139 | 1 | 391 | 1.2716/4.1559 |
| 0.25 | eligible | 103/912 | 0.1129 | 0.0940–0.1351 | 103 | 0 | 353 | 1.1202/4.5022 |
| 0.25 | all_events | 103/914 | 0.1127 | 0.0938–0.1348 | 103 | 0 | 353 | 1.1202/4.5022 |
| 0.5 | eligible | 262/914 | 0.2867 | 0.2583–0.3168 | 261 | 1 | 1043 | 0.9174/4.2189 |
| 0.5 | all_events | 262/914 | 0.2867 | 0.2583–0.3168 | 261 | 1 | 1043 | 0.9174/4.2189 |
| 1.0 | eligible | 358/914 | 0.3917 | 0.3606–0.4237 | 357 | 1 | 1458 | 0.8673/4.2226 |
| 1.0 | all_events | 358/914 | 0.3917 | 0.3606–0.4237 | 357 | 1 | 1458 | 0.8673/4.2226 |
| 2.0 | eligible | 321/914 | 0.3512 | 0.3209–0.3827 | 320 | 1 | 1300 | 0.8073/3.8777 |
| 2.0 | all_events | 321/914 | 0.3512 | 0.3209–0.3827 | 320 | 1 | 1300 | 0.8073/3.8777 |
| 5.0 | eligible | 556/914 | 0.6083 | 0.5763–0.6394 | 555 | 1 | 3032 | 0.5702/3.4911 |
| 5.0 | all_events | 556/914 | 0.6083 | 0.5763–0.6394 | 555 | 1 | 3032 | 0.5702/3.4911 |

## Falls: negative rates and exact one-sided bounds

| Dataset | q | NEW | Hours | FA/h | Upper95 | Certified at q | Could certify with zero |
|---|---|---|---|---|---|---|---|
| MEVA-test | 0.1 | 43 | 60.0519 | 0.7160 | 0.9234 | False | True |
| MEVA-test | 0.25 | 78 | 60.0519 | 1.2989 | 1.5681 | False | True |
| MEVA-test | 0.5 | 363 | 60.0519 | 6.0448 | 6.5933 | False | True |
| MEVA-test | 1.0 | 720 | 60.0519 | 11.9896 | 12.7511 | False | True |
| MEVA-test | 2.0 | 566 | 60.0519 | 9.4252 | 10.1034 | False | True |
| MEVA-test | 5.0 | 2095 | 60.0519 | 34.8865 | 36.1665 | False | True |
| NWPU | 0.1 | 74 | 12.0224 | 6.1552 | 7.4686 | False | False |
| NWPU | 0.25 | 55 | 12.0224 | 4.5748 | 5.7269 | False | True |
| NWPU | 0.5 | 215 | 12.0224 | 17.8833 | 20.0234 | False | True |
| NWPU | 1.0 | 316 | 12.0224 | 26.2843 | 28.8498 | False | True |
| NWPU | 2.0 | 385 | 12.0224 | 32.0236 | 34.8413 | False | True |
| NWPU | 5.0 | 814 | 12.0224 | 67.7071 | 71.7428 | False | True |

## Falls: success checks

| Actual MEVA budget | >=half eligible events | Frozen rules meeting both |
|---|---|---|
| 5 | False | none |
| 2 | False | none |
| 0.5 | False | none |
| 0.1 | False | none |

| Actual MEVA-test ceiling | Frozen rules within FA ceiling | Result and reason |
|---|---|---|
| **≤5, revised primary (pre-test)** | q0.1: 140/912, 15.35% (13.16–17.84%), 0.7160/h; q0.25: 103/912, 11.29% (9.40–13.51%), 1.2989/h | **NOT MET**: both below half of eligible events |
| ≤2, secondary | Same q0.1/q0.25 rules | **NOT MET** |
| ≤0.5, secondary | None | **NOT MET** |
| ≤0.1, original pre-registered, superseded | None | **NOT MET** |

## Falls: validation-to-test transfer

B denotes the frozen border veto. The six rules are not a nested threshold curve.

| q | B | Val NEW | Val/h | MEVA NEW | MEVA/h | MEVA/val | NWPU NEW | NWPU/h | NWPU/val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | on | 6 | 0.0999 | 43 | 0.7160 | 7.16× | 74 | 6.1552 | 61.58× |
| 0.25 | off | 15 | 0.2499 | 78 | 1.2989 | 5.20× | 55 | 4.5748 | 18.31× |
| 0.5 | on | 25 | 0.4165 | 363 | 6.0448 | 14.51× | 215 | 17.8833 | 42.94× |
| 1.0 | on | 59 | 0.9828 | 720 | 11.9896 | 12.20× | 316 | 26.2843 | 26.74× |
| 2.0 | off | 105 | 1.7491 | 566 | 9.4252 | 5.39× | 385 | 32.0236 | 18.31× |
| 5.0 | off | 294 | 4.8975 | 2095 | 34.8865 | 7.12× | 814 | 67.7071 | 13.82× |

## Falls: tracking and misses

Post-fall absence does not always indicate detector failure: short clips can censor the observation window. Ambiguous subject assignments remain unchanged.

| Miss measure | q2 | q5 |
|---|---:|---:|
| Total missed events |593|358|
| Not tracked after fall in +1 to +5 s |130|109|
| Tracked after fall but not credited/flagged |463|249|
| Of not-tracked: clip ends before +1 s |21|20|
| All misses whose +5 s window is clip-end censored |295|184|
| Saved stage: probability/persistence rule |578|342|
| Saved stage: no assigned tracked subject |14|14|
| Saved stage: event assignment |1|2|
| Border veto caused miss |0|0|
| Miss with some border-truncated observed box in matching window (overlapping diagnostic) |319|188|

## Falls: assistant observations

A is the 828-notice lower-q census; B is the 150-view upper-q sample, with fixed 100/50 dataset allocation; C is a sample of 50 missed falls. Categories describe visible evidence, not relabelled ground truth. A repeats some views across rules. B describes sample composition, not a population-weighted estimate. Wilson intervals do not account for camera clustering.

| Selection | One-word observation | Count | Share | Wilson 95% |
| --- | --- | --- | --- | --- |
| A | bending | 25/828 | 3.0% | 2.1%–4.4% |
| A | falling | 0/828 | 0.0% | 0.0%–0.5% |
| A | occluded | 5/828 | 0.6% | 0.3%–1.4% |
| A | riding | 267/828 | 32.2% | 29.2%–35.5% |
| A | rising | 5/828 | 0.6% | 0.3%–1.4% |
| A | sitting | 275/828 | 33.2% | 30.1%–36.5% |
| A | squatting | 2/828 | 0.2% | 0.1%–0.9% |
| A | standing | 24/828 | 2.9% | 2.0%–4.3% |
| A | unclear | 27/828 | 3.3% | 2.3%–4.7% |
| A | vehicle | 18/828 | 2.2% | 1.4%–3.4% |
| A | walking | 180/828 | 21.7% | 19.1%–24.7% |
| B | bending | 4/150 | 2.7% | 1.0%–6.7% |
| B | falling | 0/150 | 0.0% | 0.0%–2.5% |
| B | reclining | 1/150 | 0.7% | 0.1%–3.7% |
| B | riding | 25/150 | 16.7% | 11.6%–23.4% |
| B | sitting | 37/150 | 24.7% | 18.5%–32.1% |
| B | standing | 2/150 | 1.3% | 0.4%–4.7% |
| B | unclear | 4/150 | 2.7% | 1.0%–6.7% |
| B | vehicle | 1/150 | 0.7% | 0.1%–3.7% |
| B | walking | 76/150 | 50.7% | 42.7%–58.6% |
| C | bending | 2/50 | 4.0% | 1.1%–13.5% |
| C | falling | 37/50 | 74.0% | 60.4%–84.1% |
| C | occluded | 6/50 | 12.0% | 5.6%–23.8% |
| C | standing | 4/50 | 8.0% | 3.2%–18.8% |
| C | unclear | 1/50 | 2.0% | 0.4%–10.5% |

## Combined real-time test (gate GI)

| Configuration | Knife p95 q2 / q5 (s) | Firearm p95 q2 / q5 (s) | Falls p95 q2 / q5 (s) | Hour result |
|---|---:|---:|---:|---|
| serial4 | 2235.633 / 2235.633 | 2244.624 / 2242.948 | 2237.161 / 2237.059 | Latency FAIL |
| batch4 | 2.040 / 2.041 | 3.832 / 3.824 | 2335.741 / 2335.640 | Latency FAIL |
| V_separate4 | 2.040 / 2.041 | 3.863 / 3.858 | 2442.224 / 2442.119 | Latency FAIL |
| V_separate3 | 1.825 / 1.825 | 3.779 / 3.774 | 1441.434 / 1441.249 | Latency FAIL |

Batching kept detected weapon-alert p95 below four seconds, but falls still exceeded ten seconds with three feeds, so the combined system did not pass its real-time gate. The two-feed fallback then stopped on a GPU3 CUDA error; frozen outputs were preserved, but no passing combined feed count was established.

Each completed schedule lasted 3,600 seconds. Delay includes queueing and is conditional on a match. Repeated mixed-rate validation loops are not independent accuracy samples or a four-native-10-Hz-camera certification. Across completed configurations, knife matches were 129/129 at both tiers; firearm 515/643 at q2 and 643/643 at q5; falls 97/290 at both tiers. One feed was not attempted.

Preservation comparisons were exact (240/240). All four completed hours had 1,352/1,352 schema-valid packages each, zero recorded crashes and no flagged memory growth. The partial two-feed run stopped after 1,052.848 seconds, with 395 valid immediate JSONs, 393 complete packages and two unfinished packages; this does not certify an hour of stability. The later device-handle error and the earlier CUDA failure have no established underlying cause.

## Provenance and reporting boundaries

The reused negative perception caches lack execution-linked historical runtime/package provenance. All 1,053 payload hashes matched receipts and code/configuration comparisons agreed. Three perception-only 60-second prefix checks matched exactly: box IoU 1.0, zero unmatched detections, zero keypoint differences and identical track IDs. This narrow check does not establish whole-dataset identity or recover historical provenance. Reuse was explicitly accepted before the falls locked run.

The [aggregate JSON](../results/aggregate.json) drives the [figures](../scripts/make_figures.py). Six-q validation FA rates are reported for both tasks. Following the 8 October release authorisation, all six validation recall points are taken from the [frozen validation gate reports cited beside each value](#validation-recall-used-in-the-figure). Locked results and false-alert rates remain unchanged. The source-time median/p95 plot must be read with the combined real-time test result above.

All limitations and post-hoc recommendations remain in [failure analysis](failure_analysis.md). See the [evaluation protocol](evaluation_protocol.md) for denominators, exposure and confidence intervals.

**Public-release verification scope:** CPU rule/feature parity and stored-notice evaluation were checked. No model inference, pixel-to-notice runtime equivalence or optional inference-environment installation was tested during curation. Frozen research results do not certify a new hardware/software environment.
