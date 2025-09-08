import types

from app.services.ingestion import embedding


def test_embed_text_returns_vector_and_meta(monkeypatch):
    class DummyEmbeddings:
        def create(self, model, input):
            class Resp:
                data = [types.SimpleNamespace(embedding=[0.1, 0.2, 0.3])]
            return Resp()

    class DummyClient:
        def __init__(self, api_key):
            self.embeddings = DummyEmbeddings()

    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(embedding, "OpenAI", DummyClient)
    vec, model, dim = embedding.embed_text("hello", model="test-model")
    assert vec == [0.1, 0.2, 0.3]
    assert model == "test-model"
    assert dim == 3