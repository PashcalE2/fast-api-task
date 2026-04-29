from datetime import time
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, PostgresDsn


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BACKEND_",
        extra="ignore",
        case_sensitive=False,
    )

    port: int
    workers: int


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        extra="ignore",
        case_sensitive=False,
    )

    name: str
    host: str
    port: int
    user: str
    password: str

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="ignore",
        case_sensitive=False,
    )

    host: str
    port: int
    expiration_at: time
    max_connections: int = 10
    decode_responses: bool = True

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return f"redis://{self.host}:{self.port}"


class Settings(BaseSettings):
    backend: BackendSettings = BackendSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
