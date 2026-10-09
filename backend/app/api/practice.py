from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import DEFAULT_MODEL
from app.schemas import FeedbackRequest
from app.services.coding_service import coding_service
from app.services.evaluation_service import evaluation_service
from app.database.models import Feedback
from app.database.session import SessionLocal

router = APIRouter()


@router.post('/code/explain')
async def code_explain(payload: dict) -> dict:
    code = payload.get('code')
    language = payload.get('language', 'python')
    if not code:
        raise HTTPException(status_code=400, detail='Code is required.')
    answer = await coding_service.explain_code(code, language)
    return {'answer': answer}


@router.post('/code/debug')
async def code_debug(payload: dict) -> dict:
    code = payload.get('code')
    language = payload.get('language', 'python')
    if not code:
        raise HTTPException(status_code=400, detail='Code is required.')
    answer = await coding_service.debug_code(
        code,
        language,
        payload.get('error_message', ''),
        payload.get('expected_behavior', 'The program should behave correctly.'),
        payload.get('actual_behavior', 'The program fails or behaves unexpectedly.'),
    )
    return {'answer': answer}


@router.post('/practice/generate')
async def practice_generate(payload: dict) -> dict:
    answer = await coding_service.generate_practice_questions(
        payload.get('language', 'python'),
        payload.get('topic', 'algorithms'),
        payload.get('difficulty', 'beginner'),
        int(payload.get('count', 2)),
    )
    return {'answer': answer}


@router.post('/interview/answer')
async def interview_answer(payload: dict) -> dict:
    question = payload.get('question')
    answer = payload.get('answer')
    if not question or not answer:
        raise HTTPException(status_code=400, detail='Question and answer are required.')
    evaluation = await evaluation_service.evaluate_answer(question, answer)
    return {'answer': evaluation}


@router.post('/feedback')
async def submit_feedback(payload: FeedbackRequest) -> dict:
    db = SessionLocal()
    db.add(Feedback(
        conversation_id=payload.conversation_id,
        rating=payload.rating,
        comment=payload.comment,
    ))
    db.commit()
    db.close()
    return {'message': 'Feedback saved'}
