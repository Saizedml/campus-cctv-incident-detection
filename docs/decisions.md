# Curated decision log

This records decisions that explain the final research system. It is a public summary, not the full private experiment history. No frozen result changed during curation.

| Decision | Rationale and outcome |
|---|---|
| Share perception across tasks | Reuse person tracks, pose and evidence infrastructure; capacity still needs separate measurement. |
| Use a crop detector and conditional VLM verifier | Preserve small-object evidence while limiting verifier cost; high-score bypass later dominated weapon test false alerts. |
| Select FT-HNF with declared deviation | The final detector retained restored firearm data and hard-negative mining. The deviation from the earlier near-tie selection rule was explicitly approved rather than concealed. |
| Keep two operational tiers | Alert now is q2; Check when free is q5. Their labels are validation budgets, not promised test rates. |
| Use generic weapon alerts | Knife/firearm class guesses were unreliable; subtype metrics remain reported separately. |
| Freeze before locked access | Code, weights, rules and provenance checks were fixed; each locked set had one claim and completion. |
| Revise weapons criterion after results | **Original pre-registered ≤0.1: NOT MET. Revised ≤5: MET, post-hoc revision on 6 October 2026**. The decision followed known weapon results and cannot be presented as pre-registered success. |
| Amend falls before testing | **Revised primary ≤5: NOT MET, pre-test amendment 2 on 6 October 2026**. The original ≤0.1 criterion is superseded but retained as NOT MET. Eligibility remained annotation-only. |
| Accept a perception provenance gap | Matching payload hashes and narrow exact prefix checks supported reuse under the deadline, but historical execution-linked runtime/package identity remains missing. |
| Keep model, assistant and human fields separate | Review observations do not become training labels or silently change the locked results. |
| Accept deliverables with limitations | W-DONE GO and F-DONE GO record Max's acceptance, not passes of every criterion. |
| Preserve the combined real-time test failure (gate GI) | Batching, separate verification and reduced feed count did not establish a passing combined configuration; no behavioural change was made to obtain a pass. |
| Defer violence and recency work | Complete weapons/falls evaluation and reporting; planned work remains explicitly unmeasured. |
| Publish a curated release | Portable code, synthetic media and permitted aggregates are public. The full research record remains private. |

Post-hoc recommendations in [failure analysis](failure_analysis.md) were not applied to either frozen model.
