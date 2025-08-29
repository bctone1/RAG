from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",           # .env 허용
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",            # 정의되지 않은 키 무시
    )

    OPENAI_API_KEY: str
    FRIENDLI_API_KEY: str
    UPLOAD_FOLDER: str = "./file/upload"
    DEBUG: bool = False
    PORT: int = 5000
    DATABASE_URL: AnyUrl | None = None

settings = Settings()
