from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import UPLOAD_DIR
from app.database.models import DocumentRecord
from app.database.vector_store import vector_store
from app.dependencies import get_db
from app.services.document_service import index_document, validate_file

router = APIRouter()


@router.post('/documents/upload')
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail='Filename is required.')
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {'.txt', '.md', '.pdf', '.docx'}:
        raise HTTPException(status_code=400, detail='Unsupported file type. Allowed: PDF, TXT, Markdown, DOCX.')
    file_path = UPLOAD_DIR / file.filename
    file_bytes = await file.read()
    file_path.write_bytes(file_bytes)
    validate_file(file_path)
    document_id = str(uuid.uuid4())
    index = await index_document(file_path, document_id, file.filename)
    db.add(DocumentRecord(
        id=document_id,
        filename=file.filename,
        path=str(file_path),
        file_type=suffix.lstrip('.'),
        status='indexed',
        chunk_count=index['chunk_count'],
        metadata_json={'document_id': document_id}
    ))
    db.commit()
    return {'message': 'Document uploaded and indexed.', 'document_id': document_id, 'chunk_count': index['chunk_count']}


@router.get('/documents')
async def list_documents(db: Session = Depends(get_db)) -> dict:
    items = db.query(DocumentRecord).all()
    payload = [{
        'id': item.id,
        'filename': item.filename,
        'file_type': item.file_type,
        'status': item.status,
        'chunk_count': item.chunk_count,
    } for item in items]
    return {'documents': payload, 'total': len(payload), 'vector_count': vector_store.get_count()}


@router.get('/documents/{document_id}')
async def get_document(document_id: str, db: Session = Depends(get_db)) -> dict:
    item = db.query(DocumentRecord).filter(DocumentRecord.id == document_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Document not found.')
    return {'document': {'id': item.id, 'filename': item.filename, 'file_type': item.file_type, 'status': item.status, 'path': item.path}}


@router.delete('/documents/{document_id}')
async def delete_document(document_id: str, db: Session = Depends(get_db)) -> dict:
    item = db.query(DocumentRecord).filter(DocumentRecord.id == document_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Document not found.')
    try:
        vector_store.delete_by_ids([f'{document_id}_{idx}' for idx in range(item.chunk_count or 0)])
    except Exception:
        pass
    file_path = Path(item.path)
    if file_path.exists():
        file_path.unlink()
    db.delete(item)
    db.commit()
    return {'message': 'Document deleted', 'document_id': document_id}


@router.post('/documents/reindex')
async def reindex_documents() -> dict:
    return {'message': 'Re-index workflow is available; current implementation reuses the upload/index pipeline.'}


@router.post('/search')
async def search_documents(payload: dict) -> dict:
    query = payload.get('query')
    top_k = int(payload.get('top_k', 4))
    if not query:
        raise HTTPException(status_code=400, detail='Query is required.')
    docs = await __import__('app.services.retrieval_service', fromlist=['retrieval_service']).retrieval_service.search(query, top_k=top_k)
    return {'results': docs}
