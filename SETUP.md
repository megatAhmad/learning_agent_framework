# Setup Instructions

## Prerequisites

- Python `3.10+`
- Internet access for package installation and live provider calls
- One provider configured:
  - OpenRouter API key, or
  - Azure OpenAI endpoint plus API key

This course is live-provider-first. Most agent notebooks assume working credentials.

## 1. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

## 2. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

Core framework packages:

- `agent-framework-core==1.0.0`
- `agent-framework-openai==1.0.0`

These provide:

- `agent_framework`
- `agent_framework_openai`

## 3. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Then edit `.env`.

### OpenRouter

Minimum configuration:

```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

### Azure OpenAI

Minimum configuration:

```bash
LLM_PROVIDER=azure_openai
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_MODEL=gpt-4.1-mini
AZURE_OPENAI_API_VERSION=preview
```

## 4. Generate Course Assets

The notebooks and mirrored solution notebooks are generated from the repository templates:

```bash
python3 scripts/generate_course_materials.py
```

You only need to rerun this when the templates or generated assets change.

## 5. Validate the Repo

Structural validation:

```bash
python3 scripts/validate_notebooks.py
```

Optional live smoke tests:

```bash
python3 scripts/smoke_live.py --provider openrouter
python3 scripts/smoke_live.py --provider azure_openai
```

## Troubleshooting

### `ModuleNotFoundError: agent_framework`

Install the pinned dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The importable module comes from `agent-framework-core`, not the meta package alone.

### OpenRouter 401 or 403

- Check `OPENROUTER_API_KEY`
- Confirm the selected model is available to your account
- Make sure `OPENROUTER_BASE_URL` is `https://openrouter.ai/api/v1`

### Azure OpenAI Authentication Errors

- Verify `AZURE_OPENAI_ENDPOINT`
- Verify `AZURE_OPENAI_API_KEY`
- Verify `AZURE_OPENAI_MODEL`
- If using a preview Responses API deployment, keep `AZURE_OPENAI_API_VERSION=preview`

### Notebook Import Errors

Run notebooks from the repo root or from the `notebooks/` folder with the repo root on `sys.path`. Each generated notebook includes the path bootstrap cell already.

## Suggested Workflow

1. Complete Step 1 fully.
2. Pick one provider and keep it consistent for the first 5-7 notebooks.
3. Re-run `scripts/smoke_live.py` when provider settings change.
4. Use the mirrored notebook in `solutions/` only after trying the learner notebook first.
