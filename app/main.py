from app.api.v1.router import router as v1
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import UPLOAD_FOLDER
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

# from app.api.v1.ingestion import router as ingestion_router

app = FastAPI()
app.include_router(v1, prefix="/api/v1")
app.mount("/file", StaticFiles(directory="file"), name="file")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용, 실제 운영 환경에서는 특정 도메인만 허용하는 것이 좋음
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


if __name__ == "__main__":
    # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=5000)


