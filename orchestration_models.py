"""Typed domain models for the Screenplectics multi-model orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class EvidenceStatus(str, Enum):
    """Epistemic status attached to a claim or assumption."""

    VERIFIED = "Verified"
    INFERRED = "Inferred"
    ASSUMED = "Assumed"
    OPINION = "Opinion"


class AgentRole(str, Enum):
    """Roles available to the orchestration engine."""

    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    TECHNICAL_SPECIALIST = "technical_specialist"
    CRITIC = "critic_red_team"
    EDITOR = "editor_final_synthesizer"


@dataclass(frozen=True, slots=True)
class HandoffArtifact:
    """Contract passed between specialized agents."""

    objective: str
    inputs: tuple[str, ...]
    output_format: str
    confidence: float = 0.5
    unresolved_questions: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class TaskBrief:
    """A self-contained work order for one specialized AI role."""

    task_id: str
    role: AgentRole
    objective: str
    context: str
    inputs: tuple[str, ...]
    required_output: str
    quality_bar: str
    constraints: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()

    def handoff(self, confidence: float = 0.5) -> HandoffArtifact:
        return HandoffArtifact(
            objective=self.objective,
            inputs=self.inputs,
            output_format=self.required_output,
            confidence=confidence,
            unresolved_questions=(),
            risks=self.constraints,
        )


@dataclass(slots=True)
class OrchestrationPlan:
    """Decision-ready plan produced before specialist execution begins."""

    objective: str
    audience: str
    deliverable: str
    constraints: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    deadline: str | None = None
    tasks: list[TaskBrief] = field(default_factory=list)

    def task(self, task_id: str) -> TaskBrief:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise KeyError(f"Unknown task id: {task_id}")

    def validate_dependencies(self) -> None:
        known = {task.task_id for task in self.tasks}
        for task in self.tasks:
            missing = set(task.depends_on) - known
            if missing:
                raise ValueError(
                    f"Task {task.task_id} depends on undefined tasks: {sorted(missing)}"
                )

    def parallelizable_tasks(self, completed: Iterable[str] = ()) -> list[TaskBrief]:
        completed_set = set(completed)
        return [
            task
            for task in self.tasks
            if task.task_id not in completed_set
            and set(task.depends_on).issubset(completed_set)
        ]
