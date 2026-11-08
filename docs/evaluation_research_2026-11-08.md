# Evaluation Core — Research and Implementation Decision (2026-11-08)

## Mission
Make rigorous, contestable evaluation accessible to creators, while measuring AI representation failures without reducing people or creative quality to opaque scores.

## Evidence informing design
- NIST AI RMF Measure: document uncertainty, evaluate fairness and bias, permit feedback and appeal. https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST Generative AI Profile: define context of use, document measurement plans, include diverse interdisciplinary reviewers. https://doi.org/10.6028/NIST.AI.600-1
- Wallach et al., *Evaluating Generative AI Systems is a Social Science Measurement Challenge*: define constructs before instruments. https://arxiv.org/abs/2411.10939

## Implemented in this branch
- Domain-specific evaluation cases, rubric versioning and explicit construct definitions
- Evidence-backed reviewer assessments
- Range and mean to preserve reviewer disagreement
- Validation of unknown criteria, out-of-range scores and duplicate assessments
- Explicit unassessed values instead of misleading zeros

## Not implemented
- Human-reviewer recruitment or credentials verification
- Inter-rater reliability statistics, calibration, construct validity studies
- AI image-generation adapters, image scoring, consent and privacy workflows
- Benchmark dataset, statistical power analysis, accessibility audit
- Deployment or production-grade persistence

## Next engineering gates
1. Run the unit test suite in CI and correct failures.
2. Add persisted evaluation runs and a CSV import/export contract.
3. Design two pilot rubrics with independent subject-matter experts.
4. Measure reviewer agreement and publish disagreement and limitations.
5. Pilot with consenting creators and affected communities; evaluate whether feedback changes decisions.
6. Test paid customer demand before adding autonomous agents.

## Non-negotiable
No automatic hiring, casting, financing, or creative exclusion decisions based solely on a score. Human review and an appeal pathway are required.
