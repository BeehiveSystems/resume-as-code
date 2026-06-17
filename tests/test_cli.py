from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class ResumeCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        return subprocess.run(
            [sys.executable, "-m", "resume_as_code", *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validate_yaml_example(self) -> None:
        result = self.run_cli("validate", "examples/jane-doe.yaml")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Valid resume spec for Jane Doe", result.stdout)

    def test_render_json_example(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "resume.html"
            result = self.run_cli("render", "examples/jane-doe.json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("Jane Doe", html)
            self.assertIn("Staff Product Engineer", html)
            self.assertIn("Senior Platform Engineer", html)
            self.assertIn("Release Graph", html)
            self.assertIn('id="resume-pages"', html)
            self.assertIn("page--source", html)
            self.assertIn("initializePagination", html)

    def test_init_writes_yaml_starter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "starter.yaml"
            result = self.run_cli("init", "--format", "yaml", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            content = output.read_text(encoding="utf-8")
            self.assertIn('name: "Jane Doe"', content)
            self.assertIn("experience:", content)
            self.assertIn("positions:", content)

    def test_render_theme_override_uses_slate_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "resume.html"
            result = self.run_cli(
                "render",
                "examples/jane-doe.json",
                "--theme",
                "slate",
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("--accent: #2f5d62;", html)

    def test_render_all_themes(self) -> None:
        themes = ["classic", "slate", "compact", "technical", "mono"]
        with tempfile.TemporaryDirectory() as tmpdir:
            for theme in themes:
                output = Path(tmpdir) / f"resume-{theme}.html"
                result = self.run_cli(
                    "render",
                    "examples/jane-doe.json",
                    "--theme",
                    theme,
                    "--output",
                    str(output),
                )
                self.assertEqual(result.returncode, 0, f"{theme}: {result.stderr}")
                html = output.read_text(encoding="utf-8")
                self.assertIn("Jane Doe", html)
                self.assertIn(f"theme-{theme}", html)

    def test_render_experience_with_multiple_positions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = Path(tmpdir) / "resume.json"
            output = Path(tmpdir) / "resume.html"
            spec.write_text(
                """
{
  "basics": {
    "name": "Jane Doe"
  },
  "experience": [
    {
      "company": "Credit.com",
      "location": "Remote",
      "start": "Mar. 2020",
      "end": "Present",
      "positions": [
        {
          "title": "Senior DevOps Engineer",
          "start": "Oct. 2021",
          "end": "Present",
          "highlights": [
            "Designed GitLab CI pipelines."
          ]
        },
        {
          "title": "Linux Systems Engineer",
          "start": "Mar. 2020",
          "end": "Oct. 2021",
          "highlights": [
            "Automated PCI remediation."
          ]
        }
      ]
    }
  ]
}
""".strip(),
                encoding="utf-8",
            )
            result = self.run_cli("render", str(spec), "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            self.assertIn("Credit.com", html)
            self.assertIn("Senior DevOps Engineer", html)
            self.assertIn("Linux Systems Engineer", html)
            self.assertIn("Mar. 2020 - Present", html)

    def test_themes_lists_all_built_ins(self) -> None:
        result = self.run_cli("themes")
        self.assertEqual(result.returncode, 0, result.stderr)
        for theme in ["classic", "slate", "compact", "technical", "mono"]:
            self.assertIn(theme, result.stdout)

    def test_init_prints_next_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "starter.yaml"
            result = self.run_cli("init", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"Next: resume-as-code render {output}", result.stdout)

    def test_validate_emits_warnings_for_sparse_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = Path(tmpdir) / "sparse.json"
            spec.write_text('{"basics": {"name": "Jane Doe"}}', encoding="utf-8")
            result = self.run_cli("validate", str(spec))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Valid resume spec for Jane Doe", result.stdout)
            self.assertIn("basics.email is empty", result.stderr)

    def test_validate_rejects_missing_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = Path(tmpdir) / "broken.json"
            spec.write_text('{"basics": {"role": "Engineer"}}', encoding="utf-8")
            result = self.run_cli("validate", str(spec))
            self.assertEqual(result.returncode, 1)
            self.assertIn("`basics.name` is required", result.stderr)

    def test_validate_rejects_position_without_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            spec = Path(tmpdir) / "broken.json"
            spec.write_text(
                """
{
  "basics": {
    "name": "Jane Doe"
  },
  "experience": [
    {
      "company": "Credit.com",
      "positions": [
        {}
      ]
    }
  ]
}
""".strip(),
                encoding="utf-8",
            )
            result = self.run_cli("validate", str(spec))
            self.assertEqual(result.returncode, 1)
            self.assertIn("positions[1].title", result.stderr)


if __name__ == "__main__":
    unittest.main()
