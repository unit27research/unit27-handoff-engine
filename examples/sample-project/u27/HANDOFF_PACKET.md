# Handoff Packet

`SOURCE_STATUS: PUBLIC_PACKAGE`
`ACCESS_STATUS: CLEARED_FOR_EXTERNAL_USE`

Generated: 2026-01-01T00:00:00+00:00
Release Class: U27-S06

## Objective

Add a concise usage section to the README.

## Context

- Source: examples/sample-project/context_report.json
- Summary: Demo context for a README usage update.
- Files considered: 4
- Token count: 1200

## Allowed Files

- README.md
- tests/test_cli.py

## Blocked Files

- .github/workflows/ci.yml

## Constraints

- Keep public claims inside recorded proof.

## Acceptance Checks

- README includes a runnable command example.
- Tests still pass.

## Proof Cases

- `readme-usage-present`: Evidence exists for `readme-usage-present` before the work is represented as complete.
- `tests-pass`: Evidence exists for `tests-pass` before the work is represented as complete.

## Boundary Notes

- Do not claim production readiness.

## Launch Gate

Run `u27-check` after implementation and public-surface updates.

Reason: Run after implementation and public-surface updates, before a real user reaches the launch path.
