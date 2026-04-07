"""SQLite-backed helpers for the memory notebooks."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class MemoryRecord:
    user_id: str
    user_message: str
    agent_response: str
    created_at: str


class SQLiteConversationMemory:
    """Tiny SQLite store used in the memory-focused lessons."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def save(self, user_id: str, user_message: str, agent_response: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO conversations (user_id, user_message, agent_response, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, user_message, agent_response, timestamp),
            )
            connection.commit()

    def history(self, user_id: str, limit: int = 5) -> list[MemoryRecord]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                SELECT user_id, user_message, agent_response, created_at
                FROM conversations
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        return [MemoryRecord(*row) for row in rows]
