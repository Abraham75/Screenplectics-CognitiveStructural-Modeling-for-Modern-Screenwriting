import unittest
from camera_intelligence import (
    ReferenceFootage, ShotTechnique, TECHNIQUE_INSTRUCTIONS, plan_shot
)


class CameraIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.reference = ReferenceFootage("clip-01", "Single reference clip", True, True)

    def test_nine_source_techniques(self):
        self.assertEqual(len(TECHNIQUE_INSTRUCTIONS), 9)

    def test_default_four_second_shot(self):
        plan = plan_shot(self.reference, ShotTechnique.DUTCH_ANGLE)
        self.assertEqual(plan.duration_seconds, 4)
        self.assertIn("25 degrees", plan.prompt)
        self.assertTrue(plan.synthetic_view)

    def test_requires_rights_and_consent(self):
        with self.assertRaises(PermissionError):
            plan_shot(ReferenceFootage("clip-02", "Unlicensed", False, True), ShotTechnique.ORBIT)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            plan_shot(self.reference, ShotTechnique.CRANE, duration_seconds=0)


if __name__ == "__main__":
    unittest.main()
