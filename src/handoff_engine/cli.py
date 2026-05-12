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
    print(f"Release Class: {handoff.get('release_class', 'unknown')}")
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
