from pathlib import Path
from app.services.ingestion.preprocess.render_html_md import render_all

def test_render_all(tmp_path: Path):
    blocks = [{"text":"hello","block_type":"text","page_num":1}]
    res = render_all(blocks, tmp_path, "sample")
    assert Path(res["html_path"]).exists()
    assert Path(res["md_path"]).exists()
