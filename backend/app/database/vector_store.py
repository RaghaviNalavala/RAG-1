from __future__ import annotations

from typing import Any

import chromadb

from app.config import CHROMA_PATH, DEFAULT_MODEL, EMBEDDING_MODEL


class VectorStore:
    def __init__(self, collection_name: str = 'ai_coding_assistant') -> None:
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        if not documents:
            return
        self.collection.add(
            ids=[doc['id'] for doc in documents],
            documents=[doc['content'] for doc in documents],
            metadatas=[doc.get('metadata', {}) for doc in documents],
            embeddings=[doc['embedding'] for doc in documents],
        )

    def query(self, embedding: list[float], top_k: int = 4, where: dict | None = None) -> dict:
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where,
        )

    def delete_by_ids(self, ids: list[str]) -> None:
        if ids:
            self.collection.delete(ids=ids)

    def get_count(self) -> int:
        return self.collection.count()

    def get_collection_info(self) -> dict:
        return {"name": self.collection.name, "count": self.get_count()}


vector_store = VectorStore()
