# LLM Provider Guide

This course supports two live providers:

- OpenRouter
- Azure OpenAI

Both are accessed through `agent-framework-openai` and the shared helper factory in [helpers/llm.py](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/helpers/llm.py).

## OpenRouter

Use OpenRouter when you want:

- fast local experimentation
- easy model switching
- a simple API key setup

Required environment variables:

```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

Implementation notes:

- the course uses `OpenAIChatClient` with an OpenAI-compatible `base_url`
- the helper adds `HTTP-Referer` and `X-Title` headers for OpenRouter attribution

## Azure OpenAI

Use Azure OpenAI when you want:

- enterprise-aligned authentication
- Azure-hosted OpenAI deployments
- a closer production path for Microsoft-native environments

Required environment variables:

```bash
LLM_PROVIDER=azure_openai
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_MODEL=gpt-4.1-mini
AZURE_OPENAI_API_VERSION=preview
```

Implementation notes:

- the course uses `OpenAIChatClient` with `azure_endpoint=...`
- for this repo, API-key auth is the default teaching path
- `azure-identity` is installed so the repo can be extended to Entra-based auth later

## How Switching Works

The course helper surface is intentionally small:

- `load_settings()`
- `create_chat_client(provider=...)`
- `create_agent(...)`

Most notebooks call `create_agent(...)` and stay provider-agnostic at the lesson level.

## Recommendation

- Start the first 5-7 notebooks on OpenRouter.
- Validate your mental model of the framework and notebook flow.
- Switch to Azure OpenAI once you want to compare behavior or test a more enterprise-oriented path.
