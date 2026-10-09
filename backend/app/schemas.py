from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    conversation_id: str | None = None
    selected_model: str | None = None
    response_language: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]] = []
    conversation_id: str
    active_model: str
    processing_time_ms: int


class DocumentUploadRequest(BaseModel):
    filename: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 4


class FeedbackRequest(BaseModel):
    conversation_id: str | None = None
    rating: Literal['helpful', 'partially_helpful', 'not_helpful']
    comment: str | None = None


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    active_model: str
    model_available: bool
    vector_db_ready: bool
    version: str
