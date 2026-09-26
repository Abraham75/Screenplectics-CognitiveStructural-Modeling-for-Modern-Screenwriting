"""Planning and routing engine for coordinated Screenplectics AI workflows.

The orchestrator deliberately does not execute specialist work. It decomposes a
request, assigns work according to comparative advantage, defines dependencies,
and emits explicit handoff contracts that can be executed by external models,
services, humans, or future agent adapters.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from orchestration_models import AgentRole, OrchestrationPlan, TaskBrief


class ScreenplayOrchestrator:
    """Builds auditable multi-role plans for screenplay and film-development work."""

    def create_plan(
        self,
        request: str,
        *,
        audience: str = "screenwriter / producer",
        deliverable: str = "decision-ready screenplay development package",
        deadline: str | None = None,
        requires_research: bool = False,
        requires_technical_work: bool = True,\n        requires_audience_validation: bool = False,
    ) -> OrchestrationPlan:
        if not request or not request.strip():
            raise ValueError("request must contain a non-empty objective")

        request = request.strip()
        tasks: list[TaskBrief] = []

        if requires_research:
            tasks.append(
                TaskBrief(
                    task_id="research",
                    role=AgentRole.RESEARCHER,
                    objective="Establish verified external context relevant to the request.",
                    context=request,
                    inputs=(request,),
                    required_output=(
                        "Evidence table: evidence_id, claim, source, date, confidence, caveat"
                    ),
                    quality_bar="Separate verified facts from inference and explicitly flag uncertainty.",
                    constraints=("No unsupported claims.", "Prefer primary and authoritative sources."),
                )
            )

        if requires_audience_validation:
            audience_deps = ("research",) if requires_research else ()
            tasks.append(
                TaskBrief(
                    task_id="audience_architecture",
                    role=AgentRole.ANALYST,
                    objective="Define target audience hypotheses and pre-production signal experiments.",
                    context=request,
                    inputs=(request, "market evidence when available"),
                    required_output=(
                        "Audience hypotheses; falsification criteria; experiment ladder; "
                        "metrics; thresholds; provenance; caveats; stop/iterate/advance criteria"
                    ),
                    quality_bar=(
                        "Separate attention, retention, intent, conversion, payment, and advocacy. "
                        "Never equate views with willingness to pay."
                    ),
                    constraints=(
                        "Pre-register thresholds before interpreting results.",
                        "Do not claim commercial certainty from audience signals.",
                        "Preserve creator control over narrative decisions.",
                    ),
                    depends_on=audience_deps,
                )
            )

        analysis_dependencies = tuple(
            x for x in ("research" if requires_research else None,
                        "audience_architecture" if requires_audience_validation else None) if x
        )
        tasks.append(
            TaskBrief(
                task_id="analysis",
                role=AgentRole.ANALYST,
                objective="Convert the request and approved evidence into narrative and decision logic.",
                context=request,
                inputs=(request, "research evidence when available"),
                required_output="Assumptions, method, findings, alternatives, tradeoffs, recommendation criteria",
                quality_bar="Reason explicitly and cite evidence IDs when research is available.",
                constraints=("Do not replace missing evidence with silent assumptions.",),
                depends_on=analysis_dependencies,
            )
        )

        if requires_technical_work:
            tasks.append(
                TaskBrief(
                    task_id="technical",
                    role=AgentRole.TECHNICAL_SPECIALIST,
                    objective="Design or implement the software artifact required by the request.",
                    context=request,
                    inputs=(request, "current Screenplectics application architecture"),
                    required_output="Architecture/implementation artifact, dependencies, edge cases, tests, risks",
                    quality_bar="Distinguish conceptual examples from production-ready implementation.",
                    constraints=("Preserve modularity and backwards compatibility where practical.",),
                )
            )

        writer_dependencies = ["analysis"]\n        if requires_audience_validation:\n            writer_dependencies.append("audience_architecture")
        if requires_technical_work:
            writer_dependencies.append("technical")
        tasks.append(
            TaskBrief(
                task_id="writing",
                role=AgentRole.WRITER,
                objective="Draft the audience-facing creative or business deliverable.",
                context=request,
                inputs=(request, "approved analysis", "approved technical constraints"),
                required_output="Audience-tailored draft with placeholders marked [VERIFY] or [INSERT]",
                quality_bar="Use only approved facts, assumptions, and narrative constraints.",
                constraints=("Do not invent factual claims.",),
                depends_on=tuple(writer_dependencies),
            )
        )

        review_dependencies = ["analysis", "writing"]\n        if requires_audience_validation:\n            review_dependencies.append("audience_architecture")
        if requires_technical_work:
            review_dependencies.append("technical")
        if requires_research:
            review_dependencies.append("research")
        tasks.append(
            TaskBrief(
                task_id="red_team",
                role=AgentRole.CRITIC,
                objective="Identify material weaknesses before final synthesis.",
                context=request,
                inputs=("evidence", "analysis", "draft", "technical artifact"),
                required_output="Prioritized Critical/Major/Minor issue list; each issue includes a proposed fix",
                quality_bar="Challenge conclusions; identify unsupported claims, contradictions, omissions, and risks.",
                depends_on=tuple(review_dependencies),
            )
        )

        tasks.append(
            TaskBrief(
                task_id="synthesis",
                role=AgentRole.EDITOR,
                objective="Reconcile reviewed work into a decision-ready final deliverable.",
                context=request,
                inputs=("all specialist outputs", "red-team findings", "change log"),
                required_output=(
                    "Executive summary; objective/scope; verified findings; analysis/options; "
                    "recommendation; implementation plan; risks/assumptions/unresolved questions; "
                    "sources when applicable; change log"
                ),
                quality_bar="Preserve meaningful disagreement and uncertainty rather than hiding it.",
                depends_on=("red_team",),
            )
        )

        plan = OrchestrationPlan(
            objective=request,
            audience=audience,
            deliverable=deliverable,
            constraints=[
                "Label material claims as Verified, Inferred, Assumed, or Opinion.",
                "Every specialist handoff must state confidence, unresolved questions, and risks.",
                "High-stakes subject matter requires qualified human review.",\n                "Audience signals inform development and financing decisions; they do not guarantee demand or recoupment.",
            ],
            success_criteria=[
                "Every workstream has a clear owner and artifact.",
                "Dependencies are explicit and acyclic at the planning level.",
                "The final output is traceable to specialist inputs and review findings.",
            ],
            deadline=deadline,
            tasks=tasks,
        )
        plan.validate_dependencies()
        return plan

    @staticmethod
    def to_dict(plan: OrchestrationPlan) -> dict[str, Any]:
        """Serialize a plan for APIs, JSON persistence, or UI rendering."""
        return asdict(plan)

    @staticmethod
    def render_markdown(plan: OrchestrationPlan) -> str:
        """Render the planning artifact in a human-reviewable format."""
        lines = [
            "# Orchestration Plan",
            "",
            f"**Objective:** {plan.objective}",
            f"**Audience:** {plan.audience}",
            f"**Deliverable:** {plan.deliverable}",
            f"**Deadline:** {plan.deadline or 'Not specified'}",
            "",
            "## Task Graph",
            "",
            "| Task | Role | Depends on | Required output |",
            "|---|---|---|---|",
        ]
        for task in plan.tasks:
            dependencies = ", ".join(task.depends_on) or "None"
            lines.append(
                f"| {task.task_id} | {task.role.value} | {dependencies} | {task.required_output} |"
            )
        lines.extend(["", "## Constraints"])
        lines.extend(f"- {item}" for item in plan.constraints)
        lines.extend(["", "## Success Criteria"])
        lines.extend(f"- {item}" for item in plan.success_criteria)
        return "\n".join(lines)
