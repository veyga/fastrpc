import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
