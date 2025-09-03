import os
from sqlalchemy import create_engine
from app.core.settings import settings

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")

engine = create_engine(
    f"postgresql+psycopg://postgres:3636@localhost:5432/postgres"
)

with engine.connect() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
