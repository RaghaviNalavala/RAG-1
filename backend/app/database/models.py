from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Text, Float, JSON
from sqlalchemy.sql import func

from app.database.session import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    model_name = Column(String, nullable=True)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata_json = Column(JSON, nullable=True)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(String, nullable=True)
    rating = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DocumentRecord(Base):
    __tablename__ = 'documents'

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    status = Column(String, default='indexed')
    chunk_count = Column(Integer, default=0)
    metadata_json = Column(JSON, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class Preference(Base):
    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=True)
