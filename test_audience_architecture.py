import unittest
from audience_architecture import (AudienceEvidence, AudienceHypothesis, SignalObservation,
                                   SignalType, experiment_ladder)

class AudienceArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.h=AudienceHypothesis("women 35-54 navigating identity transitions",
            "selfhood can become submerged beneath obligation",
            "a mature identity-awakening drama", "complete and share serialized episodes",
            "retention and intent fail to exceed a pre-registered comparable baseline")

    def test_ladder_progresses_to_payment(self):
        ladder=experiment_ladder(self.h)
        self.assertEqual(ladder[0].signal_type, SignalType.ATTENTION)
        self.assertEqual(ladder[-1].signal_type, SignalType.PAYMENT)

    def test_payment_is_stronger_than_attention(self):
        e=AudienceEvidence("test")
        e.add(SignalObservation("1",SignalType.ATTENTION,"views",1000,1000,"test","2026-09-26"))
        e.add(SignalObservation("2",SignalType.PAYMENT,"preorders",3,100,"test","2026-09-26"))
        self.assertEqual(e.strongest_signal(), SignalType.PAYMENT)

if __name__=="__main__":
    unittest.main()
