from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str | None = None
    DATABASE_URL_SYNC: str | None = None
    PROJECT_NAME: str = "Persoon FastAPI"
    APP_VERSION: str | None = None
    GIT_BRANCH: str | None = None
    GIT_COMMIT: str | None = None
    BUILD_TIME: str | None = None
    DEBUG: bool = False
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    FRONTEND_DIR: str = "frontend"

    @property
    def sqlalchemy_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        raise NotImplementedError("DATABASE_URL must be set in the .env file.")


@lru_cache()
def get_settings() -> Settings:
    """Get cached Settings instance (use in dependencies)."""
    return Settings()

