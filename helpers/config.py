"""Configuration helpers for the course notebooks."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

ProviderName = Literal["openrouter", "azure_openai"]


@dataclass(slots=True)
class CourseSettings:
    """Resolved environment settings for the course."""

    provider: ProviderName
    debug: bool
    log_level: str
    openrouter_api_key: str | None
    openrouter_base_url: str
    openrouter_model: str
    openrouter_app_name: str
    openrouter_site_url: str
    azure_openai_endpoint: str | None
    azure_openai_api_key: str | None
    azure_openai_model: str
    azure_openai_api_version: str

    def provider_label(self) -> str:
        return "Azure OpenAI" if self.provider == "azure_openai" else "OpenRouter"


def _as_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings(env_file_path: str | Path | None = None) -> CourseSettings:
    """Load course settings from the environment and optional `.env` file."""

    if env_file_path is None:
        repo_root = Path(__file__).resolve().parents[1]
        candidate = repo_root / ".env"
        if candidate.exists():
            load_dotenv(candidate, override=False)
    else:
        load_dotenv(Path(env_file_path), override=False)

    provider = os.getenv("LLM_PROVIDER", "openrouter").strip().lower()
    if provider not in {"openrouter", "azure_openai"}:
        raise ValueError(f"Unsupported provider {provider!r}. Use 'openrouter' or 'azure_openai'.")

    return CourseSettings(
        provider=provider,  # type: ignore[arg-type]
        debug=_as_bool(os.getenv("DEBUG")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        openrouter_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini"),
        openrouter_app_name=os.getenv(
            "OPENROUTER_APP_NAME",
            "Microsoft Agent Framework Mastery Program",
        ),
        openrouter_site_url=os.getenv(
            "OPENROUTER_SITE_URL",
            "https://example.com/agent-framework-mastery",
        ),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_openai_model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4.1-mini"),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "preview"),
    )
