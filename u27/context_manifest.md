# U27-S03 // CONTEXT ENGINE MANIFEST

REF_ID: CONTEXT-ENGINE-01
CLASS: SYSTEM
FUNCTION: Context Ingestion + Token Intelligence
SOURCE: .
FILES_INCLUDED: 15
FILES_SKIPPED: 14
TOTAL_TOKENS: 7901
TOKEN_BUDGET: 50000
STATUS: PASS

## FILE: .gitignore

PATH: .gitignore
EXTENSION: 
PRIORITY: SUPPORTING
TOKENS: 31

```
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.venv/
dist/
build/
handoff-engine-demo/
```

## FILE: DESIGN_NOTES.md

PATH: DESIGN_NOTES.md
EXTENSION: .md
PRIORITY: SUPPORTING
TOKENS: 414

````markdown
# Handoff Engine Design Notes

`U27-S04 // HANDOFF ENGINE`

Handoff Engine exists to convert prepared context and a known objective into a bounded agent work packet.

## System Role

```text
Stack Engine -> Context Engine -> Knowledge Readiness -> Handoff Engine -> Eval Bench -> Proof Ledger -> Boundary Engine -> u27-check
```

Stack Engine shapes the work. Context Engine prepares the material. Knowledge Readiness classifies what the prepared context is allowed to become. Handoff Engine states exactly what the agent should do with approved context. Eval Bench runs declared checks. Proof Ledger records what happened after the work. Boundary Engine checks whether public language stays inside proof. `u27-check` gates the first user path.

## Boundary

Handoff Engine deliberately does not own scope selection, context scanning, eval execution, proof recording, public-claim review, or launch QA.

It creates the handoff packet that sits between those systems.

## Output Contract

The public artifact contract is:

```text
u27/handoff.json
u27/HANDOFF_PACKET.md
evals/proof_cases.json
```

The JSON file is the durable handoff record. The Markdown packet is readable by a reviewer or agent operator. The proof cases are starter claims for Proof Ledger.

## Failure Modes

1. The packet becomes too broad and starts acting like a project plan.
2. Acceptance checks are vague enough that completion becomes subjective.
3. Proof cases imply evidence that has not been recorded.
4. The tool attempts to infer context instead of accepting a supplied context report.
5. The README makes the tool sound like an autonomous agent manager instead of a handoff generator.

## Unit27 README Gate

Every public Unit27 repo should include a near-top `## Why Use It` section before setup details.

The section should answer:

1. Who should pick this up?
2. What immediate problem does it solve?
3. What concrete artifact does it produce?
4. Where does it stop?

For Handoff Engine, the answer is direct: use it when context exists but the agent work order still needs boundaries, acceptance checks, proof cases, and launch-gate guidance.
````

## FILE: README.md

PATH: README.md
EXTENSION: .md
PRIORITY: CORE
TOKENS: 1207

````markdown
# U27-S04 // Handoff Engine

