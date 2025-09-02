import json
from pathlib import Path
from app.services.ingestion.preprocess.analyzer_upstage import LayoutAnalyzer

class DummyResp:
    status_code = 200
    def __init__(self, payload): self._p = payload
    def json(self): return self._p
    text = ""

def test_analyzer_mock(monkeypatch, tmp_path: Path):
    def fake_post(*a, **k): return DummyResp({"elements": [], "metadata": {"pages": []}})
    import requests
    monkeypatch.setattr(requests, "post", fake_post)

    src = Path(__file__).resolve().parents[2] / "test.pdf"  # 실제 파일 존재 필요 없음. open은 analyzer 내부에서 requests만 사용.
    # monkeypatch로 파일 open 경로를 대체하려면 더 감쌀 수 있지만 여기선 post만 목킹
    out = LayoutAnalyzer(api_key="x").analyze(src)
    assert Path(out).suffix == ".json"
    assert Path(out).exists()
    data = json.loads(Path(out).read_text(encoding="utf-8"))
    assert "elements" in data
