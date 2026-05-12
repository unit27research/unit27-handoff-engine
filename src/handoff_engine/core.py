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
