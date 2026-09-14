"""Command-line interface for screenplay formatting and orchestration planning."""

from __future__ import annotations

import argparse
from pathlib import Path

from orchestrator import ScreenplayOrchestrator
from screenplay_elements import Action, Character, Dialogue, Slugline, SpeechMode
from screenplay_formatter import ScreenplayFormatter


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Screenplectics screenplay formatting and planning toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    sample = subparsers.add_parser(
        "sample",
        help="Generate a sample formatted screenplay PDF.",
    )
    sample.add_argument(
        "--output",
        default="screenplay_output.pdf",
        help="Destination PDF filename.",
    )

    plan = subparsers.add_parser(
        "plan",
        help="Create a multi-model orchestration plan without executing agents.",
    )
    plan.add_argument("request", help="Creative, research, or technical objective.")
    plan.add_argument("--audience", default="screenwriter / producer")
    plan.add_argument(
        "--deliverable",
        default="decision-ready screenplay development package",
    )
    plan.add_argument("--deadline", default=None)
    plan.add_argument(
        "--research",
        action="store_true",
        help="Include an evidence-gathering workstream before analysis.",
    )
    plan.add_argument(
        "--no-technical",
        action="store_true",
        help="Omit software/implementation work when the request is purely creative.",
    )
    plan.add_argument(
        "--output",
        help="Optional Markdown path. Prints to stdout when omitted.",
    )

    return parser


def _run_sample(output: str) -> None:
    formatter = ScreenplayFormatter()
    formatter.extend(
        [
            Slugline("EXT. PARK - NIGHT"),
            Action("Dogs bark in the distance as a figure crosses beneath a streetlamp."),
            Character("DETECTIVE HARRIS", speech_mode=SpeechMode.OFF_SCREEN),
            Dialogue(
                "Something does not add up here.",
                parenthetical="under his breath",
            ),
        ]
    )
    formatter.export_to_pdf(output)
    print(f"Created {output}")


def _run_plan(args: argparse.Namespace) -> None:
    orchestrator = ScreenplayOrchestrator()
    plan = orchestrator.create_plan(
        args.request,
        audience=args.audience,
        deliverable=args.deliverable,
        deadline=args.deadline,
        requires_research=args.research,
        requires_technical_work=not args.no_technical,
    )
    rendered = orchestrator.render_markdown(plan)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Created {output_path}")
    else:
        print(rendered)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "sample":
        _run_sample(args.output)
    elif args.command == "plan":
        _run_plan(args)
    else:  # Defensive guard for future subcommands.
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
