# Camera Intelligence — Shot Planning Feature

## Source and scope
Based on two user-supplied screenshots describing nine camera techniques and a workflow of one reference video, one prompt per angle, and approximately four seconds per shot. The screenshots claim fifteen techniques, but only nine are visible. No other six are inferred.

## Supported shot techniques
- Low angle: low camera tilted up; often conveys stature or power
- High angle: elevated camera tilted down; can convey vulnerability or scale
- Bird's-eye: straight down from above
- Worm's-eye: floor-level looking straight up
- Dutch angle: deliberate 25-degree roll (source-specific example, not a universal requirement)
- Dolly in: camera moves toward subject
- Orbit: camera circles subject
- Crane: camera rises from feet to above head
- Drone: camera moves up and back over room

Angle, camera movement, and camera platform are different categories. The initial API preserves source names for usability; future metadata should distinguish these types.

## Product placement
Projects > Scenes > Shot Planner. Each shot stores scene/shot identifiers, reference media, creative intent, technique, prompt, requested duration, generated result reference, review status and provenance.

## Implemented
camera_intelligence.py defines the nine techniques, consent/rights checks, typed shot plans, prompt assembly, default four-second duration, and explicit synthetic-view review requirements. test_camera_intelligence.py adds four tests.

## Not implemented
No video ingestion, uploads, AI video provider integration, 3D reconstruction, video rendering, interactive UI, shot sequencing, or physical camera control. Code is a planning layer only. Tests have not been run in CI.

## UX requirements
- Show storyboard thumbnails and a plain-language explanation of what each technique does.
- Let creators select shots based on narrative purpose, not only visual spectacle.
- Show expected duration, rights/consent requirements, generation cost estimate if available, and source provenance.
- Mark generated alternate views as synthesized and potentially inconsistent with reference geometry.
- Require human approval before publishing or exporting a generated sequence.
- Make the interface keyboard accessible and usable without color discrimination.

## Acceptance criteria for next milestone
1. Scene-to-shot data model with ordered shot list.
2. Shot technique selector with descriptive labels and previews.
3. Import authorized reference footage and maintain provenance.
4. Generate prompts with selectable model adapters and transparent failure handling.
5. Evaluate continuity/identity/representation with human review before approval.
6. Export approved shot list as CSV/JSON; never represent generated footage as real camera capture.

## Excluded from this feature
Claims of guaranteed 15-angle reconstruction, automatic fidelity to unseen geometry, physical drone/crane operation, and unrelated screenplay financing functionality.
