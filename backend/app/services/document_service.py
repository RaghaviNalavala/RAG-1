from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pypdf
from docx import Document as DocxDocument

from app.config import ALLOWED_EXTENSIONS, CHUNK_OVERLAP, CHUNK_SIZE, MAX_FILE_SIZE_MB, UPLOAD_DIR
from app.database.vector_store import vector_store
from app.services.embedding_service import embedding_service


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[^A-Za-z0-9_.-]', '_', name)
    return cleaned.strip()[:150] or 'document'


async def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == '.txt':
        return file_path.read_text(encoding='utf-8', errors='ignore')
    if suffix == '.md':
        return file_path.read_text(encoding='utf-8', errors='ignore')
    if suffix == '.docx':
        doc = DocxDocument(str(file_path))
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    if suffix == '.pdf':
        reader = pypdf.PdfReader(str(file_path))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or '')
        return '\n\n'.join(pages)
    raise ValueError(f'Unsupported file type: {suffix}')


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text.strip():
        return []
    text = re.sub(r'\s+', ' ', text).strip()
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text):
            break
        start += chunk_size - overlap
    return chunks


async def index_document(file_path: Path, document_id: str, filename: str) -> dict:
    text = await extract_text(file_path)
    chunks = chunk_text(text)
    records = []
    for idx, chunk in enumerate(chunks):
        embedding = await embedding_service.embed_text(chunk)
        records.append({
            'id': f'{document_id}_{idx}',
            'content': chunk,
            'embedding': embedding,
            'metadata': {
                'document_id': document_id,
                'filename': filename,
                'chunk_id': idx,
                'file_type': file_path.suffix.lower().replace('.', ''),
                'source': filename,
                'page': 1,
            },
        })
    vector_store.add_documents(records)
    return {'document_id': document_id, 'chunk_count': len(chunks), 'records': records}


def is_duplicate_upload(file_path: Path) -> bool:
    digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
    return digest in {}


def validate_file(path: Path) -> None:
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError('Unsupported file extension.')
    if path.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError('File exceeds the maximum upload size.')
