# Changelog

## v1.0.1: Presentation update

Wording, figures and dashboard captures only. No code behaviour, frozen rule, result or test outcome changed.

- README: shorter results summary, plain-language explanation of the q2/q5 tiers and the MEVA/NWPU false-alert footage, the qualifying q1 weapons setting stated beside the revised criterion, one architecture diagram instead of two, and less internal shorthand.
- Figures, dashboard and docs: "Combined real-time test: not passed" replaces the internal gate code "GI FAIL"; displayed values are rounded; revision dates are stated without personal shorthand.
- Release notes moved from `RELEASE_NOTES_v1.0.0.md` into this changelog.

## v1.0.0: Curated research release

First public release of a research prototype built during a research internship at the Cisco–La Trobe Centre for AI and IoT: detection and evaluation logic, fixed operating-point configuration, an offline synthetic review dashboard, CPU tests, aggregate figures and documentation.

- Weapons: 75% of incidents detected (36/48) at both alert tiers.
- Falls: 35% (321/914) at the urgent tier and 61% (556/914) at the deferred tier.
- Original success criteria: not met for either task. The revised weapons criterion (≤5 false alerts per camera-hour) was met, but was revised after the results were known. The revised falls criterion, set before testing, was not met.
- Combined real-time test (weapons and falls on several feeds at once): not passed.

Scores are model confidence, not probabilities. This is a research prototype and is not deployed. No weights, datasets, annotations or real footage are included. Full confidence intervals, false-alert rates and limitations are in [results](docs/results.md); external model and dataset terms are in [third-party notices](THIRD_PARTY_NOTICES.md).
