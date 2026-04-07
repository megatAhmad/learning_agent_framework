# Supplemental Notebook Depth Plan

This document extends the original 15-step course with a supplemental track aimed at learners who want stronger intermediate and advanced coverage without changing the beginner-first flow.

## Goals

- keep the original 15 notebooks as the primary path
- add deeper follow-on notebooks for intermediate and advanced learners
- focus the new material on the depth gaps identified in review:
  - more framework-aware reasoning about tools and workflows
  - stronger context and memory design patterns
  - more operational treatment of evaluation, human oversight, and production hardening

## Supplemental Track

### Intermediate

1. `16_intermediate_tool_reasoning_and_schema_design.ipynb`
   Focus: tool contracts, schema-aware design, tool selection tradeoffs, multi-step tool planning

2. `17_intermediate_context_engineering_and_memory_patterns.ipynb`
   Focus: context shaping, session-memory boundaries, recall injection, summarization and pruning

3. `18_intermediate_workflow_patterns_with_typed_executors.ipynb`
   Focus: typed executors, edge conditions, fan-out/fan-in, workflow inspection and debugging

### Advanced

4. `19_advanced_multi_agent_evaluation_and_trace_analysis.ipynb`
   Focus: evaluation datasets, rubric-based assessment, trace inspection, iterative improvement loops

5. `20_advanced_human_approval_and_checkpointed_workflows.ipynb`
   Focus: approval boundaries, checkpoint design, resume mechanics, operator-facing audit state

6. `21_advanced_provider_strategy_and_production_hardening.ipynb`
   Focus: provider fallback thinking, failure handling, cost and latency tradeoffs, hardening checklists

## Notebook Design Rules

- each supplemental notebook should feel deeper than the core notebooks
- each one should include at least:
  - 3-4 implementation sections
  - 2 guided exercises
  - 1 extension/reflection section
- exercises should require modification, not just running a provided cell
- advanced notebooks should include explicit tradeoff discussions and failure modes

## Intended Usage

- finish the main 15-step path first
- then pick the supplemental notebooks by current learning goal
- intermediate notebooks are suitable after Step 9 or Step 10
- advanced notebooks are most useful after Step 12+
