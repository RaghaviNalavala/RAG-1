from __future__ import annotations

from app.database.vector_store import vector_store
from app.services.embedding_service import embedding_service


class RetrievalService:
    async def search(self, query: str, top_k: int = 4, filters: dict | None = None) -> list[dict]:
        embedding = await embedding_service.embed_text(query)
        result = vector_store.query(embedding=embedding, top_k=top_k, where=filters)
        docs: list[dict] = []
        if not result.get('documents'):
            return docs
        for idx, content in enumerate(result['documents'][0]):
            metadata = result.get('metadatas', [{}])[0][idx] if result.get('metadatas') else {}
            score = result.get('distances', [[0]])[0][idx] if result.get('distances') else 0.0
            docs.append({
                'content': content,
                'metadata': metadata,
                'score': score,
            })
        return docs


retrieval_service = RetrievalService()
