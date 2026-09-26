"""Audience-demand modeling for Screenplectics.

This module turns an audience thesis into explicit, testable hypotheses. It does
not predict box office or guarantee financing outcomes. Scores summarize observed
signals and must retain provenance and caveats.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class SignalType(str, Enum):
    ATTENTION="attention"
    RETENTION="retention"
    INTENT="intent"
    CONVERSION="conversion"
    PAYMENT="payment"
    ADVOCACY="advocacy"

@dataclass(frozen=True, slots=True)
class AudienceHypothesis:
    segment: str
    need_or_tension: str
    story_promise: str
    expected_behavior: str
    falsification_condition: str

@dataclass(frozen=True, slots=True)
class SignalExperiment:
    experiment_id: str
    hypothesis: AudienceHypothesis
    artifact: str
    channel: str
    signal_type: SignalType
    metric: str
    threshold: float
    sample_size_target: int
    cost_cap: float | None = None
    notes: tuple[str, ...] = ()

    def __post_init__(self):
        if self.sample_size_target <= 0:
            raise ValueError("sample_size_target must be positive")
        if self.threshold < 0:
            raise ValueError("threshold cannot be negative")

@dataclass(frozen=True, slots=True)
class SignalObservation:
    experiment_id: str
    signal_type: SignalType
    metric: str
    value: float
    sample_size: int
    source: str
    observed_at: str
    caveat: str = ""

@dataclass(slots=True)
class AudienceEvidence:
    project: str
    observations: list[SignalObservation] = field(default_factory=list)

    def add(self, observation: SignalObservation) -> None:
        if observation.sample_size < 0:
            raise ValueError("sample_size cannot be negative")
        self.observations.append(observation)

    def evidence_by_signal(self) -> dict[SignalType, list[SignalObservation]]:
        grouped={kind: [] for kind in SignalType}
        for item in self.observations:
            grouped[item.signal_type].append(item)
        return grouped

    def strongest_signal(self) -> SignalType | None:
        """Return highest-funnel-depth signal observed, not a success verdict."""
        order=[SignalType.PAYMENT, SignalType.CONVERSION, SignalType.INTENT,
               SignalType.RETENTION, SignalType.ADVOCACY, SignalType.ATTENTION]
        present={x.signal_type for x in self.observations}
        return next((x for x in order if x in present), None)

def experiment_ladder(hypothesis: AudienceHypothesis) -> list[SignalExperiment]:
    """Create a default progression from cheap attention tests to payment evidence."""
    specs=[
        ("attention", SignalType.ATTENTION, "qualified_view_rate"),
        ("retention", SignalType.RETENTION, "completion_rate"),
        ("intent", SignalType.INTENT, "waitlist_or_follow_rate"),
        ("conversion", SignalType.CONVERSION, "landing_page_conversion"),
        ("payment", SignalType.PAYMENT, "paid_preorder_or_ticket_conversion"),
    ]
    return [
        SignalExperiment(f"aud-{i:02d}", hypothesis, "minimum viable story artifact",
                         "creator-controlled test channel", kind, metric, 0.0, 100,
                         notes=("Set threshold from comparable baseline before launch.",
                                "Do not treat platform engagement as proof of payment intent."))
        for i,(_,kind,metric) in enumerate(specs,1)
    ]
