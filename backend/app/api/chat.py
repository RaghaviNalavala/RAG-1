from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import DEFAULT_MODEL, TOP_K
from app.database.models import Conversation, Message
from app.database.session import SessionLocal
from app.dependencies import get_db
from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_service import ollama_service
from app.services.rag_service import rag_service
from app.services.retrieval_service import retrieval_service

router = APIRouter()


@router.post('/chat', response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail='Question cannot be empty.')
    model_name = request.selected_model or DEFAULT_MODEL
    available_models = await ollama_service.list_models()
    if not available_models:
        raise HTTPException(status_code=503, detail='Ollama is not reachable or no models are installed. Run `ollama pull qwen2.5:3b`.')
    if model_name not in available_models:
        raise HTTPException(status_code=400, detail=f'Model {model_name} is not installed. Install it with `ollama pull {model_name}`.')

    conversation_id = request.conversation_id or str(uuid.uuid4())
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        conversation = Conversation(id=conversation_id, title=request.question[:50] or 'New chat', model_name=model_name)
        db.add(conversation)
        db.commit()

    start = time.perf_counter()
    context_chunks = await retrieval_service.search(request.question, top_k=TOP_K)
    answer = await rag_service.answer_question(request.question, context_chunks, model_name=model_name)
    answer_time_ms = round((time.perf_counter() - start) * 1000)

    db.add(Message(conversation_id=conversation_id, role='user', content=request.question))
    db.add(Message(conversation_id=conversation_id, role='assistant', content=answer, metadata_json={'sources': context_chunks}))
    db.commit()

    return ChatResponse(
        answer=answer,
        sources=[{'filename': c['metadata'].get('filename', 'unknown'), 'chunk_id': c['metadata'].get('chunk_id'), 'content': c['content']} for c in context_chunks],
        conversation_id=conversation_id,
        active_model=model_name,
        processing_time_ms=answer_time_ms,
    )
