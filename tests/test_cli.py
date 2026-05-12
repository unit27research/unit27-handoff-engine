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
