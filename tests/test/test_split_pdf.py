from pathlib import Path
from app.services.ingestion.preprocess.split_pdf import split_pdf

def test_split_pdf(tmp_path: Path):
    # 준비: 샘플 PDF 복사
    src = Path("../../test.pdf")
    out = tmp_path
    parts = split_pdf(src, out_dir=out, batch_size=5)
    assert len(parts) >= 1
    for p in parts:
        assert Path(p).exists()
