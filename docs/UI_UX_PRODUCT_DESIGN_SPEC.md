# Screenplectics — UI/UX Research and Product Design Specification
Version: 0.1 (research-informed proposal) | 2026-11-08
Status: Design specification; not a deployed UI or completed usability study.

## Product promise
Help people create, evaluate, improve, and present creative work with transparent evidence, meaningful human control, and accessible interactions. Do not imply that artistic quality, audience demand, or representational fairness can be established by a single AI score.

## Evidence and design rationale
- W3C WCAG 2.2 (normative): https://www.w3.org/TR/WCAG22/ — target Level AA, test keyboard navigation, focus, targets, forms, text alternatives, responsive layout, error prevention and screen-reader announcements.
- Nielsen Norman Group, Progressive Disclosure: https://www.nngroup.com/articles/progressive-disclosure/ — prioritize frequent actions and progressively expose complex settings.
- Nielsen Norman Group, Strength of User Research Evidence: https://www.nngroup.com/articles/ux-evidence/ — diversify participants, tasks, methods, and contexts; do not generalize from one user group.
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework — design for accountability, transparency, privacy, human oversight and recourse.
- NIST AI RMF Playbook: https://airc.nist.gov/airmf-resources/playbook/ — document decisions, oversight, limitations, and feedback loops.

These sources inform requirements, but do not establish usability of this particular proposed interface. Usability and accessibility must be tested.

## Primary users and jobs to be done
1. Emerging creator: "Help me understand how my work is evaluated, what evidence supports feedback, and how to improve it without gatekeeper access."
2. Independent producer: "Show me which claims about audience demand are supported before I commit money."
3. Representation researcher/auditor: "Help me find, document, compare, and challenge AI image representation failures."
4. Human reviewer: "Let me assess work independently, explain my reasoning, and register disagreement."

## Information architecture (MVP)
Primary navigation: Projects | Evaluations | Evidence | Reports.
Secondary: Settings, Accessibility, Help, Privacy/consent, Reviewer administration.
Project detail tabs: Overview | Artifacts | Experiments | Findings | Decisions.
Do not lead with agent topology, model configuration, or algorithmic scores.

## Core journeys
A. Creator onboarding: explain purpose and limitations -> create project -> consent/privacy choices -> upload/link artifact -> choose evaluation purpose -> preview rubric -> submit -> inspect findings and sources -> challenge or accept -> export portable report.
B. Audience experiment: define hypothesis -> define outcome and baseline -> register creative variants -> import observations -> review quality warnings -> compare outcomes with uncertainty -> human decision -> log rationale.
C. Representation audit: define attributes and context -> create controlled prompt set -> log model version and outputs -> human reviewer assessments -> disaggregated failures -> record disagreement -> remediation and retest.
D. Reviewer: see assignment and conflict-of-interest disclosure -> apply criterion-anchored rubric -> cite evidence -> save draft -> submit -> review disagreement (without retroactively changing original rating).
E. Producer: inspect summary -> expand evidence provenance and caveats -> compare options -> record decision with confidence and accountable owner.

## Essential screens and content hierarchy
1. Home: recent projects, unfinished actions, next decision, clearly labeled evidence gaps.
2. Create project: minimal fields (title, type, objective); optional advanced metadata.
3. Evaluation setup: purpose, rubric, scope, reviewer policy, cost/time estimate, consent.
4. Evaluation workspace: artifact viewer + criterion-specific assessments + cited passages or images.
5. Findings: per-dimension results, reviewer count, disagreement, evidence links, missing data, limitations. Never present a single unqualified "quality score".
6. Experiment comparison: consistent denominators, sampling context, baseline, sample size, confidence interval when justified, observed vs inferred distinction.
7. Decision: STOP / ITERATE / ADVANCE / SCALE as suggested options, not automated determinations; explicit human approval and rationale.
8. Report: printable/exportable, accessible, provenance-linked, includes rubric/model versions and dissent.
9. Challenge assessment: choose disputed criterion, provide reasoning, request independent review; preserve original and revised history.
10. Settings: privacy, retention, permissions, accessibility preferences, model/provider controls.

## Interaction rules
- Start each page with the user's decision, not system internals.
- Label Verified / Inferred / Assumed / Opinion explicitly where factual claims appear.
- Show "Not measured" instead of zero when no data exists.
- Always expose the denominator and collection conditions behind percentages.
- Use progressive disclosure for advanced methodology, never hide a material caveat.
- Preserve drafts; confirm destructive actions; explain upload and evaluation progress.
- Avoid dark patterns and paid upsells inside review results.
- Provide human-readable explanations, source links, and an appeal pathway.
- A reviewer disagreement is a finding, not a software error.
- Support desktop-first complex review and responsive mobile read/review experiences.

