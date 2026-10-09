from fastapi.testclient import TestClient

from app.main import app
from app.services import ollama_service as ollama_module
from app.services import retrieval_service as retrieval_module
from app.services import rag_service as rag_module

client = TestClient(app)


def test_health(monkeypatch) -> None:
    async def fake_check() -> bool:
        return True

    async def fake_list() -> list[str]:
        return ['qwen2.5:3b', 'llama3.2:3b']

    monkeypatch.setattr(ollama_module.ollama_service, 'check_connection', fake_check)
    monkeypatch.setattr(ollama_module.ollama_service, 'list_models', fake_list)
    response = client.get('/api/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'


def test_chat_endpoint(monkeypatch) -> None:
    async def fake_list() -> list[str]:
        return ['qwen2.5:3b']

    async def fake_search(*args, **kwargs):
        return []

    async def fake_answer(*args, **kwargs):
        return 'A list comprehension creates a new list in one readable line.'

    monkeypatch.setattr(ollama_module.ollama_service, 'list_models', fake_list)
    monkeypatch.setattr(retrieval_module.retrieval_service, 'search', fake_search)
    monkeypatch.setattr(rag_module.rag_service, 'answer_question', fake_answer)

    response = client.post('/api/chat', json={'question': 'What is a list comprehension?', 'selected_model': 'qwen2.5:3b'})
    assert response.status_code == 200
    payload = response.json()
    assert payload['active_model'] == 'qwen2.5:3b'
    assert 'list comprehension' in payload['answer'].lower()


def test_upload_document_endpoint(monkeypatch, tmp_path) -> None:
    async def fake_index(*args, **kwargs):
        return {'chunk_count': 1}

    monkeypatch.setattr('app.api.documents.index_document', fake_index)
    response = client.post('/api/documents/upload', files={'file': ('notes.txt', 'hello world', 'text/plain')})
    assert response.status_code == 200
    payload = response.json()
    assert payload['chunk_count'] == 1
