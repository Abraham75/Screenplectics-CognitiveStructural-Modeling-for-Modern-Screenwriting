"""Core screenplay assembly and export service.

This module owns application-level screenplay composition. Element definitions
live in ``screenplay_elements.py`` and low-level rendering rules live in
``screenplay_utils.py``. Keeping those concerns separate makes formatting rules
testable without coupling them to CLI or orchestration code.
"""

from __future__ import annotations

from collections.abc import Iterable

from screenplay_elements import ScreenplayElement
from screenplay_pdf import generate_pdf
from screenplay_utils import format_element, validate_element


class ScreenplayFormatter:
    """Validate, format, assemble, and export screenplay elements."""

    def __init__(self) -> None:
        self._elements: list[ScreenplayElement] = []

    @property
    def elements(self) -> tuple[ScreenplayElement, ...]:
        """Return an immutable view of the screenplay's source elements."""
        return tuple(self._elements)

    def add_element(self, element: ScreenplayElement) -> None:
        """Validate and append one screenplay element.

        Raises:
            TypeError: If ``element`` is not a supported screenplay element.
            ValueError: If the element contains invalid or empty content.
        """
        validate_element(element, raise_on_error=True)
        self._elements.append(element)

    def extend(self, elements: Iterable[ScreenplayElement]) -> None:
        """Append several validated elements in source order."""
        for element in elements:
            self.add_element(element)

    def render_text(self) -> str:
        """Render the complete screenplay as formatted plain text."""
        return "".join(format_element(element) for element in self._elements)

    def export_to_txt(self, filename: str) -> None:
        """Persist the rendered screenplay as UTF-8 plain text."""
        with open(filename, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(self.render_text())

    def export_to_pdf(self, filename: str) -> None:
        """Render the screenplay into a PDF using the PDF adapter."""
        generate_pdf(
            [format_element(element) for element in self._elements],
            filename,
        )


def build_example_screenplay() -> ScreenplayFormatter:
    """Return a minimal example useful for smoke tests and documentation."""
    from screenplay_elements import Action, Character, Dialogue, Slugline

    formatter = ScreenplayFormatter()
    formatter.extend(
        [
            Slugline("INT. HOUSE - NIGHT"),
            Action("Wind pushes through a broken window."),
            Character("JOHN"),
            Dialogue("I told you this would happen.", parenthetical="whispering"),
        ]
    )
    return formatter


if __name__ == "__main__":
    example = build_example_screenplay()
    print(example.render_text())
