from functools import lru_cache
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Backend Boilerplate"
    db_server: str = os.environ.get("DB_SERVER")
    db_hostname: str = os.environ.get("DB_HOSTNAME")
    db_database: str = os.environ.get("DB_DATABASE")
    db_username: str = os.environ.get("DB_USERNAME")
    db_password: str = os.environ.get("DB_PASSWORD")
    db_port: int = 3306
    db_sslmode: bool = True


@lru_cache
def get_settings():
    return Settings()