[![CI](https://github.com/unit27research/unit27-handoff-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/unit27research/unit27-handoff-engine/actions/workflows/ci.yml)

Handoff Engine converts objectives and context summaries into agent-ready work packets.

```text
U27-S04
HANDOFF ENGINE

CLASS: SYSTEM
FUNCTION: Agent Handoff + Work Packet Generation
REF_ID: HANDOFF-ENGINE-01
```

## Release Status

`SOURCE_STATUS: PUBLIC_PACKAGE`
`ACCESS_STATUS: CLEARED_FOR_EXTERNAL_USE`

This repository is a released Unit27 field kit: visible, inspectable, and intended for orientation, testing, and practical use. Controlled protocol materials remain outside this source package.

It answers one narrow question:

> What exactly should the agent do with this context, under what constraints, and how will completion be checked?

## Why Use It

Use Handoff Engine after context has been prepared and before implementation begins, when an AI agent needs a precise work packet instead of a loose instruction.

It is useful when the objective is known, the relevant context has been gathered, and the next risk is drift: touching the wrong files, expanding scope, skipping acceptance checks, or claiming completion before proof exists.

Example:

```text
Problem: The agent has context, but the actual work order is still vague.
Result: Handoff Engine writes a handoff packet with objective, constraints, acceptance checks, proof cases, and launch-gate guidance.
```

## 60-Second Start

From this repo:

```bash
pip install -e .
handoff-engine demo
cat handoff-engine-demo/u27/HANDOFF_PACKET.md
```

On your own repo:

```bash
handoff-engine init
handoff-engine build \
  --objective "Add README usage section" \
  --context context_report.json \
  --allowed README.md \
  --constraint "Keep public claims inside recorded proof." \
  --acceptance "README includes a runnable command example." \
  --proof-case readme-usage-present
handoff-engine inspect u27/handoff.json
```

## What It Does

Handoff Engine writes:

1. `u27/handoff.json`
2. `u27/HANDOFF_PACKET.md`
3. `evals/proof_cases.json`

It is designed to feel like a deterministic agent handoff generator, not a project manager, code reviewer, or proof recorder.

## System Position

```text
Stack Engine -> Context Engine -> Knowledge Readiness -> Handoff Engine -> Eval Bench -> Proof Ledger -> Boundary Engine -> u27-check
```

Handoff Engine sits after Knowledge Readiness classification and before eval execution. It turns approved context into bounded work packets; it does not decide whether the project should exist, scan the repository, run the work, record proof, or certify the result.

## Dogfood Artifacts

This repository includes a Unit27 system-order dogfood pass against itself:

1. `u27/context_report.json`
2. `u27/context_manifest.md`
3. `u27/handoff.json`
4. `u27/HANDOFF_PACKET.md`
5. `u27/proof_ledger.json`
6. `u27/PROOF_PACKET.md`
7. `u27/BOUNDARY_REGISTER.md`

The launch-gate role is recorded as an applicability assessment. Handoff Engine is a CLI field kit, not a web launch surface, so no `u27-check` launch-pass claim is made.

## CLI

```bash
handoff-engine init
handoff-engine build --objective "Add README usage section"
handoff-engine inspect u27/handoff.json
handoff-engine demo
```

Build options:

```bash
handoff-engine build \
  --root . \
  --objective "Add README usage section" \
  --context context_report.json \
  --allowed README.md \
  --blocked .github/workflows/ci.yml \
  --constraint "Keep public claims inside recorded proof." \
  --acceptance "README includes a runnable command example." \
  --proof-case readme-usage-present \
  --boundary-note "Do not claim production readiness."
```

Exit codes:

```text
0 = success
2 = input or inspection error
```

## Artifact Shape

```text
objective -> context summary -> scope -> constraints -> acceptance checks -> proof cases -> handoff packet
```

The JSON file is the durable machine-readable work order. The Markdown packet is the reviewer-facing export. The proof cases give Proof Ledger a starter set of claims to record after implementation.

## Reliability

Handoff Engine is released as part of the Unit27 public tooling channel. CI verifies the unit test suite and wheel contents before changes are considered ready.

## What It Does Not Do

Handoff Engine does not:

1. Decide whether the project is worth building
2. Scan the whole repo for context
3. Run tests or demos
4. Record proof
5. Rewrite public claims
6. Perform launch QA
7. Replace Proof Ledger, Boundary Engine, or `u27-check`

## Verify

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
handoff-engine demo
handoff-engine inspect handoff-engine-demo/u27/handoff.json
```

## Acceptance

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m handoff_engine.cli demo --root examples/sample-project
PYTHONPATH=src python3 -m handoff_engine.cli inspect examples/sample-project/u27/handoff.json
python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/handoff-engine-wheel
python3 scripts/verify_wheel.py /tmp/handoff-engine-wheel/unit27_handoff_engine-0.1.0-py3-none-any.whl
```

## License

MIT
````

## FILE: pyproject.toml

PATH: pyproject.toml
EXTENSION: .toml
PRIORITY: SUPPORTING
TOKENS: 207

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "unit27-handoff-engine"
version = "0.1.0"
description = "Unit27 public field kit for generating agent-ready handoff packets from objectives and context."
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [
  { name = "Unit27 Research" }
]
keywords = ["ai", "agents", "cli", "handoff", "research-infrastructure", "unit27"]
classifiers = [
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.9",
  "License :: OSI Approved :: MIT License",
  "Environment :: Console",
  "Topic :: Software Development :: Documentation"
]

[project.scripts]
handoff-engine = "handoff_engine.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

## FILE: .github/workflows/ci.yml

PATH: .github/workflows/ci.yml
EXTENSION: .yml
PRIORITY: SUPPORTING
TOKENS: 174

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - name: Run tests
        run: PYTHONPATH=src python -m unittest discover -s tests
      - name: Install build tooling
        run: python -m pip install --upgrade pip setuptools wheel
      - name: Build wheel
        run: python -m pip wheel . --no-deps --no-build-isolation -w dist
      - name: Verify wheel
        run: python scripts/verify_wheel.py dist/unit27_handoff_engine-0.1.0-py3-none-any.whl
```

## FILE: evals/proof_cases.json

PATH: evals/proof_cases.json
EXTENSION: .json
PRIORITY: SUPPORTING
TOKENS: 488

```json
[
  {
    "claim": "Context Engine produced a context report and manifest for the handoff target.",
    "expected": "The context scan command exits 0 and writes inspectable context artifacts.",
    "id": "context-engine-scan",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "Handoff Engine produced a handoff packet from the recorded objective and context.",
    "expected": "The handoff build command exits 0 and writes handoff JSON plus a Markdown packet.",
    "id": "handoff-packet-build",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "The project test suite passes in the current local checkout.",
    "expected": "The configured test command exits 0 and stores stdout/stderr as evidence.",
    "id": "tests-pass",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "The primary CLI or demo command runs successfully.",
    "expected": "The smoke command exits 0 and produces inspectable output.",
    "id": "cli-smoke-test",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "The project can produce its expected build or package artifact.",
    "expected": "The build command exits 0 and stores build output as evidence.",
    "id": "package-builds",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "Boundary Engine reports no unsupported public claims for the README.",
    "expected": "The boundary scan exits 0 and writes a boundary register.",
    "id": "boundary-readme-scan",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "The launch-gate role is explicitly assessed for this repository.",
    "expected": "The assessment records whether u27-check is applicable before any launch-surface claim is made.",
    "id": "launch-gate-assessed",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  }
]
```

## FILE: examples/sample-project/README.md

PATH: examples/sample-project/README.md
EXTENSION: .md
PRIORITY: SUPPORTING
TOKENS: 17

```markdown
# Sample Project

This directory is used by Handoff Engine demo and acceptance commands.
```

## FILE: examples/sample-project/context_report.json

PATH: examples/sample-project/context_report.json
EXTENSION: .json
PRIORITY: SUPPORTING
TOKENS: 34

```json
{
  "files_considered": 4,
  "summary": "Demo context for a README usage update.",
  "total_tokens": 1200
}
```

## FILE: examples/sample-project/evals/proof_cases.json

PATH: examples/sample-project/evals/proof_cases.json
EXTENSION: .json
PRIORITY: SUPPORTING
TOKENS: 152

```json
[
  {
    "claim": "The handoff objective is satisfied: Add a concise usage section to the README.",
    "expected": "Evidence exists for `readme-usage-present` before the work is represented as complete.",
    "id": "readme-usage-present",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  },
  {
    "claim": "The handoff objective is satisfied: Add a concise usage section to the README.",
    "expected": "Evidence exists for `tests-pass` before the work is represented as complete.",
    "id": "tests-pass",
    "limits": [
      "This claim covers the recorded handoff objective only."
    ]
  }
]
```

## FILE: scripts/verify_wheel.py

PATH: scripts/verify_wheel.py
EXTENSION: .py
PRIORITY: SUPPORTING
TOKENS: 229

```python
"""Verify wheel contents for Unit27 Handoff Engine."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


REQUIRED = {
    "handoff_engine/__init__.py",
    "handoff_engine/cli.py",
    "handoff_engine/core.py",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_wheel.py PATH_TO_WHEEL", file=sys.stderr)
        return 2

    wheel = Path(sys.argv[1])
    if not wheel.exists():
        print(f"wheel not found: {wheel}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())

    missing = sorted(required for required in REQUIRED if not any(name.endswith(required) for name in names))
    if missing:
        print("missing wheel contents:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("wheel contents verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## FILE: src/handoff_engine/__init__.py

PATH: src/handoff_engine/__init__.py
EXTENSION: .py
PRIORITY: CORE
TOKENS: 18

```python
"""Unit27 Handoff Engine."""

__version__ = "0.1.0"
```

## FILE: src/handoff_engine/cli.py

PATH: src/handoff_engine/cli.py
EXTENSION: .py
PRIORITY: CORE
TOKENS: 1060

```python
"""Command-line interface for Unit27 Handoff Engine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from handoff_engine.core import HandoffInputs, build_handoff, create_demo, write_handoff


def add_common_build_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="Project root for generated artifacts.")
    parser.add_argument("--objective", help="Objective the agent should complete.")
    parser.add_argument("--context", help="Optional Context Engine JSON report.")
    parser.add_argument("--allowed", action="append", default=[], help="Allowed file or glob. Repeatable.")
    parser.add_argument("--blocked", action="append", default=[], help="Blocked file or glob. Repeatable.")
    parser.add_argument("--constraint", action="append", default=[], help="Work constraint. Repeatable.")
    parser.add_argument("--acceptance", action="append", default=[], help="Acceptance check. Repeatable.")
    parser.add_argument("--proof-case", action="append", default=[], help="Proof case label. Repeatable.")
    parser.add_argument("--boundary-note", action="append", default=[], help="Boundary note. Repeatable.")


def command_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    (root / "u27").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    print(f"Initialized handoff workspace: {root}")
    return 0


def command_build(args: argparse.Namespace) -> int:
    if not args.objective or not args.objective.strip():
        print("handoff-engine: --objective is required for build", file=sys.stderr)
        return 2

    try:
        handoff = build_handoff(
            HandoffInputs(
                objective=args.objective,
                context_path=args.context,
                allowed_files=tuple(args.allowed),
                blocked_files=tuple(args.blocked),
                constraints=tuple(args.constraint),
                acceptance_checks=tuple(args.acceptance),
                proof_cases=tuple(args.proof_case),
                boundary_notes=tuple(args.boundary_note),
            )
        )
    except ValueError as exc:
        print(f"handoff-engine: {exc}", file=sys.stderr)
        return 2

    paths = write_handoff(args.root, handoff)
    print(f"Handoff packet written: {paths['packet']}")
    print(f"Handoff JSON written: {paths['handoff']}")
    print(f"Proof cases written: {paths['proof_cases']}")
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.exists():
        print(f"handoff-engine: handoff file not found: {path}", file=sys.stderr)
        return 2

    try:
        handoff = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"handoff-engine: invalid handoff JSON: {path}: {exc}", file=sys.stderr)
        return 2

    print(f"Objective: {handoff.get('objective', 'unknown')}")
    print(f"System Class: {handoff.get('system_class', 'unknown')}")
    print(f"Proof Cases: {len(handoff.get('proof_cases', []))}")
    print(f"Launch Gate: {handoff.get('launch_gate', {}).get('tool', 'unknown')}")
    return 0


