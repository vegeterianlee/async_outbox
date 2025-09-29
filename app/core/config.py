from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="dev")

    # FastAPI
    API_TITLE: str
    API_VERSION: str

    # DB, Redis(브로커, 백엔드)
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


