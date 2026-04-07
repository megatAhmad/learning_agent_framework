#!/usr/bin/env python3
"""Structural validation for the course notebooks and support files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
SOLUTIONS_DIR = REPO_ROOT / "solutions"
SUPPLEMENTAL_NOTEBOOKS_DIR = NOTEBOOKS_DIR / "supplemental"
SUPPLEMENTAL_SOLUTIONS_DIR = SOLUTIONS_DIR / "supplemental"

EXPECTED_NOTEBOOK_COUNT = 15
EXPECTED_SUPPLEMENTAL_NOTEBOOK_COUNT = 6
REQUIRED_MARKDOWN_HEADINGS = [
    "# Step",
    "## Learning Objectives",
    "## Prerequisites",
    "## Table of Contents",
    "## Setup & Imports",
    "## Part 1: Introduction",
    "## Part 2: Core Implementation",
    "## Part 3: Hands-On Exercises",
    "## Part 4: Solutions & Discussion",
    "## Part 5: Best Practices & Tips",
    "## Summary & Key Takeaways",
    "## Additional Resources",
]


def load_notebook(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_text(notebook: dict) -> str:
    chunks: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = cell.get("source", [])
            if isinstance(source, str):
                chunks.append(source)
            else:
                chunks.append("".join(source))
    return "\n".join(chunks)


def validate_notebook(path: Path) -> list[str]:
    notebook = load_notebook(path)
    errors: list[str] = []

    if notebook.get("nbformat") != 4:
        errors.append("nbformat must be 4")
    if "metadata" not in notebook:
        errors.append("missing metadata")

    md = markdown_text(notebook)
    for heading in REQUIRED_MARKDOWN_HEADINGS:
        if heading not in md:
            errors.append(f"missing heading: {heading}")

    if len(notebook.get("cells", [])) < 10:
        errors.append("expected at least 10 cells")

    return errors


def main() -> int:
    failures: list[str] = []

    learner = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    solutions = sorted(SOLUTIONS_DIR.glob("*.ipynb"))
    supplemental_learner = sorted(SUPPLEMENTAL_NOTEBOOKS_DIR.glob("*.ipynb"))
    supplemental_solutions = sorted(SUPPLEMENTAL_SOLUTIONS_DIR.glob("*.ipynb"))

    if len(learner) != EXPECTED_NOTEBOOK_COUNT:
        failures.append(
            f"expected {EXPECTED_NOTEBOOK_COUNT} learner notebooks, found {len(learner)}"
        )
    if len(solutions) != EXPECTED_NOTEBOOK_COUNT:
        failures.append(
            f"expected {EXPECTED_NOTEBOOK_COUNT} solution notebooks, found {len(solutions)}"
        )
    if len(supplemental_learner) != EXPECTED_SUPPLEMENTAL_NOTEBOOK_COUNT:
        failures.append(
            f"expected {EXPECTED_SUPPLEMENTAL_NOTEBOOK_COUNT} supplemental learner notebooks, found {len(supplemental_learner)}"
        )
    if len(supplemental_solutions) != EXPECTED_SUPPLEMENTAL_NOTEBOOK_COUNT:
        failures.append(
            f"expected {EXPECTED_SUPPLEMENTAL_NOTEBOOK_COUNT} supplemental solution notebooks, found {len(supplemental_solutions)}"
        )

    for path in learner + solutions + supplemental_learner + supplemental_solutions:
        errors = validate_notebook(path)
        if errors:
            failures.append(f"{path.relative_to(REPO_ROOT)}: {', '.join(errors)}")

    required_paths = [
        REPO_ROOT / "helpers" / "config.py",
        REPO_ROOT / "helpers" / "llm.py",
        REPO_ROOT / "data" / "documents",
        REPO_ROOT / "docs" / "llm_providers.md",
        REPO_ROOT / "docs" / "depth_expansion_plan.md",
        REPO_ROOT / "SETUP.md",
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"missing required path: {path.relative_to(REPO_ROOT)}")

    if failures:
        print("Notebook validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Notebook validation passed.")
    print(f"- learner notebooks: {len(learner)}")
    print(f"- solution notebooks: {len(solutions)}")
    print(f"- supplemental learner notebooks: {len(supplemental_learner)}")
    print(f"- supplemental solution notebooks: {len(supplemental_solutions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
