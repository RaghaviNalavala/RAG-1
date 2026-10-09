from __future__ import annotations

from app.config import DEFAULT_MODEL
from app.services.ollama_service import ollama_service


class CodingService:
    async def explain_code(self, code: str, language: str, explanation_level: str = 'beginner') -> str:
        prompt = (
            f"Explain the following {language} code for a {explanation_level} learner. "
            "Describe the purpose, key variables and functions, control flow, expected output, and pitfalls.\n\n"
            f"```{language}\n{code}\n```"
        )
        return await ollama_service.generate(DEFAULT_MODEL, prompt, system_prompt='You are a clear programming tutor who explains code accurately and simply.')

    async def debug_code(self, code: str, language: str, error_message: str, expected_behavior: str, actual_behavior: str) -> str:
        prompt = (
            f"Programming language: {language}\n\nCode:\n```{language}\n{code}\n```\n\n"
            f"Error message: {error_message}\nExpected behavior: {expected_behavior}\nActual behavior: {actual_behavior}\n\n"
            "Provide a concise problem summary, likely cause, explanation, corrected code, and prevention tips. "
            "Label any fix as a suggestion if it has not been validated in a runtime."
        )
        return await ollama_service.generate(DEFAULT_MODEL, prompt, system_prompt='You are a debugging assistant that explains root causes and suggests safe, understandable fixes.')

    async def generate_practice_questions(self, language: str, topic: str, difficulty: str, count: int) -> str:
        prompt = (
            f"Generate {count} {difficulty.lower()} {language} practice questions on {topic}. "
            "For each question, include the prompt, constraints, input/output format, sample input, sample output, hints, and a hidden solution."
        )
        return await ollama_service.generate(DEFAULT_MODEL, prompt, system_prompt='You create well-structured beginner-friendly coding problems with explanations but do not reveal solutions immediately.')

    async def prepare_interview_question(self, topic: str) -> str:
        prompt = (
            f"Create a technical interview question on {topic}. Include a problem statement, expected answer outline, rubric, and model answer."
        )
        return await ollama_service.generate(DEFAULT_MODEL, prompt, system_prompt='You are a technical interview coach and explain concepts clearly without claiming an employer-specific score.')


coding_service = CodingService()
