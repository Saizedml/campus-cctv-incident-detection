# How this was built

Max Blunden-Slusarski designed the approach from a literature review, chose the datasets, wrote the evaluation protocol and success criteria, reviewed the results and footage, and made every go/no-go decision. AI coding agents (OpenAI Codex) wrote most of the code under that gated process. This repository is a curated release; the full experiment history, experiment registry and 26 gate reports remain in a private research repository.

The workflow separated decisions from execution: define comparisons and stop rules, preserve source identities, inspect validation evidence, obtain approval, freeze, then execute the locked assessment once. Failures were retained rather than hidden. Human acceptance meant the research deliverable was accepted with its limitations; it did not turn an unmet numerical criterion into a pass.

| Gate or review record | One-line disposition |
|---|---|
| G0, initial | STOP for dataset terms; resumed after authorisation. |
| G0, resumed | PASS after required terms were accepted; an unavailable authenticated model used the declared fallback. |
| GW1, source integrity | E10 STOP on a changed source image. |
| GW1, source recovery | Human-approved source recovery applied; scoped continuation allowed. |
| GW1, crop route | FAIL; registered fallback followed. |
| GW1, fallback | FAIL; stopped for human decision. |
| GW1, corrected comparison | Still failed; further work needed explicit approval. |
| GW1-W, first selection | Validation candidate selected; no locked access. |
| GW2, first verifier comparison | Historical verifier comparison PASS. |
| GW3, first temporal comparison | Historical temporal comparison PASS. |
| GW1-W2, later selection | Validation candidate selected; final detector deviation was recorded separately. |
| GD1, playlist proposal | Awaited human review at that stage. |
| GD1, automated readiness | Checks passed; human run-through still pending then. |
| GD1, first approval | GO from Max; subsequent revised approval recorded separately. |
| W-DONE | GO with limitations; original NOT MET, revised MET under post-hoc revision on 6 October 2026. |
| GF1 | FALLBACK-PASS; geometry head selected over the alternative. |
| GF2 | FALLBACK-PASS; initial plain-down rule later amended. |
| GF-SN | FALLBACK-PASS with safety net off: no gain. |
| GF amendment | Revised down-or-peak proposal; superseded by the next amendment. |
| GF amendment 2 | Validation proposal subsequently frozen; criterion revised pre-test. |
| F2 prelocked | STOP for missing execution provenance; cache reuse later explicitly accepted. |
| F-DONE | GO with limitations; revised pre-test and original criteria both NOT MET. |
| GD1/GD2 revised run-through | PASS from Max for the revised dashboard. |
| GD1 final | PASS from Max; UI acceptance is separate from accuracy. |
| GD2 final | PASS from Max without requested changes. |
| GI, combined real-time test | FAIL; no passing combined feed count; partial reduced-feed attempt ended with a CUDA failure. |

The public release removes private orchestration and data-specific records, retains portable inference interfaces and event/evaluation logic, and uses synthetic fixtures for CPU tests. The equivalence check reads stored research notices locally without redistributing them. Dependency upgrades and later model changes require a fresh version and evaluation; they do not amend frozen research results.

See [decisions](decisions.md), [evaluation protocol](evaluation_protocol.md) and [limitations](failure_analysis.md).
