"""Validation utilities used from notebooks and scripts."""

from __future__ import annotations

import sys
from pathlib import Path

from .config import ProviderName, load_settings


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_notebook_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "helpers").exists():
        return cwd
    if (cwd.parent / "helpers").exists():
        return cwd.parent
    return get_repo_root()


def assert_minimum_python(major: int = 3, minor: int = 10) -> None:
    if sys.version_info < (major, minor):
        raise RuntimeError(f"Python {major}.{minor}+ is required. Found {sys.version.split()[0]}.")


def validate_provider_configuration(provider: ProviderName | None = None) -> dict[str, bool]:
    settings = load_settings()
    active_provider = provider or settings.provider

    if active_provider == "openrouter":
        return {
            "provider_selected": settings.provider == "openrouter",
            "api_key_present": bool(settings.openrouter_api_key),
            "model_present": bool(settings.openrouter_model),
            "base_url_present": bool(settings.openrouter_base_url),
        }

    return {
        "provider_selected": settings.provider == "azure_openai",
        "endpoint_present": bool(settings.azure_openai_endpoint),
        "api_key_present": bool(settings.azure_openai_api_key),
        "model_present": bool(settings.azure_openai_model),
        "api_version_present": bool(settings.azure_openai_api_version),
    }
