# Proof Packet

Project: unit27-handoff-engine
Generated: 2026-05-12T16:55:06+00:00

## Verified Claims

- Context Engine produced a context report and manifest for the handoff target.
  - Case: `context-engine-scan`
  - Command: `/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m context_engine.cli scan . --output u27/context_manifest.md --report u27/context_report.json --max-tokens 50000 --exact-tokens --exclude 'u27/*' --exclude 'examples/sample-project/u27/*' --exclude 'build/*' --exclude '*.egg-info/*'`
  - Evidence: `u27/evidence/run-0001.txt`

- Handoff Engine produced a handoff packet from the recorded objective and context.
  - Case: `handoff-packet-build`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m handoff_engine.cli build --objective 'Dogfood the Unit27 system order on Handoff Engine and preserve the generated context, handoff, proof, boundary, and launch-gate artifacts.' --context u27/context_report.json --allowed README.md --allowed DESIGN_NOTES.md --allowed src/handoff_engine/core.py --allowed src/handoff_engine/cli.py --allowed tests/test_core.py --allowed tests/test_cli.py --allowed u27/context_report.json --allowed u27/context_manifest.md --allowed u27/HANDOFF_PACKET.md --allowed u27/handoff.json --allowed u27/proof_ledger.json --allowed u27/PROOF_PACKET.md --allowed u27/BOUNDARY_REGISTER.md --blocked .github/workflows/ci.yml --constraint 'Keep public claims inside recorded proof.' --constraint 'Do not expand Handoff Engine into Proof Ledger, Boundary Engine, Context Engine, or launch QA.' --acceptance 'Context Engine produces u27/context_report.json and u27/context_manifest.md for this repo.' --acceptance 'Handoff Engine produces u27/handoff.json and u27/HANDOFF_PACKET.md from the context report.' --acceptance 'Proof Ledger records passing tests, CLI smoke, package build, and boundary scan evidence.' --acceptance 'Boundary Engine reports unsupported=0 for README.md.' --acceptance 'u27-check launch gate is explicitly assessed for CLI applicability.' --proof-case context-engine-scan --proof-case handoff-packet-build --proof-case tests-pass --proof-case cli-smoke-test --proof-case package-builds --proof-case boundary-readme-scan --proof-case launch-gate-assessed --boundary-note 'This dogfood packet proves the toolchain sequence for this repo only.' --boundary-note 'u27-check is a launch-surface gate; CLI-only repos may record it as not applicable rather than force a web-app check.'`
  - Evidence: `u27/evidence/run-0002.txt`

- The project test suite passes in the current local checkout.
  - Case: `tests-pass`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m unittest discover -s tests`
  - Evidence: `u27/evidence/run-0003.txt`

- The primary CLI or demo command runs successfully.
  - Case: `cli-smoke-test`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m handoff_engine.cli demo --root /tmp/handoff-engine-dogfood-demo`
  - Evidence: `u27/evidence/run-0004.txt`

- The project can produce its expected build or package artifact.
  - Case: `package-builds`
  - Command: `/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/handoff-engine-dogfood-wheel`
  - Evidence: `u27/evidence/run-0005.txt`

- Boundary Engine reports no unsupported public claims for the README.
  - Case: `boundary-readme-scan`
  - Command: `/usr/bin/env PYTHONPATH=../unit27-boundary-engine/src python3 -m boundary_engine.cli scan README.md --proof u27/proof_ledger.json`
  - Evidence: `u27/evidence/run-0006.txt`

- The launch-gate role is explicitly assessed for this repository.
  - Case: `launch-gate-assessed`
  - Command: `python3 -c 'print('"'"'u27-check launch-gate assessment: not applicable for unit27-handoff-engine because this repository is a CLI field kit, not a web/product launch surface. No launch-pass claim is made.'"'"')'`
  - Evidence: `u27/evidence/run-0007.txt`

## Open Failures

- No failing, blocked, or regression runs are recorded.

## Known Limits
- This claim covers the recorded handoff objective only.

## Case Inventory
- `boundary-readme-scan`: pass - Boundary Engine reports no unsupported public claims for the README.
- `cli-smoke-test`: pass - The primary CLI or demo command runs successfully.
- `context-engine-scan`: pass - Context Engine produced a context report and manifest for the handoff target.
- `handoff-packet-build`: pass - Handoff Engine produced a handoff packet from the recorded objective and context.
- `launch-gate-assessed`: pass - The launch-gate role is explicitly assessed for this repository.
- `package-builds`: pass - The project can produce its expected build or package artifact.
- `tests-pass`: pass - The project test suite passes in the current local checkout.
