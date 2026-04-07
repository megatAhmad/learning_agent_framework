"""Small debugging helpers used inside notebooks."""

from __future__ import annotations

import json
from typing import Any


def print_banner(title: str) -> None:
    line = "=" * len(title)
    print(f"\n{line}\n{title}\n{line}")


def print_json(data: Any, *, title: str | None = None) -> None:
    if title:
        print_banner(title)
    print(json.dumps(data, indent=2, default=str))


def describe_response(response: Any) -> dict[str, Any]:
    """Return a lightweight response summary that works across response types."""

    return {
        "type": type(response).__name__,
        "text": getattr(response, "text", str(response)),
        "response_id": getattr(response, "response_id", None),
        "usage": getattr(response, "usage", None),
        "message_count": len(getattr(response, "messages", []) or []),
    }


def summarize_session(session: Any) -> dict[str, Any]:
    """Summarize an AgentSession without assuming custom fields."""

    state = getattr(session, "state", {})
    return {
        "session_id": getattr(session, "session_id", None),
        "service_session_id": getattr(session, "service_session_id", None),
        "state_keys": sorted(state.keys()) if isinstance(state, dict) else [],
        "message_count": len(state.get("messages", [])) if isinstance(state, dict) else None,
    }
