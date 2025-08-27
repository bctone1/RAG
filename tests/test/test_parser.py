import json
from pathlib import Path
from app.services.ingestion import parser

def test_parser_pipeline(tmp_path, monkeypatch):
    pdf = Path("../../test.pdf")

    # split 목킹
    monkeypatch.setattr(parser, "split_pdf", lambda *a, **k: [str(tmp_path / "part_0000_0009.pdf")])
    # analyzer 목킹
    class DummyAnalyzer:
        def __init__(self, api_key=None): pass
        def analyze(self, p):
            j = Path(str(p).replace(".pdf",".json"))
            j.write_text(json.dumps({"elements":[],"metadata":{"pages":[]}}), encoding="utf-8")
            return str(j)
    monkeypatch.setattr(parser, "LayoutAnalyzer", DummyAnalyzer)
    # extract 목킹
    monkeypatch.setattr(parser, "extract_blocks_and_images", lambda **k: ([{"text":"t","block_type":"text","page_num":1}], []))

    out = parser.parse_to_md_html(pdf, work_dir=tmp_path, upstage_key="x", batch_size=10)
    assert Path(out["html_path"]).exists()
    assert Path(out["md_path"]).exists()
    assert out["blocks"]
