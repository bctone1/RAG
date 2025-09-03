from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.db.models import Base
from dotenv import load_dotenv

load_dotenv(override=True)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

try:
    from app.core.settings import settings
    default_database_url = settings.DATABASE_URL
except Exception:
    try:
        from app.db.base import DATABASE_URL as default_database_url
    except Exception:
        default_database_url = None

database_url = os.getenv("DATABASE_URL", default_database_url or "")
if not database_url:
    raise RuntimeError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

