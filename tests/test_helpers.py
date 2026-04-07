from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from helpers.config import load_settings
from helpers.memory import SQLiteConversationMemory
from helpers.rag import LocalTfidfVectorStore, chunk_documents, load_text_documents


class HelpersTestCase(unittest.TestCase):
    def test_load_settings_defaults_to_openrouter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text("LLM_PROVIDER=openrouter\nOPENROUTER_MODEL=test-model\n", encoding="utf-8")
            settings = load_settings(env_path)
            self.assertEqual(settings.provider, "openrouter")
            self.assertEqual(settings.openrouter_model, "test-model")

    def test_sqlite_memory_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            memory = SQLiteConversationMemory(Path(tmp_dir) / "memory.sqlite3")
            memory.save("alice", "hello", "hi there")
            rows = memory.history("alice", limit=1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].user_message, "hello")

    def test_rag_helpers_load_and_search(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        documents = load_text_documents(repo_root / "data" / "documents")
        chunks = chunk_documents(documents, chunk_size=120, overlap=20)
        store = LocalTfidfVectorStore()
        store.add_chunks(chunks)
        results = store.search("async programming", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertIn("score", results[0])


if __name__ == "__main__":
    unittest.main()
