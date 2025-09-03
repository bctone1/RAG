from __future__ import annotations
from sqlalchemy.orm import declarative_base
import os
# from dotenv import load_dotenv

Base = declarative_base()

# try:
#     from dotenv import load_dotenv
#     load_dotenv(override=True)
# except Exception:
#     pass

DB = os.getenv("DB") or os.getenv("DB_DRIVER") or "postgresql+psycopg"

# .env 값
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
NAME = os.getenv("POSTGRES_DB")

# DATABASE_URL이 있으면 우선 사용, 없으면 조합
DATABASE_URL = os.getenv("DATABASE_URL",
    f"{DB}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}",
)