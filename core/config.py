from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    be_api_url: str = "http://localhost:8000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.be_api_url.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        # "+asyncpg" tells SQLAlchemy to use the asyncpg driver, required
        # for create_async_engine to work with Postgres.
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


settings = get_settings()
