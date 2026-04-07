"""Reusable helpers for the course notebooks."""

from .config import CourseSettings, load_settings
from .debug import describe_response, print_banner, print_json, summarize_session
from .display import bullet_list, code_block, print_step_header
from .logging_utils import setup_notebook_logging
from .llm import create_agent, create_chat_client, require_live_provider
from .memory import SQLiteConversationMemory
from .notebook_checks import (
    assert_minimum_python,
    get_repo_root,
    resolve_notebook_root,
    validate_provider_configuration,
)
from .rag import DocumentChunk, LocalTfidfVectorStore, chunk_documents, load_text_documents

__all__ = [
    "CourseSettings",
    "DocumentChunk",
    "LocalTfidfVectorStore",
    "SQLiteConversationMemory",
    "assert_minimum_python",
    "bullet_list",
    "chunk_documents",
    "code_block",
    "create_agent",
    "create_chat_client",
    "describe_response",
    "get_repo_root",
    "load_settings",
    "load_text_documents",
    "print_banner",
    "print_json",
    "print_step_header",
    "require_live_provider",
    "resolve_notebook_root",
    "setup_notebook_logging",
    "summarize_session",
    "validate_provider_configuration",
]
