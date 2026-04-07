"""Factory helpers for creating clients and agents."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from agent_framework import Agent
from agent_framework_openai import OpenAIChatClient

from .config import CourseSettings, ProviderName, load_settings


def _default_headers(settings: CourseSettings) -> dict[str, str]:
    return {
        "X-Title": settings.openrouter_app_name,
        "HTTP-Referer": settings.openrouter_site_url,
    }


def require_live_provider(provider: ProviderName | None = None) -> CourseSettings:
    """Return settings or raise a friendly error if credentials are missing."""

    settings = load_settings()
    active_provider = provider or settings.provider

    if active_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required for live OpenRouter calls.")
    elif active_provider == "azure_openai":
        if not settings.azure_openai_endpoint:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT is required for live Azure OpenAI calls.")
        if not settings.azure_openai_api_key:
            raise RuntimeError("AZURE_OPENAI_API_KEY is required for live Azure OpenAI calls.")
    else:
        raise ValueError(f"Unsupported provider {active_provider!r}.")

    return settings


def create_chat_client(
    provider: ProviderName | None = None,
    *,
    env_file_path: str | None = None,
    model: str | None = None,
    default_headers: Mapping[str, str] | None = None,
) -> OpenAIChatClient:
    """Create a live chat client for OpenRouter or Azure OpenAI."""

    settings = load_settings(env_file_path)
    active_provider = provider or settings.provider

    if active_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required to create an OpenRouter client.")
        headers = dict(_default_headers(settings))
        if default_headers:
            headers.update(default_headers)
        return OpenAIChatClient(
            model=model or settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            default_headers=headers,
            env_file_path=env_file_path,
        )

    if active_provider == "azure_openai":
        if not settings.azure_openai_endpoint:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT is required to create an Azure OpenAI client.")
        if not settings.azure_openai_api_key:
            raise RuntimeError("AZURE_OPENAI_API_KEY is required to create an Azure OpenAI client.")
        return OpenAIChatClient(
            model=model or settings.azure_openai_model,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            default_headers=dict(default_headers or {}),
            env_file_path=env_file_path,
        )

    raise ValueError(f"Unsupported provider {active_provider!r}.")


def create_agent(
    *,
    name: str,
    instructions: str,
    provider: ProviderName | None = None,
    description: str | None = None,
    tools: Any | Sequence[Any] | None = None,
    default_options: Mapping[str, Any] | None = None,
    context_providers: Sequence[Any] | None = None,
) -> Agent:
    """Create a standard course agent."""

    client = create_chat_client(provider)
    return Agent(
        client=client,
        name=name,
        description=description or f"Course helper agent for {name}",
        instructions=instructions,
        tools=tools,
        default_options=dict(default_options or {}),
        context_providers=list(context_providers or []),
    )
