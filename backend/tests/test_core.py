from app.services.document_service import chunk_text


def test_chunk_text_generates_expected_slices() -> None:
    text = 'word ' * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=150)
    assert len(chunks) > 1
    assert all(len(chunk) <= 800 for chunk in chunks)
    assert chunks[0].startswith('word')
