from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import DEFAULT_MODEL, EMBEDDING_MODEL
from app.services.ollama_service import ollama_service

router = APIRouter()


@router.get('/models')
async def list_models() -> dict:
    try:
        models = await ollama_service.list_models()
        return {'models': models, 'default_model': DEFAULT_MODEL, 'embedding_model': EMBEDDING_MODEL}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get('/models/status')
async def models_status() -> dict:
    try:
        connected = await ollama_service.check_connection()
        available = await ollama_service.list_models()
        return {
            'ollama_connected': connected,
            'available_models': available,
            'default_model': DEFAULT_MODEL,
            'embedding_model': EMBEDDING_MODEL,
            'active_model': DEFAULT_MODEL,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post('/models/select')
async def select_model(payload: dict) -> dict:
    model_name = payload.get('model_name') or payload.get('model')
    if not model_name:
        raise HTTPException(status_code=400, detail='A model name is required.')
    available = await ollama_service.list_models()
    if model_name not in available:
        raise HTTPException(status_code=400, detail=f'Model {model_name} not found. Install it with `ollama pull {model_name}`.')
    return {'message': 'Model selected', 'selected_model': model_name}
