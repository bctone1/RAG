import os
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_upload_file_returns_file_id(tmp_path):
    # 임시 스토리지 및 데이터베이스 설정
    storage_root = tmp_path / "ingestion_storage"
    os.environ["INGESTION_STORAGE"] = str(storage_root)
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    # import after env vars set
    from fastapi import FastAPI
    from app.api.v1.ingestion import router as ingestion_router
    from app.db.session import get_db

    app = FastAPI()
    app.include_router(ingestion_router, prefix="/api/v1")

    engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
    # SQLite에서 BigInteger 자동 증가 문제를 피하기 위해 수동으로 테이블 생성
    with engine.begin() as conn:
        conn.exec_driver_sql(
            """
            CREATE TABLE files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_name VARCHAR NOT NULL,
                mime_type VARCHAR NOT NULL,
                storage_path VARCHAR NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
            """
        )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    files = {"file": ("sample.pdf", b"%PDF-1.4 test", "application/pdf")}
    res = client.post("/api/v1/ingestion/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "file_id" in data
    assert isinstance(data["file_id"], int)
    # 파일이 지정된 디렉토리에 저장되었는지도 확인
    saved_file = Path(data["path"])
    assert saved_file.exists()