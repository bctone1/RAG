from app.services.ingestion.chunking import chunk_text


def test_chunk_text_splits_and_orders():
    text = "A" * 1200
    chunks = chunk_text(text, size=500)
    assert len(chunks) == 3
    assert chunks[0]["order"] == 1
    assert chunks[1]["order"] == 2
    assert chunks[2]["order"] == 3
    assert chunks[0]["text"] == "A" * 500
    assert chunks[-1]["text"] == "A" * 200