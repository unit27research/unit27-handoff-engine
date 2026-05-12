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
Stack Engine -> Context Engine -> Handoff Engine -> Proof Ledger -> Boundary Engine -> u27-check
```

Handoff Engine sits after context preparation and before proof recording. It does not decide whether the project should exist, scan the repository, run the work, or certify the result.

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
