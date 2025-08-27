from typing import List, Optional, Dict
from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str
    path: str
    size: int

class SplitRequest(BaseModel):
    pdf_path: str
    batch_size: int = 10

class SplitResponse(BaseModel):
    parts: List[str]

class AnalyzeRequest(BaseModel):
    pdf_paths: List[str]
    upstage_api_key: Optional[str] = None  # 없으면 환경변수 사용

class AnalyzeResponse(BaseModel):
    json_paths: Dict[str, str]  # {pdf_path: json_path}

class ExtractRequest(BaseModel):
    pdf_path: str  # 같은 prefix의 *.json 을 자동 탐색

class ExtractResponse(BaseModel):
    output_folder: str
    images: List[str]
    html_path: str
    md_path: str

class RunRequest(BaseModel):
    pdf_path: str
    batch_size: int = 10
    upstage_api_key: Optional[str] = None

class RunResponse(BaseModel):
    parts: List[str]
    json_paths: Dict[str, str]
    output_folder: str
    html_path: str
    md_path: str
    images: List[str]
