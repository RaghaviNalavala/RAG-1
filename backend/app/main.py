from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.models import router as models_router
from app.api.practice import router as practice_router
from app.config import FRONTEND_ORIGIN
from app.database.session import init_db

app = FastAPI(title='AI Coding Assistant API', version='0.1.0')

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, 'http://localhost:5174', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router, prefix='/api')
app.include_router(models_router, prefix='/api')
app.include_router(chat_router, prefix='/api')
app.include_router(documents_router, prefix='/api')
app.include_router(conversations_router, prefix='/api')
app.include_router(practice_router, prefix='/api')


@app.on_event('startup')
def startup_event() -> None:
    init_db()


@app.get('/')
def root() -> dict:
    return {'message': 'AI Coding Assistant Backend'}