## Design system proposal
Brand personality: credible, creative, calm, non-judgmental, precise.
Palette: ink #17212B; canvas #F7F8FA; white #FFFFFF; accent teal #087E79; secondary blue #345995; amber #996600; danger #B42318.
Colors are proposals only; verify text and UI contrast with automated and manual testing.
Typography: accessible sans-serif (system UI preferred); base 16px; readable line length; scalable text and responsive spacing.
Spacing: 4px scale; controls >= 44px preferred, with WCAG 2.2 target-size compliance verified.
Data visualizations: direct labels, tabular alternatives, patterns/shapes rather than color alone.
Motion: restrained, respects reduced-motion settings; no essential information conveyed through animation.
States: empty, loading, partial, complete, uncertain, error, permission denied, no evidence.
Copy: plain language first; optional expandable methodology and statistical details.

## Accessibility and inclusion acceptance criteria
- WCAG 2.2 AA target, not claimed certification.
- Full keyboard access; logical focus; visible focus; no keyboard traps.
- Screen reader semantics for every chart, form, status, and interactive comparison.
- Text resizing/reflow, sufficient contrast, captions/transcripts, descriptive alternatives.
- Test with users with visual, mobility, hearing, and cognitive disabilities, including assistive technology.
- Accessible error recovery and alternative nonvisual ways to interpret images and charts.
- Representation audits must avoid treating protected identities as automatically inferable from appearance.

## Privacy, security and creator rights
- Explicit purpose-limited consent; minimize collection of sensitive identity information.
- Creator controls artifact visibility and sharing; private by default.
- Clearly state whether uploaded content is sent to external model providers.
- No silent model training on uploaded creative work.
- Role-based permissions, audit trail, deletion/export request workflow, retention policy.
- Human review and appeal for consequential evaluation decisions.
- Legal/privacy review before deployment; these are requirements, not implemented guarantees.

## MVP scope
Build first: project creation, evaluation setup, rubric preview, artifact viewer, evidence-backed findings, challenge flow, exportable report.
Second: experiment imports, comparisons, and decision log.
Later: image audit generation integrations, collaboration, billing, autonomous agents, predictive financing.
Avoid: social feed, creator ranking leaderboard, opaque single-number score, universal "success probability".

## Usability research plan
Round 0: 8-12 discovery interviews across emerging creators, producers, and evaluators (planning target, not a statistical sample).
Round 1: clickable prototype tested on 5-8 participants per primary workflow; include assistive technology users and diverse experience levels.
Round 2: revise and test with new participants; measure task success, time, critical errors, comprehension, perceived agency, and trust calibration.
Research questions:
- Can creators understand the evaluation purpose and rubric before consenting?
- Can users distinguish observations from inferences and missing data?
- Can a user locate and challenge a disputed assessment without assistance?
- Can producers identify a recommendation's evidence and limitations?
- Can screen-reader and keyboard users complete the core workflow?
Pre-register tasks and acceptance criteria; do not claim usability until observed.

## Instrumentation
Track privacy-conscious events: project_created, rubric_previewed, evaluation_started, evidence_opened, finding_challenged, report_exported, decision_recorded, error_recovered.
Avoid tracking sensitive creative text or inferred protected characteristics in analytics.
Track task completion, drop-off, critical error frequency, appeal success, accessibility defects, and time to first meaningful insight.

## Proposed delivery gates
G0: user interviews confirm target problems and primary workflow.
G1: accessible low-fidelity prototype passes internal walkthrough.
G2: moderated usability tests identify and resolve critical blockers.
G3: front-end implementation connected to real evaluation records; no fabricated results.
G4: accessibility audit and security/privacy review.
G5: controlled pilot with consenting users; measure repeat usage and willingness to pay.

## Suggested implementation stack (subject to repository review)
Web: React + TypeScript; accessible component primitives; server API in Python/FastAPI; PostgreSQL for project/evaluation records; object storage for artifacts.
Do not adopt a stack merely because it is popular; verify hosting, engineering resources, and integration requirements first.

## Immediate next engineering tasks
1. Define typed frontend API contracts for Project, EvaluationCase, Assessment, Evidence, Finding, Challenge, and Decision.
2. Create low-fidelity flows and a design-token package.
3. Build an accessible clickable prototype of Home -> Project -> Evaluation -> Findings -> Challenge -> Report.
4. Connect prototype to existing evaluation_core.py records via a minimal API.
5. Conduct usability tests before committing to visual polish or a complex dashboard.

## What remains uncertain
No user research has yet validated these personas, information architecture, pricing, or visual language. The existing GitHub repository is primarily a Python toolkit; this file is a design brief, not a working UI. No accessibility conformance claim is warranted without testing.
