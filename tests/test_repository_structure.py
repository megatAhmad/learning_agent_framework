from __future__ import annotations

import json
import unittest
from pathlib import Path


class RepositoryStructureTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_notebook_counts(self) -> None:
        learner = sorted((self.repo_root / "notebooks").glob("*.ipynb"))
        solutions = sorted((self.repo_root / "solutions").glob("*.ipynb"))
        supplemental_learner = sorted((self.repo_root / "notebooks" / "supplemental").glob("*.ipynb"))
        supplemental_solutions = sorted((self.repo_root / "solutions" / "supplemental").glob("*.ipynb"))
        self.assertEqual(len(learner), 15)
        self.assertEqual(len(solutions), 15)
        self.assertEqual(len(supplemental_learner), 6)
        self.assertEqual(len(supplemental_solutions), 6)

    def test_generated_notebook_has_required_heading(self) -> None:
        notebook_path = self.repo_root / "notebooks" / "01_setup_and_environment.ipynb"
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        markdown = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell.get("cell_type") == "markdown"
        )
        self.assertIn("## Part 3: Hands-On Exercises", markdown)
        self.assertIn("## Part 4: Solutions & Discussion", markdown)

    def test_docs_exist(self) -> None:
        expected = [
            self.repo_root / "SETUP.md",
            self.repo_root / "docs" / "depth_expansion_plan.md",
            self.repo_root / "docs" / "llm_providers.md",
            self.repo_root / "docs" / "troubleshooting.md",
            self.repo_root / "docs" / "glossary.md",
            self.repo_root / "docs" / "progress_tracker.md",
        ]
        for path in expected:
            self.assertTrue(path.exists(), f"missing {path}")

    def test_supplemental_notebook_has_required_heading(self) -> None:
        notebook_path = (
            self.repo_root / "notebooks" / "supplemental" / "16_intermediate_tool_reasoning_and_schema_design.ipynb"
        )
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        markdown = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell.get("cell_type") == "markdown"
        )
        self.assertIn("## Part 3: Hands-On Exercises", markdown)
        self.assertIn("## Reflection & Next Experiments", markdown)


if __name__ == "__main__":
    unittest.main()
