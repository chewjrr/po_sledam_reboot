from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"


settings = Settings()