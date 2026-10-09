from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Conversation, Message
from app.dependencies import get_db

router = APIRouter()


@router.get('/conversations')
async def list_conversations(db: Session = Depends(get_db)) -> dict:
    conversations = db.query(Conversation).all()
    return {'conversations': [{
        'id': item.id,
        'title': item.title,
        'model_name': item.model_name,
    } for item in conversations]}


@router.get('/conversations/{conversation_id}')
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)) -> dict:
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found.')
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.id.asc()).all()
    return {'conversation': {'id': conversation.id, 'title': conversation.title, 'model_name': conversation.model_name}, 'messages': [
        {'id': m.id, 'role': m.role, 'content': m.content, 'created_at': str(m.created_at)} for m in messages
    ]}


@router.delete('/conversations/{conversation_id}')
async def delete_conversation(conversation_id: str, db: Session = Depends(get_db)) -> dict:
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found.')
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    db.delete(conversation)
    db.commit()
    return {'message': 'Conversation deleted', 'conversation_id': conversation_id}
