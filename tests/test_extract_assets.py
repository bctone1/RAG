import json
from pathlib import Path
from app.services.ingestion.preprocess.extract_assets import extract_blocks_and_images

def test_extract_blocks_and_images(tmp_path: Path, monkeypatch):
    pdf = Path("test.pdf")
    jp = tmp_path / "part_0000_0009.json"
    jp.write_text(json.dumps({"elements": [], "metadata": {"pages":[{"page":1,"width":612,"height":792}]}}), encoding="utf-8")

    # 페이지 이미지를 실제로 만들지 않도록 pdf_page_to_image 목킹 가능
    from app.services.ingestion.preprocess import extract_assets as m
    monkeypatch.setattr(m, "pdf_page_to_image", lambda *a, **k: __import__("PIL").Image.new("RGB",(100,100)))

    blocks, images = extract_blocks_and_images(pdf, [jp], tmp_path)
    assert isinstance(blocks, list)
    assert isinstance(images, list)
