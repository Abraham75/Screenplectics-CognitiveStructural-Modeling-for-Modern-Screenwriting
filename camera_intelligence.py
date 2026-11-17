"""Camera Intelligence: source-grounded shot plans and AI-video prompt specifications.

A shot plan is not a generated video. Unseen camera views require synthesis and
must be labeled as such; reference footage cannot guarantee 3D reconstruction.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ShotTechnique(str, Enum):
    LOW_ANGLE = "low_angle"
    HIGH_ANGLE = "high_angle"
    BIRDS_EYE = "birds_eye"
    WORMS_EYE = "worms_eye"
    DUTCH_ANGLE = "dutch_angle"
    DOLLY_IN = "dolly_in"
    ORBIT = "orbit"
    CRANE = "crane"
    DRONE = "drone"


TECHNIQUE_INSTRUCTIONS = {
    ShotTechnique.LOW_ANGLE: "Position camera low, pointing upward toward subject.",
    ShotTechnique.HIGH_ANGLE: "Position camera above subject, pointing downward.",
    ShotTechnique.BIRDS_EYE: "Frame a straight-down overhead view.",
    ShotTechnique.WORMS_EYE: "Frame from floor level, looking straight upward.",
    ShotTechnique.DUTCH_ANGLE: "Roll the camera 25 degrees for a deliberate tilted horizon.",
    ShotTechnique.DOLLY_IN: "Move camera smoothly toward subject.",
    ShotTechnique.ORBIT: "Move camera in a controlled arc around subject.",
    ShotTechnique.CRANE: "Raise camera from subject's feet to above their head.",
    ShotTechnique.DRONE: "Move camera upward and backward over the room.",
}


@dataclass(frozen=True, slots=True)
class ReferenceFootage:
    reference_id: str
    description: str
    rights_confirmed: bool
    subject_consent_confirmed: bool

    def __post_init__(self):
        if not self.reference_id.strip() or not self.description.strip():
            raise ValueError("reference ID and description required")


@dataclass(frozen=True, slots=True)
class ShotPlan:
    reference_id: str
    technique: ShotTechnique
    duration_seconds: float
    prompt: str
    synthetic_view: bool
    review_requirements: tuple[str, ...]


def plan_shot(
    reference: ReferenceFootage,
    technique: ShotTechnique,
    *,
    duration_seconds: float = 4.0,
    creative_intent: str = "",
) -> ShotPlan:
    if not reference.rights_confirmed or not reference.subject_consent_confirmed:
        raise PermissionError("reference rights and subject consent must be confirmed")
    if not 0 < duration_seconds <= 30:
        raise ValueError("duration must be greater than zero and at most 30 seconds")
    if not isinstance(technique, ShotTechnique):
        raise ValueError("unknown camera technique")
    prompt = (
        f"Use authorized reference footage '{reference.reference_id}' as a visual reference. "
        f"Create a {duration_seconds:g}-second shot. "
        f"{TECHNIQUE_INSTRUCTIONS[technique]} "
        "Preserve recognizable subject and scene details where observable. "
        "Do not claim physically unobserved details are verified. "
    )
    if creative_intent.strip():
        prompt += f"Creative intention: {creative_intent.strip()}."
    return ShotPlan(
        reference_id=reference.reference_id,
        technique=technique,
        duration_seconds=duration_seconds,
        prompt=prompt,
        synthetic_view=True,
        review_requirements=(
            "Check subject identity and appearance fidelity",
            "Check continuity of costume, environment and lighting",
            "Check geometry, anatomy and motion artifacts",
            "Label output as synthetic and obtain human approval",
        ),
    )
