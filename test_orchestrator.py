"""Unit tests for the Screenplectics orchestration layer."""

import unittest

from orchestration_models import AgentRole
from orchestrator import ScreenplayOrchestrator


class ScreenplayOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = ScreenplayOrchestrator()

    def test_empty_request_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.orchestrator.create_plan("   ")

    def test_default_plan_contains_required_review_chain(self) -> None:
        plan = self.orchestrator.create_plan("Develop a ten-episode micro-drama arc.")
        task_ids = [task.task_id for task in plan.tasks]

        self.assertIn("analysis", task_ids)
        self.assertIn("writing", task_ids)
        self.assertIn("technical", task_ids)
        self.assertIn("red_team", task_ids)
        self.assertIn("synthesis", task_ids)
        self.assertNotIn("research", task_ids)

        synthesis = plan.task("synthesis")
        self.assertEqual(synthesis.role, AgentRole.EDITOR)
        self.assertEqual(synthesis.depends_on, ("red_team",))

    def test_research_plan_routes_research_before_analysis(self) -> None:
        plan = self.orchestrator.create_plan(
            "Assess current micro-drama market conditions.",
            requires_research=True,
        )

        self.assertEqual(plan.task("research").role, AgentRole.RESEARCHER)
        self.assertEqual(plan.task("analysis").depends_on, ("research",))

    def test_initial_parallel_tasks_are_identified(self) -> None:
        plan = self.orchestrator.create_plan(
            "Design a screenplay workflow.",
            requires_research=True,
            requires_technical_work=True,
        )
        initial = {task.task_id for task in plan.parallelizable_tasks()}
        self.assertEqual(initial, {"research", "technical"})

    def test_markdown_render_contains_task_graph(self) -> None:
        plan = self.orchestrator.create_plan("Generate a screenplay package.")
        rendered = self.orchestrator.render_markdown(plan)
        self.assertIn("# Orchestration Plan", rendered)
        self.assertIn("| Task | Role | Depends on | Required output |", rendered)


if __name__ == "__main__":
    unittest.main()
