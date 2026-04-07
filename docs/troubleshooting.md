# Troubleshooting Guide

## Common Setup Issues

### `python: command not found`

This repo assumes `python3` is available in the shell.

Use:

```bash
python3 --version
python3 -m venv .venv
```

### `ModuleNotFoundError: agent_framework`

Cause:
The importable `agent_framework` module comes from `agent-framework-core`.

Fix:

```bash
python3 -m pip install -r requirements.txt
```

### `ModuleNotFoundError: agent_framework_openai`

Fix:

```bash
python3 -m pip install -r requirements.txt
```

The OpenAI/Azure OpenAI provider integration is shipped through `agent-framework-openai`.

## Provider Issues

### OpenRouter request fails with 401

Check:

- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- selected model availability

### Azure OpenAI request fails with 404 or deployment errors

Check:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_MODEL`
- `AZURE_OPENAI_API_VERSION`

The `model` should match your deployment name when Azure expects deployment-based routing.

### Smoke test is skipped

`scripts/smoke_live.py` skips safely when required credentials are missing. That is expected behavior for CI or local environments without provider access.

## Notebook Issues

### Import path problems inside Jupyter

Each generated notebook includes a path bootstrap cell. If you still see import errors, start Jupyter from the repo root:

```bash
jupyter lab
```

### RAG notebook fails on scikit-learn import

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

### SQLite file is not created

Make sure the target directory exists or use the helper class in [helpers/memory.py](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/helpers/memory.py), which creates parent directories automatically.

## Validation Issues

### `validate_notebooks.py` reports missing headings

Regenerate the notebook assets:

```bash
python3 scripts/generate_course_materials.py
```

### Notebook count is wrong

The repo expects:

- 15 learner notebooks
- 15 solution notebooks

If counts drift, regenerate the materials.
