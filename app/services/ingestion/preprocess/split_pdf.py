from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def split_pdf(src: str | Path,
              out_dir: str | Path | None = None,
              batch_size: int = 10,
              password: str | None = None) -> list[str]:

    src = Path(src)
    assert src.suffix.lower() == ".pdf", "PDF만 허용"
    out_dir = Path(out_dir or src.parent)
    out_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(src))
    if reader.is_encrypted:
        if not password:
            raise ValueError("암호화된 PDF. password 필요")
        reader.decrypt(password)

    n = len(reader.pages)
    ret: list[str] = []
    for start in range(0, n, batch_size):
        end = min(start + batch_size, n) - 1
        out = out_dir / f"{src.stem}_{start:04d}_{end:04d}.pdf"
        writer = PdfWriter()
        for i in range(start, end + 1):
            writer.add_page(reader.pages[i])
        with open(out, "wb") as f:
            writer.write(f)
        ret.append(str(out))
    return ret
