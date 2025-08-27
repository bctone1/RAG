from __future__ import annotations
import os, json, requests
from pathlib import Path
from typing import Optional

class LayoutAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("UPSTAGE_API_KEY")
        if not self.api_key:
            raise RuntimeError("UPSTAGE_API_KEY 누락")

    def analyze(self, input_pdf: str | Path, ocr: bool = False) -> str:
        """PDF 1개를 분석해 같은 prefix의 JSON을 생성하고 JSON 경로 반환"""
        input_pdf = Path(input_pdf)
        url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
        with open(input_pdf, "rb") as f:
            r = requests.post(
                url,
                headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
                data={"ocr": str(bool(ocr)).lower()},
                files={"document": f},
                timeout=120,
            )
        if r.status_code != 200:
            raise ValueError(f"Layout API 실패: {r.status_code} {r.text[:200]}")
        out = input_pdf.with_suffix(".json")
        with open(out, "w", encoding="utf-8") as fp:
            json.dump(r.json(), fp, ensure_ascii=False, indent=2)
        return str(out)
