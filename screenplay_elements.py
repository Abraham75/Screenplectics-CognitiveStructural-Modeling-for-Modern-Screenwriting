"""Domain objects representing canonical screenplay elements."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SpeechMode(str, Enum):
    """Industry-standard character cue extensions."""

    VOICE_OVER = "V.O."
    OFF_SCREEN = "O.S."


@dataclass(frozen=True, slots=True)
class ScreenplayElement:
    """Base immutable screenplay element."""

    content: str

    def __post_init__(self) -> None:
        normalized = self.content.strip() if isinstance(self.content, str) else ""
        if not normalized:
            raise ValueError(f"{type(self).__name__} content cannot be empty")
        object.__setattr__(self, "content", normalized)


@dataclass(frozen=True, slots=True)
class Slugline(ScreenplayElement):
    """Scene heading, e.g. ``INT. OFFICE - DAY``."""


@dataclass(frozen=True, slots=True)
class Action(ScreenplayElement):
    """Visible or audible action description."""


@dataclass(frozen=True, slots=True)
class Character(ScreenplayElement):
    """Character cue optionally qualified by V.O. or O.S."""

    speech_mode: SpeechMode | None = None
    target: str | None = None

    @property
    def cue(self) -> str:
        cue = self.content.upper()
        if self.target:
            cue += f" (to {self.target.upper()})"
        if self.speech_mode:
            cue += f" ({self.speech_mode.value})"
        return cue


@dataclass(frozen=True, slots=True)
class Dialogue(ScreenplayElement):
    """Spoken dialogue with an optional performance parenthetical."""

    parenthetical: str | None = None

    def __post_init__(self) -> None:
        # Explicit base call is used because dataclass(slots=True) creates a new
        # class object and zero-argument super() is not reliable in that mode.
        ScreenplayElement.__post_init__(self)
        if self.parenthetical:
            cleaned = self.parenthetical.strip().strip("()")
            object.__setattr__(self, "parenthetical", cleaned or None)


@dataclass(frozen=True, slots=True)
class Transition(ScreenplayElement):
    """Scene transition such as ``CUT TO:`` or ``FADE OUT:``."""
