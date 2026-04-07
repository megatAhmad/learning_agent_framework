# Microsoft Agent Framework Mastery Program

Hands-on learning repository for building local, production-minded AI agents with the Microsoft Agent Framework in Python.

This repo now contains a full course project built from the PRD package in the root:

- 15 core learner notebooks in [notebooks](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/notebooks)
- 15 mirrored core solution notebooks in [solutions](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/solutions)
- 6 supplemental intermediate and advanced learner notebooks in [notebooks/supplemental](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/notebooks/supplemental)
- 6 mirrored supplemental solution notebooks in [solutions/supplemental](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/solutions/supplemental)
- reusable helper modules in [helpers](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/helpers)
- sample documents, examples, and database assets in [data](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/data)
- setup and reference docs in [docs](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/docs)
- generation, validation, and smoke-test scripts in [scripts](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/scripts)

The implementation targets the current Python package surface used in this repo:

- `agent-framework-core==1.0.0`
- `agent-framework-openai==1.0.0`
- Python `>=3.10`

## Quick Start

Create a virtual environment and install the pinned dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Copy the environment template and add provider credentials:

```bash
cp .env.example .env
```

Generate or refresh the notebooks and sample assets:

```bash
python scripts/generate_course_materials.py
```

Validate the generated materials:

```bash
python scripts/validate_notebooks.py
python -m unittest discover -s tests
python scripts/smoke_live.py --provider openrouter
```

`scripts/smoke_live.py` is credential-gated and safely skips when the required environment variables are not set.

## Course Layout

### Core 15-Step Path

| Step | Notebook | Focus |
| --- | --- | --- |
| 1 | `01_setup_and_environment.ipynb` | Environment, dependencies, provider setup |
| 2 | `02_your_first_agent.ipynb` | Single-agent basics |
| 3 | `03_multi_turn_conversations.ipynb` | Sessions and conversation history |
| 4 | `04_understanding_tools.ipynb` | Tool anatomy and registration |
| 5 | `05_single_tool_integration.ipynb` | Single-tool agent flow |
| 6 | `06_multiple_tools.ipynb` | Coordinated tool use |
| 7 | `07_custom_tools_and_apis.ipynb` | Async tools and REST APIs |
| 8 | `08_memory_and_sessions.ipynb` | Persistent memory and session state |
| 9 | `09_rag_implementation.ipynb` | Retrieval-augmented generation |
| 10 | `10_basic_workflows.ipynb` | Sequential workflows |
| 11 | `11_conditional_workflows.ipynb` | Branching and routing |
| 12 | `12_orchestration_patterns.ipynb` | Sequential, concurrent, handoff patterns |
| 13 | `13_advanced_orchestration.ipynb` | Group chat and manager-worker orchestration |
| 14 | `14_human_in_the_loop.ipynb` | Approvals, checkpoints, resume |
| 15 | `15_production_features.ipynb` | Logging, metrics, debugging, cost awareness |

### Supplemental Depth Track

These notebooks deepen the intermediate and advanced material without changing the beginner-first core sequence.

| Level | Notebook | Focus |
| --- | --- | --- |
| Intermediate | `supplemental/16_intermediate_tool_reasoning_and_schema_design.ipynb` | tool contracts, schema design, tool-choice strategy |
| Intermediate | `supplemental/17_intermediate_context_engineering_and_memory_patterns.ipynb` | context shaping, recall strategies, memory boundaries |
| Intermediate | `supplemental/18_intermediate_workflow_patterns_with_typed_executors.ipynb` | typed executors, routing, fan-out/fan-in, debugging |
| Advanced | `supplemental/19_advanced_multi_agent_evaluation_and_trace_analysis.ipynb` | evaluation loops, trace review, quality feedback |
| Advanced | `supplemental/20_advanced_human_approval_and_checkpointed_workflows.ipynb` | approval design, checkpointing, resumability |
| Advanced | `supplemental/21_advanced_provider_strategy_and_production_hardening.ipynb` | provider policy, degradation, hardening checklists |

## Repository Workflow

The checked-in `.ipynb` files are the learner-facing source of truth, but they are generated consistently from [generate_course_materials.py](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/scripts/generate_course_materials.py). If you change notebook content in the generator, regenerate the materials before validating the repo.

The repo also includes:

- [SETUP.md](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/SETUP.md) for installation and provider setup
- [llm_providers.md](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/docs/llm_providers.md) for OpenRouter and Azure OpenAI configuration
- [troubleshooting.md](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/docs/troubleshooting.md) for common issues
- [progress_tracker.md](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/docs/progress_tracker.md) for learner progress tracking
- [depth_expansion_plan.md](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/docs/depth_expansion_plan.md) for the intermediate and advanced expansion track

## Validation

[validate_notebooks.py](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/scripts/validate_notebooks.py) checks:

- core learner and solution notebook counts
- supplemental learner and solution notebook counts
- notebook metadata
- required markdown sections
- required helper/data/doc paths

The test suite in [tests](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/tests) covers:

- helper configuration loading
- SQLite memory round-trips
- local RAG helper behavior
- repository structure expectations

## Notes

- The repo is live-provider-first for agent calls.
- OpenRouter and Azure OpenAI are both supported through the shared helper layer in [llm.py](/home/percy/code/gptCodex/agentLearning/learning_agent_framework/helpers/llm.py).
- The original PRD markdown files remain in the repo root as reference specifications for the generated course.
