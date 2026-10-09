from __future__ import annotations

from app.services.ollama_service import ollama_service


class EvaluationService:
    async def evaluate_answer(self, question: str, answer: str) -> str:
        prompt = (
            f"Question: {question}\n\nSubmitted answer: {answer}\n\nEvaluate the answer using a structured rubric. "
            "Return correct concepts, missing concepts, suggested improvements, and a model answer."
        )
        return await ollama_service.generate('qwen2.5:3b', prompt, system_prompt='You are a fair interviewer with clear criteria and measured feedback.')


evaluation_service = EvaluationService()
