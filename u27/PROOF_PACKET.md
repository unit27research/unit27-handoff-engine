# Proof Packet

Project: unit27-handoff-engine
Generated: 2026-05-12T02:01:35+00:00

## Verified Claims

- The project test suite passes in the current local checkout.
  - Case: `tests-pass`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m unittest discover -s tests`
  - Evidence: `u27/evidence/run-0004.txt`

- The primary CLI or demo command runs successfully.
  - Case: `cli-smoke-test`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m handoff_engine.cli demo --root /tmp/handoff-engine-proof-demo`
  - Evidence: `u27/evidence/run-0002.txt`

- The project can produce its expected build or package artifact.
  - Case: `package-builds`
  - Command: `/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/handoff-engine-proof-wheel`
  - Evidence: `u27/evidence/run-0003.txt`

## Open Failures

- No failing, blocked, or regression runs are recorded.

## Known Limits
- This claim covers the recorded local test command only.
- This smoke test does not prove every CLI option or integration path.
- This claim covers local artifact creation, not distribution or release state.

## Case Inventory
- `cli-smoke-test`: pass - The primary CLI or demo command runs successfully.
- `package-builds`: pass - The project can produce its expected build or package artifact.
- `tests-pass`: pass - The project test suite passes in the current local checkout.
