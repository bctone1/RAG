import os
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",           # .env <- 이 경로를 탐색함
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",            # 정의되지 않은 키 무시
    )

    OPENAI_API_KEY: str | None = None
    # ANTHROPIC_API_KEY: str | None = None
    # GOOGLE_API_KEY: str | None = None
    FRIENDLI_API_KEY: str | None = None
    UPLOAD_FOLDER: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "file",
        "upload",
    )
    DEBUG: bool = False
    PORT: int = 5000
    DATABASE_URL: AnyUrl | None = None

settings = Settings()
