# Screenplectics: Cognitive-Structural Modeling for Modern Screenwriting

A modular Python toolkit for screenplay parsing, formatting, narrative modeling, and coordinated multi-model AI planning.

## Overview

Screenplectics treats screenplay development as both a creative process and a structured computational system. The project combines two complementary layers:

1. **Screenplay domain layer** — canonical screenplay elements, validation, formatting, and PDF export.
2. **Multi-model orchestration layer** — request decomposition, role assignment, dependency management, explicit handoffs, red-team review, and final synthesis planning.

The orchestration layer does **not** pretend that one model should perform every task. Instead, it creates an auditable task graph that routes work according to comparative advantage: research to a Researcher, structured reasoning to an Analyst, prose to a Writer, implementation to a Technical Specialist, adversarial review to a Critic, and reconciliation to a Final Synthesizer.

## Architecture

```text
User Request
    |
    v
ScreenplayOrchestrator
    |
    +--> Researcher (optional) ----+
    |                              |
    +--> Technical Specialist -----+----> Analyst ----> Writer
                                                   \       /
                                                    Red Team
                                                       |
                                                       v
                                                Final Synthesizer

Screenplay Domain Layer
    screenplay_elements.py
        -> screenplay_utils.py
        -> screenplay_formatter.py
        -> screenplay_pdf.py
```

### Core orchestration guarantees

- Explicit task ownership and dependencies
- Typed handoff contracts
- Confidence, uncertainty, and risk fields
- Separation of verified facts from inference and assumption
- Red-team review before synthesis
- Preservation of unresolved disagreement
- Human-review warning for high-stakes domains

## Screenplay Formatting Features

The screenplay subsystem supports:

- Sluglines / scene headings
- Action blocks
- Character cues
- Dialogue
- Parentheticals
- `V.O.` and `O.S.` character extensions
- Character-target cues such as `JOHN (to MARY)`
- Scene transitions
- Plain-text rendering
- PDF export

The renderer uses consistent screenplay spacing and indentation conventions while keeping semantic screenplay elements separate from their presentation logic.

## Multi-Model Roles

| Role | Primary responsibility |
|---|---|
| Orchestrator | Decomposition, routing, dependencies, quality control |
| Researcher | Source evaluation, evidence gathering, chronology, market research |
| Analyst | Structured reasoning, comparisons, scenarios, decision criteria |
| Writer | Audience-aware drafting using approved facts and assumptions |
| Technical Specialist | Architecture, implementation, tests, edge cases, risks |
| Critic / Red Team | Unsupported claims, contradictions, omissions, failure modes |
| Editor / Final Synthesizer | Reconciliation and decision-ready final output |

## Repository Structure

```text
.
├── orchestration_models.py   # Typed roles, task briefs, plans, handoff contracts
├── orchestrator.py           # Task graph and routing engine
├── test_orchestrator.py      # Unit tests for orchestration behavior
├── screenplay_elements.py    # Canonical screenplay domain objects
├── screenplay_utils.py       # Validation and plain-text rendering rules
├── screenplay_formatter.py   # Screenplay assembly and export service
├── screenplay_pdf.py         # PDF adapter
├── cli.py                    # CLI for screenplay samples and orchestration plans
├── requirements.txt          # Runtime dependency declaration
└── README.md
```

## Installation

```bash
git clone https://github.com/Abraham75/Screenplectics-CognitiveStructural-Modeling-for-Modern-Screenwriting.git
cd Screenplectics-CognitiveStructural-Modeling-for-Modern-Screenwriting
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## CLI Usage

### Generate a sample screenplay PDF

```bash
python cli.py sample --output screenplay_output.pdf
```

### Create an orchestration plan

```bash
python cli.py plan "Develop a ten-episode vertical micro-drama for independent producers" --research
```

Write the planning artifact to Markdown:

```bash
python cli.py plan "Assess and package a screenplay for market outreach" \
  --audience "independent producers and representation" \
  --deliverable "market-ready development package" \
  --research \
  --output plan.md
```

The `plan` command creates the task graph and handoff specifications only. It intentionally does not execute external AI agents yet. This makes the current implementation deterministic, inspectable, and suitable as the control plane for later provider integrations.

## Programmatic Example

```python
from orchestrator import ScreenplayOrchestrator

orchestrator = ScreenplayOrchestrator()
plan = orchestrator.create_plan(
    "Build a market-ready micro-drama package",
    audience="independent producers",
    requires_research=True,
    requires_technical_work=False,
)

print(orchestrator.render_markdown(plan))
```

## Testing

Run the orchestration unit tests with the Python standard library:

```bash
python -m unittest test_orchestrator.py
```

## Current Design Boundary

The current release implements the **orchestration control plane**, not autonomous multi-provider execution. Future adapters can connect the task briefs to LLM APIs, search systems, screenplay generation models, or human workflows without changing the task-contract model.

This distinction is intentional: orchestration, provenance, evaluation, and handoff semantics should remain stable even when model providers change.

## Roadmap

- Provider-neutral agent execution interface
- Evidence registry with claim-level provenance
- Persistent change log across review cycles
- Screenplay beat and character-arc models
- FDX / Final Draft export
- Scene continuity validation
- Revision marks and production draft support
- Structured JSON/YAML screenplay import
- Human-in-the-loop approval gates
- Evaluation harness for generated screenplay quality
- Web UI for visual task graphs and screenplay editing

## Engineering Principles

- Separation of concerns
- Strong typing and immutable domain records where practical
- Explicit failure over silent fallback
- Testable deterministic planning
- Traceable handoffs
- Evidence-aware reasoning
- Human review for high-stakes outputs

## License

No license file is currently included. Add an explicit license before representing the repository as open source or permitting third-party reuse.
