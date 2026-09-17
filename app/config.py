from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lista de Compras API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./banco.db"
    SECRET_KEY: str = "change-me-in-production"
    DEBUG: bool = False

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
