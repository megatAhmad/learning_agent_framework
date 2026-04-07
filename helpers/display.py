"""Display-oriented helpers for notebook output."""

from __future__ import annotations


def print_step_header(step_number: int, title: str) -> None:
    print(f"Step {step_number:02d}: {title}")
    print("-" * (len(title) + 9))


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def code_block(code: str, language: str = "python") -> str:
    return f"```{language}\n{code.rstrip()}\n```"
