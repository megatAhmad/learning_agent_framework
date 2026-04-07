"""Local RAG helpers used in the retrieval notebook."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(slots=True)
class DocumentChunk:
    chunk_id: str
    source_id: str
    title: str
    content: str


def load_text_documents(documents_dir: str | Path) -> list[dict[str, str]]:
    path = Path(documents_dir)
    documents: list[dict[str, str]] = []
    for file_path in sorted(path.glob("*.txt")):
        documents.append(
            {
                "id": file_path.stem,
                "title": file_path.stem.replace("_", " ").title(),
                "content": file_path.read_text(encoding="utf-8"),
            }
        )
    return documents


def chunk_documents(
    documents: list[dict[str, str]],
    *,
    chunk_size: int = 360,
    overlap: int = 60,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for document in documents:
        text = document["content"]
        stride = max(1, chunk_size - overlap)
        for start in range(0, len(text), stride):
            content = text[start : start + chunk_size].strip()
            if not content:
                continue
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document['id']}-{start}",
                    source_id=document["id"],
                    title=document["title"],
                    content=content,
                )
            )
    return chunks


class LocalTfidfVectorStore:
    """Simple local vector store for notebook-sized examples."""

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(stop_words="english", max_features=1500)
        self._chunks: list[DocumentChunk] = []
        self._matrix = None

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        self._chunks = list(chunks)
        corpus = [chunk.content for chunk in chunks]
        self._matrix = self._vectorizer.fit_transform(corpus)

    def search(self, query: str, *, top_k: int = 3) -> list[dict[str, object]]:
        if self._matrix is None:
            raise RuntimeError("No chunks have been indexed yet.")
        query_vector = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self._matrix)[0]
        ranked = scores.argsort()[::-1][:top_k]
        return [
            {
                "chunk": self._chunks[index],
                "score": float(scores[index]),
            }
            for index in ranked
        ]
