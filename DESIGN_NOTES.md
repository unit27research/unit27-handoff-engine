# Handoff Engine Design Notes

`U27-S04 // HANDOFF ENGINE`

Handoff Engine exists to convert prepared context and a known objective into a bounded agent work packet.

## System Role

```text
Stack Engine -> Context Engine -> Handoff Engine -> Eval Bench -> Proof Ledger -> Boundary Engine -> u27-check
```

Stack Engine shapes the work. Context Engine prepares the material. Handoff Engine states exactly what the agent should do with that material. Eval Bench runs declared checks. Proof Ledger records what happened after the work. Boundary Engine checks whether public language stays inside proof. `u27-check` gates the first user path.

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
