from typing import List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_PREFIX: str = '/api/v1'
    PROJECT_NAME: str = ''
    DATABASE_DSN: PostgresDsn
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings = Settings()
