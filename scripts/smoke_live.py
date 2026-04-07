#!/usr/bin/env python3
"""Credential-gated live smoke tests for provider configuration."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from helpers import create_agent, require_live_provider


async def run_smoke(provider: str) -> int:
    try:
        settings = require_live_provider(provider=provider)  # type: ignore[arg-type]
    except Exception as exc:
        print(f"Skipping live smoke test for {provider}: {exc}")
        return 0

    agent = create_agent(
        name="SmokeTestAgent",
        instructions=(
            "You are a concise assistant. Reply with one sentence that confirms the provider is working."
        ),
        provider=provider,  # type: ignore[arg-type]
        default_options={"max_output_tokens": 120},
    )
    response = await agent.run("Say hello from the live smoke test.")
    text = getattr(response, "text", str(response))
    print(f"Provider: {settings.provider_label()}")
    print(f"Response: {text}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        choices=["openrouter", "azure_openai"],
        default="openrouter",
    )
    args = parser.parse_args()
    return asyncio.run(run_smoke(args.provider))


if __name__ == "__main__":
    raise SystemExit(main())
