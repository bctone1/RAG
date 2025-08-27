from __future__ import annotations
import json, os
from pathlib import Path
from typing import Union
import requests
from dotenv import load_dotenv
load_dotenv(override=True)

class LayoutAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _upstage_layout_analysis(self, input_file: Union[str, Path]) -> str:
        """
        레이아웃 분석 API 호출
        input_file: 분석할 PDF 파일 경로
        생성된 JSON 파일 경로 문자열
        """
        input_path = Path(input_file)

        url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        data = {"ocr": "false"}  # 필요 시 "true" 로 변경

        with input_path.open("rb") as f:
            response = requests.post(
                url,
                headers=headers,
                data=data,
                files={"document": f},
                timeout=120,
            )

        if response.status_code != 200:
            snippet = (response.text or "")[:200]
            raise ValueError(f"예상치 못한 상태 코드: {response.status_code} | {snippet}")

        output_path = input_path.with_suffix(".json")
        with output_path.open("w", encoding="utf-8") as out:
            json.dump(response.json(), out, ensure_ascii=False, indent=2)

        return str(output_path)

    def execute(self, input_file: Union[str, Path]) -> str:
        return self._upstage_layout_analysis(input_file)


# 사용 예시:
# analyzer = LayoutAnalyzer(os.environ.get("UPSTAGE_API_KEY", ""))
# result_json = analyzer.execute("path/to/file.pdf")
# print(result_json)


# from __future__ import annotations
# import os, json, requests
# from pathlib import Path
# from typing import Optional
#
# class LayoutAnalyzer:
#     def __init__(self, api_key: Optional[str] = None):
#         self.api_key = api_key or os.getenv("UPSTAGE_API_KEY")
#         if not self.api_key:
#             raise RuntimeError("UPSTAGE_API_KEY 누락")
#
#     def analyze(self, input_pdf: str | Path, ocr: bool = False) -> str:
#         """PDF 1개를 분석해 같은 prefix의 JSON을 생성하고 JSON 경로 반환"""
#         input_pdf = Path(input_pdf)
#         url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
#         with open(input_pdf, "rb") as f:
#             r = requests.post(
#                 url,
#                 headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
#                 data={"ocr": str(bool(ocr)).lower()},
#                 files={"document": f},
#                 timeout=120,
#             )
#         if r.status_code != 200:
#             raise ValueError(f"Layout API 실패: {r.status_code} {r.text[:200]}")
#         out = input_pdf.with_suffix(".json")
#         with open(out, "w", encoding="utf-8") as fp:
#             json.dump(r.json(), fp, ensure_ascii=False, indent=2)
#         return str(out)