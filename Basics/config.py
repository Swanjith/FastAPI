from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Tetherfi Basics"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    DEFAULT_LIMIT: int = 10
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
