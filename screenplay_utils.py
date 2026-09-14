"""Validation and plain-text rendering utilities for screenplay elements."""

from __future__ import annotations

from textwrap import fill

from screenplay_elements import (
    Action,
    Character,
    Dialogue,
    ScreenplayElement,
    Slugline,
    Transition,
)

CHARACTER_INDENT = 22
PARENTHETICAL_INDENT = 16
DIALOGUE_INDENT = 12
ACTION_WIDTH = 65
DIALOGUE_WIDTH = 42


def validate_element(
    element: object,
    *,
    raise_on_error: bool = False,
) -> bool:
    """Validate that an object is a supported, non-empty screenplay element."""
    valid = isinstance(element, ScreenplayElement) and bool(element.content.strip())
    if not valid and raise_on_error:
        raise TypeError("element must be a non-empty ScreenplayElement instance")
    return valid


def _indent_block(text: str, spaces: int, width: int) -> str:
    wrapped = fill(
        text.strip(),
        width=width,
        subsequent_indent="",
        break_long_words=False,
        break_on_hyphens=False,
    )
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" for line in wrapped.splitlines())


def format_element(element: ScreenplayElement) -> str:
    """Render one screenplay element using consistent screenplay spacing rules."""
    validate_element(element, raise_on_error=True)

    if isinstance(element, Slugline):
        return f"{element.content.upper()}\n\n"

    if isinstance(element, Action):
        return f"{fill(element.content, width=ACTION_WIDTH)}\n\n"

    if isinstance(element, Character):
        return f"{' ' * CHARACTER_INDENT}{element.cue}\n"

    if isinstance(element, Dialogue):
        pieces: list[str] = []
        if element.parenthetical:
            pieces.append(
                f"{' ' * PARENTHETICAL_INDENT}({element.parenthetical})\n"
            )
        pieces.append(
            f"{_indent_block(element.content, DIALOGUE_INDENT, DIALOGUE_WIDTH)}\n\n"
        )
        return "".join(pieces)

    if isinstance(element, Transition):
        return f"{element.content.upper():>65}\n\n"

    raise TypeError(f"Unsupported screenplay element: {type(element).__name__}")
