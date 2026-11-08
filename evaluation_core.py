"""Evidence-first evaluation records for creative and representation studies.

This module records claims, criteria and independent assessments. It does not
infer artistic quality, identity, or model fairness automatically.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from statistics import mean


class EvaluationDomain(str, Enum):
    CREATIVE = "creative"
    REPRESENTATION = "representation"


@dataclass(frozen=True, slots=True)
class Criterion:
    criterion_id: str
    description: str
    construct: str
    rubric_version: str
    minimum: float = 0.0
    maximum: float = 4.0

    def __post_init__(self):
        if not self.criterion_id.strip() or not self.construct.strip():
            raise ValueError("criterion and construct are required")
        if self.minimum >= self.maximum:
            raise ValueError("minimum must be below maximum")


@dataclass(frozen=True, slots=True)
class Assessment:
    criterion_id: str
    reviewer_id: str
    score: float
    evidence_reference: str
    rationale: str

    def __post_init__(self):
        if not self.reviewer_id.strip() or not self.evidence_reference.strip():
            raise ValueError("reviewer and evidence provenance are required")
        if not self.rationale.strip():
            raise ValueError("assessment rationale is required")


@dataclass(slots=True)
class EvaluationCase:
    case_id: str
    domain: EvaluationDomain
    artifact_reference: str
    context_of_use: str
    criteria: list[Criterion]
    assessments: list[Assessment] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    def record(self, assessment: Assessment) -> None:
        criterion = next((c for c in self.criteria if c.criterion_id == assessment.criterion_id), None)
        if criterion is None:
            raise ValueError("unknown criterion")
        if not criterion.minimum <= assessment.score <= criterion.maximum:
            raise ValueError("score outside rubric bounds")
        if any(a.criterion_id == assessment.criterion_id and a.reviewer_id == assessment.reviewer_id
               for a in self.assessments):
            raise ValueError("duplicate reviewer assessment")
        self.assessments.append(assessment)

    def report(self) -> dict:
        results = {}
        for criterion in self.criteria:
            ratings = [a.score for a in self.assessments if a.criterion_id == criterion.criterion_id]
            results[criterion.criterion_id] = {
                "reviewer_count": len(ratings),
                "mean_score": mean(ratings) if ratings else None,
                "range": max(ratings) - min(ratings) if len(ratings) >= 2 else None,
                "rubric_version": criterion.rubric_version,
                "construct": criterion.construct,
            }
        return {
            "case_id": self.case_id,
            "domain": self.domain.value,
            "context_of_use": self.context_of_use,
            "artifact_reference": self.artifact_reference,
            "criteria": results,
            "limitations": list(self.limitations),
            "disclaimer": "Descriptive reviewer assessments; not a validated quality or fairness certification.",
        }
