from __future__ import annotations

from fastapi import APIRouter

from app.config import DEFAULT_MODEL, EMBEDDING_MODEL
from app.database.vector_store import vector_store
from app.schemas import HealthResponse
from app.services.ollama_service import ollama_service

router = APIRouter()


@router.get('/health', response_model=HealthResponse)
async def health() -> HealthResponse:
    ollama_connected = await ollama_service.check_connection()
    models = await ollama_service.list_models()
    is_model_available = DEFAULT_MODEL in models
    ready = False
    try:
        ready = vector_store.get_count() >= 0
    except Exception:
        ready = False
    return HealthResponse(
        status='ok' if ollama_connected else 'degraded',
        ollama_connected=ollama_connected,
        active_model=DEFAULT_MODEL,
        model_available=is_model_available,
        vector_db_ready=ready,
        version='0.1.0',
    )
