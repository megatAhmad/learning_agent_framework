# Glossary

## Agent

A reusable object that wraps a chat client plus instructions, tools, middleware, and optional session/context behavior.

## Chat Client

The provider-specific runtime used by an agent to send messages to a model.

## Tool

A callable function or provider-native capability that the model can invoke while solving a task.

## Session

An `AgentSession` object that carries a `session_id`, optional service-side session identifiers, and mutable state.

## Context Provider

A hook object that can add context before a run and process results after a run.

## RAG

Retrieval-augmented generation. The system retrieves relevant context first, then uses that context during generation.

## Workflow

A graph of executors or wrapped agents connected by edges.

## Executor

A workflow node that accepts typed input and sends messages or yields outputs through a `WorkflowContext`.

## Handoff

An orchestration pattern where one agent or routing component delegates the task to a more specialized agent.

## Human-in-the-Loop

An interaction pattern where approval, review, or resume decisions require a person before the workflow continues.
