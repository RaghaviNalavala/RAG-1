from __future__ import annotations

from app.config import DEFAULT_MODEL
from app.services.ollama_service import ollama_service


class RAGService:
    async def answer_question(self, question: str, context_chunks: list[dict], model_name: str = DEFAULT_MODEL) -> str:
        if not context_chunks:
            system_prompt = (
                'You are a helpful beginner-friendly programming tutor. Answer from general programming knowledge '
                'and say when the evidence is limited or when no known document context is available.'
            )
            prompt = question
        else:
            context_text = '\n\n'.join(
                f"Source: {chunk['metadata'].get('filename', 'Unknown')}\n{chunk['content']}" for chunk in context_chunks
            )
            system_prompt = (
                'You are a helpful teaching assistant. Use the retrieved document context when relevant, '
                'cite source filenames when discussing extracted facts, and plainly say if the context is insufficient.'
            )
            prompt = f"Context:\n{context_text}\n\nQuestion:\n{question}\n\nAnswer with a clear beginner-friendly explanation and include any limitations."

        return await ollama_service.generate(model_name, prompt, system_prompt=system_prompt)


rag_service = RAGService()
