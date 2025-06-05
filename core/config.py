from dataclasses import dataclass, field

from pydantic import PostgresDsn, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class DBaseConfig:
    url: PostgresDsn

    naming_convention: dict[str, str] = field(
        default_factory=lambda: {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    access_token: AccessToken
    db: DBaseConfig

    origins: list[str] = field(
        default_factory=lambda: [
            "http://localhost:8081",
            "http://localhost:8080",
            "http://localhost:3000",
        ]
    )

    MONGO_DB_URL: str = Field(default="mongodb://admin:admin@mongodb:27017/")
    MONGO_DB_NAME: str = Field(default="test")
    ELASTICSEARCH_HOST: str = Field(default="elasticsearch")
    ELASTICSEARCH_PORT: str = Field(default="9200")
    ELASTIC_INDEX: str = "images"
    REDIS_PORT: str = Field(default="6379")
    REDIS_HOST: str = "redis"
    DH_PRIME_P: str = "1234567890123456789012345678901234567890"
    DH_GENERATOR_G: str = "2"


settings = Settings()
