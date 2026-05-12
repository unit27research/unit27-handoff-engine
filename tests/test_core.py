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
        self.assertEqual(handoff["release_class"], "U27-S04")
        self.assertEqual(handoff["objective"], "Update README usage.")
        self.assertEqual(handoff["context"]["summary"], "No context report supplied.")
        self.assertEqual(handoff["launch_gate"]["tool"], "u27-check")
        self.assertEqual(
            [case["id"] for case in handoff["proof_cases"]],
            ["implementation-complete", "tests-pass", "handoff-reviewed"],
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