def command_demo(args: argparse.Namespace) -> int:
    root = Path(args.root)
    paths = create_demo(root)
    print(f"Demo handoff packet written: {paths['packet']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="handoff-engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create handoff artifact directories.")
    init_parser.add_argument("--root", default=".", help="Project root for generated artifacts.")
    init_parser.set_defaults(func=command_init)

    build_parser_ = subparsers.add_parser("build", help="Build a handoff packet.")
    add_common_build_args(build_parser_)
    build_parser_.set_defaults(func=command_build)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a handoff JSON file.")
    inspect_parser.add_argument("path", nargs="?", default="u27/handoff.json", help="Path to handoff JSON.")
    inspect_parser.set_defaults(func=command_inspect)

    demo_parser = subparsers.add_parser("demo", help="Create a demo handoff project.")
    demo_parser.add_argument("--root", default="handoff-engine-demo", help="Demo root path.")
    demo_parser.set_defaults(func=command_demo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

## FILE: src/handoff_engine/core.py

PATH: src/handoff_engine/core.py
EXTENSION: .py
PRIORITY: CORE
TOKENS: 2367

```python
"""Core handoff packet generation for Unit27 Handoff Engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "0.1"

PROOF_CASE_TEMPLATES = {
    "context-engine-scan": (
        "Context Engine produced a context report and manifest for the handoff target.",
        "The context scan command exits 0 and writes inspectable context artifacts.",
    ),
    "handoff-packet-build": (
        "Handoff Engine produced a handoff packet from the recorded objective and context.",
        "The handoff build command exits 0 and writes handoff JSON plus a Markdown packet.",
    ),
    "tests-pass": (
        "The project test suite passes in the current local checkout.",
        "The configured test command exits 0 and stores stdout/stderr as evidence.",
    ),
    "cli-smoke-test": (
        "The primary CLI or demo command runs successfully.",
        "The smoke command exits 0 and produces inspectable output.",
    ),
    "package-builds": (
        "The project can produce its expected build or package artifact.",
        "The build command exits 0 and stores build output as evidence.",
    ),
    "boundary-readme-scan": (
        "Boundary Engine reports no unsupported public claims for the README.",
        "The boundary scan exits 0 and writes a boundary register.",
    ),
    "launch-gate-assessed": (
        "The launch-gate role is explicitly assessed for this repository.",
        "The assessment records whether u27-check is applicable before any launch-surface claim is made.",
    ),
    "implementation-complete": (
        "The requested handoff objective has been implemented within the allowed scope.",
        "Evidence exists before the work is represented as complete.",
    ),
    "handoff-reviewed": (
        "The generated handoff packet has been reviewed for scope, proof, and boundary fit.",
        "A reviewer can inspect the packet and confirm the work order is bounded.",
    ),
}


@dataclass(frozen=True)
class HandoffInputs:
    objective: str
    context_path: str | None = None
    allowed_files: tuple[str, ...] = field(default_factory=tuple)
    blocked_files: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)
    acceptance_checks: tuple[str, ...] = field(default_factory=tuple)
    proof_cases: tuple[str, ...] = field(default_factory=tuple)
    boundary_notes: tuple[str, ...] = field(default_factory=tuple)


def normalize_items(items: Iterable[str] | None) -> list[str]:
    if not items:
        return []
    normalized: list[str] = []
    for item in items:
        value = item.strip()
        if value and value not in normalized:
            normalized.append(value)
    return normalized


def slugify(value: str) -> str:
    chars: list[str] = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True
    slug = "".join(chars).strip("-")
    return slug or "handoff"


def load_context_summary(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {
            "source": None,
            "summary": "No context report supplied.",
            "files_considered": None,
            "token_count": None,
        }

    context_path = Path(path)
    try:
        raw = json.loads(context_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON context report: {context_path}") from exc

    files_considered = raw.get("files_considered")
    if files_considered is None:
        files = raw.get("files")
        if isinstance(files, list):
            files_considered = len(files)

    token_count = raw.get("total_tokens", raw.get("token_count"))
    summary = raw.get("summary") or raw.get("description") or "Context report loaded."

    return {
        "source": str(context_path),
        "summary": str(summary),
        "files_considered": files_considered,
        "token_count": token_count,
    }


def default_proof_cases(objective: str, proof_cases: Iterable[str] | None = None) -> list[dict[str, Any]]:
    requested = normalize_items(proof_cases)
    if not requested:
        requested = ["implementation-complete", "tests-pass", "handoff-reviewed"]

    cases: list[dict[str, Any]] = []
    for case in requested:
        case_id = slugify(case)
        claim, expected = PROOF_CASE_TEMPLATES.get(
            case_id,
            (
                f"The handoff objective is satisfied: {objective}",
                f"Evidence exists for `{case}` before the work is represented as complete.",
            ),
        )
        cases.append(
            {
                "id": case_id,
                "claim": claim,
                "expected": expected,
                "limits": ["This claim covers the recorded handoff objective only."],
            }
        )
    return cases


def build_handoff(inputs: HandoffInputs, generated_at: str | None = None) -> dict[str, Any]:
    objective = inputs.objective.strip()
    if not objective:
        raise ValueError("Objective is required.")

    timestamp = generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    allowed = normalize_items(inputs.allowed_files)
    blocked = normalize_items(inputs.blocked_files)
    constraints = normalize_items(inputs.constraints)
    acceptance = normalize_items(inputs.acceptance_checks)
    boundary = normalize_items(inputs.boundary_notes)
    proof = default_proof_cases(objective, inputs.proof_cases)

    if not acceptance:
        acceptance = [
            "The requested change is implemented within the allowed scope.",
            "Relevant tests, demos, or inspections are recorded before completion is claimed.",
            "Public-facing language stays inside recorded proof.",
        ]

    if not constraints:
        constraints = [
            "Do not expand scope without an updated handoff packet.",
            "Do not modify blocked files.",
            "Do not claim behavior that has not been checked.",
        ]

    if not boundary:
        boundary = [
            "This packet directs work; it does not certify completion.",
            "Proof must be recorded separately before public claims are made.",
        ]

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": timestamp,
        "system_class": "U27-S04",
        "objective": objective,
        "context": load_context_summary(inputs.context_path),
        "scope": {
            "allowed_files": allowed,
            "blocked_files": blocked,
        },
        "constraints": constraints,
        "acceptance_checks": acceptance,
        "proof_cases": proof,
        "boundary_notes": boundary,
        "launch_gate": {
            "recommended": True,
            "tool": "u27-check",
            "reason": "Run after implementation and public-surface updates, before a real user reaches the launch path.",
        },
    }


def render_list(items: list[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def render_packet(handoff: dict[str, Any]) -> str:
    scope = handoff["scope"]
    context = handoff["context"]
    proof_cases = handoff["proof_cases"]
    proof_lines = "\n".join(f"- `{case['id']}`: {case['expected']}" for case in proof_cases)

    return f"""# Handoff Packet

`SOURCE_STATUS: PUBLIC_PACKAGE`
`ACCESS_STATUS: CLEARED_FOR_EXTERNAL_USE`

Generated: {handoff['generated_at']}
System Class: {handoff['system_class']}

## Objective

{handoff['objective']}

## Context

- Source: {context['source'] or 'none supplied'}
- Summary: {context['summary']}
- Files considered: {context['files_considered'] if context['files_considered'] is not None else 'unknown'}
- Token count: {context['token_count'] if context['token_count'] is not None else 'unknown'}

## Allowed Files

{render_list(scope['allowed_files'], 'No explicit allowed-file list supplied.')}

## Blocked Files

{render_list(scope['blocked_files'], 'No explicit blocked-file list supplied.')}

## Constraints

{render_list(handoff['constraints'], 'No constraints supplied.')}

## Acceptance Checks

{render_list(handoff['acceptance_checks'], 'No acceptance checks supplied.')}

## Proof Cases

{proof_lines}

## Boundary Notes

{render_list(handoff['boundary_notes'], 'No boundary notes supplied.')}

## Launch Gate

Run `{handoff['launch_gate']['tool']}` after implementation and public-surface updates.

Reason: {handoff['launch_gate']['reason']}
"""


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_handoff(root: str | Path, handoff: dict[str, Any]) -> dict[str, Path]:
    root_path = Path(root)
    handoff_path = root_path / "u27" / "handoff.json"
    packet_path = root_path / "u27" / "HANDOFF_PACKET.md"
    proof_cases_path = root_path / "evals" / "proof_cases.json"

    write_json(handoff_path, handoff)
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(render_packet(handoff), encoding="utf-8")
    write_json(proof_cases_path, handoff["proof_cases"])

    return {
        "handoff": handoff_path,
        "packet": packet_path,
        "proof_cases": proof_cases_path,
    }


def create_demo(root: str | Path) -> dict[str, Path]:
    root_path = Path(root)
    context_path = root_path / "context_report.json"
    context_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(
        context_path,
        {
            "summary": "Demo context for a README usage update.",
            "files_considered": 4,
            "total_tokens": 1200,
        },
    )
    handoff = build_handoff(
        HandoffInputs(
            objective="Add a concise usage section to the README.",
            context_path=str(context_path),
            allowed_files=("README.md", "tests/test_cli.py"),
            blocked_files=(".github/workflows/ci.yml",),
            constraints=("Keep public claims inside recorded proof.",),
            acceptance_checks=("README includes a runnable command example.", "Tests still pass."),
            proof_cases=("readme-usage-present", "tests-pass"),
            boundary_notes=("Do not claim production readiness.",),
        ),
        generated_at="2026-01-01T00:00:00+00:00",
    )
    return write_handoff(root_path, handoff)
```

## FILE: tests/test_cli.py

PATH: tests/test_cli.py
EXTENSION: .py
PRIORITY: SUPPORTING
TOKENS: 809

```python
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from handoff_engine.cli import main


class HandoffCliTests(unittest.TestCase):
    def run_cli(self, args):
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_init_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, stdout, stderr = self.run_cli(["init", "--root", tmp])

            self.assertEqual(code, 0, stderr)
            self.assertIn("Initialized handoff workspace", stdout)
            self.assertTrue((Path(tmp) / "u27").exists())
            self.assertTrue((Path(tmp) / "evals").exists())

    def test_build_requires_objective(self):
        code, stdout, stderr = self.run_cli(["build"])

        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("--objective is required", stderr)

    def test_build_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, stdout, stderr = self.run_cli(
                [
                    "build",
                    "--root",
                    tmp,
                    "--objective",
                    "Add usage docs.",
                    "--allowed",
                    "README.md",
                    "--blocked",
                    ".github/workflows/ci.yml",
                    "--constraint",
                    "Keep claims bounded.",
                    "--acceptance",
                    "README includes an example.",
                    "--proof-case",
                    "readme-usage-present",
                ]
            )

            self.assertEqual(code, 0, stderr)
            self.assertIn("Handoff packet written", stdout)
            handoff = json.loads((Path(tmp) / "u27" / "handoff.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff["objective"], "Add usage docs.")
            self.assertEqual(handoff["scope"]["allowed_files"], ["README.md"])
            self.assertEqual(handoff["proof_cases"][0]["id"], "readme-usage-present")

    def test_build_rejects_invalid_context_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            context = Path(tmp) / "bad.json"
            context.write_text("{bad", encoding="utf-8")

            code, stdout, stderr = self.run_cli(
                ["build", "--root", tmp, "--objective", "Use context.", "--context", str(context)]
            )

            self.assertEqual(code, 2)
            self.assertEqual(stdout, "")
            self.assertIn("Invalid JSON context report", stderr)

    def test_inspect_reports_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.run_cli(["build", "--root", tmp, "--objective", "Inspect this.", "--proof-case", "tests-pass"])

            code, stdout, stderr = self.run_cli(["inspect", str(Path(tmp) / "u27" / "handoff.json")])

            self.assertEqual(code, 0, stderr)
            self.assertIn("Objective: Inspect this.", stdout)
            self.assertIn("Proof Cases: 1", stdout)

    def test_inspect_missing_file_fails(self):
        code, stdout, stderr = self.run_cli(["inspect", "missing.json"])

        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("handoff file not found", stderr)

    def test_demo_writes_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            demo_root = Path(tmp) / "demo"
            code, stdout, stderr = self.run_cli(["demo", "--root", str(demo_root)])

            self.assertEqual(code, 0, stderr)
            self.assertIn("Demo handoff packet written", stdout)
            self.assertTrue((demo_root / "u27" / "HANDOFF_PACKET.md").exists())


if __name__ == "__main__":
    unittest.main()
```

## FILE: tests/test_core.py

PATH: tests/test_core.py
EXTENSION: .py
PRIORITY: SUPPORTING
TOKENS: 694

```python
import json
import tempfile
import unittest
from pathlib import Path

from handoff_engine.core import HandoffInputs, build_handoff, create_demo, write_handoff


class HandoffCoreTests(unittest.TestCase):
    def test_build_handoff_requires_objective(self):
        with self.assertRaisesRegex(ValueError, "Objective is required"):
            build_handoff(HandoffInputs(objective=" "))

    def test_build_handoff_creates_default_packet_shape(self):
        handoff = build_handoff(
            HandoffInputs(objective="Update README usage."),
            generated_at="2026-01-01T00:00:00+00:00",
        )

        self.assertEqual(handoff["schema_version"], "0.1")
        self.assertEqual(handoff["system_class"], "U27-S04")
        self.assertEqual(handoff["objective"], "Update README usage.")
        self.assertEqual(handoff["context"]["summary"], "No context report supplied.")
        self.assertEqual(handoff["launch_gate"]["tool"], "u27-check")
        self.assertEqual(
            [case["id"] for case in handoff["proof_cases"]],
            ["implementation-complete", "tests-pass", "handoff-reviewed"],
        )
        self.assertEqual(
            handoff["proof_cases"][1]["claim"],
            "The project test suite passes in the current local checkout.",
        )

    def test_build_handoff_loads_context_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            context = Path(tmp) / "context_report.json"
            context.write_text(
                json.dumps({"summary": "Repo scan complete.", "files_considered": 7, "total_tokens": 2048}),
                encoding="utf-8",
            )

            handoff = build_handoff(
                HandoffInputs(objective="Refine CLI help.", context_path=str(context)),
                generated_at="2026-01-01T00:00:00+00:00",
            )

        self.assertEqual(handoff["context"]["summary"], "Repo scan complete.")
        self.assertEqual(handoff["context"]["files_considered"], 7)
        self.assertEqual(handoff["context"]["token_count"], 2048)

    def test_write_handoff_writes_expected_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            handoff = build_handoff(
                HandoffInputs(objective="Add tests.", proof_cases=("tests-pass",)),
                generated_at="2026-01-01T00:00:00+00:00",
            )
            paths = write_handoff(tmp, handoff)

            self.assertTrue(paths["handoff"].exists())
            self.assertTrue(paths["packet"].exists())
            self.assertTrue(paths["proof_cases"].exists())
            packet = paths["packet"].read_text(encoding="utf-8")
            self.assertIn("# Handoff Packet", packet)
            self.assertIn("Add tests.", packet)

    def test_create_demo_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = create_demo(tmp)
            handoff = json.loads(paths["handoff"].read_text(encoding="utf-8"))

        self.assertEqual(handoff["generated_at"], "2026-01-01T00:00:00+00:00")
        self.assertEqual(handoff["proof_cases"][0]["id"], "readme-usage-present")


if __name__ == "__main__":
    unittest.main()
```
