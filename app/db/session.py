from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings
import base as base
import psycopg2
engine = create_engine(str(settings.DATABASE_URL), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_connection():
    return psycopg2.connect(
        host=base.server,
        dbname=base.name,
        user=base.user,
        password=base.pw,
        port=base.port,
    )

