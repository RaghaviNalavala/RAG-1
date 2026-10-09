from __future__ import annotations

from app.config import EMBEDDING_MODEL
from app.services.ollama_service import ollama_service


class EmbeddingService:
    async def embed_text(self, text: str) -> list[float]:
        return await ollama_service.embed(EMBEDDING_MODEL, text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(await self.embed_text(text))
        return embeddings


embedding_service = EmbeddingService()
