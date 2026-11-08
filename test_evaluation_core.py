import unittest
from evaluation_core import Criterion, Assessment, EvaluationCase, EvaluationDomain


class EvaluationCoreTests(unittest.TestCase):
    def setUp(self):
        self.case = EvaluationCase(
            "case-1", EvaluationDomain.CREATIVE, "script:v1", "pilot screening",
            [Criterion("agency", "Character agency", "character agency", "1.0")]
        )

    def test_report_retains_disagreement(self):
        self.case.record(Assessment("agency", "reviewer-a", 2, "scene:1", "Limited agency"))
        self.case.record(Assessment("agency", "reviewer-b", 4, "scene:2", "Strong choice"))
        report = self.case.report()["criteria"]["agency"]
        self.assertEqual(report["mean_score"], 3)
        self.assertEqual(report["range"], 2)

    def test_reject_unknown_criterion(self):
        with self.assertRaises(ValueError):
            self.case.record(Assessment("missing", "reviewer-a", 2, "scene:1", "Reason"))

    def test_reject_duplicate_assessment(self):
        a = Assessment("agency", "reviewer-a", 2, "scene:1", "Reason")
        self.case.record(a)
        with self.assertRaises(ValueError):
            self.case.record(a)

    def test_unassessed_criterion_is_not_zero(self):
        self.assertIsNone(self.case.report()["criteria"]["agency"]["mean_score"])


if __name__ == "__main__":
    unittest.main()
