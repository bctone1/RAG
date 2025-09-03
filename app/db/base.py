from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except Exception:
    pass

DB = os.getenv("DB") or os.getenv("DB_DRIVER") or "postgresql+psycopg"

# 드라이버 스킴
DB = os.getenv("DB") or os.getenv("DB_DRIVER") or "postgresql+psycopg"

# .env 값
USER = os.getenv("POSTGRES_USER", "rag")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
NAME = os.getenv("POSTGRES_DB", "rag")

# DATABASE_URL이 있으면 우선 사용, 없으면 조합
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"{DB}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}",
)