from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core import logger_setup


class LogstashSettings(BaseSettings):
    host: str = Field()
    port: int = Field()

    model_config = SettingsConfigDict(env_prefix="logstash_")


class MongoSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="mongo_")


class Settings(BaseSettings):
    project_name: str = Field()
    logstash_logging_level: str = Field("INFO")
    console_logging_level: str = Field("DEBUG")
    rsa_public_path: str = Field()
    debug: bool = Field(False)

    mongo: ClassVar = MongoSettings()
    mongo_url: str = f"mongodb://{mongo.host}:{mongo.port}"
    logstash: ClassVar = LogstashSettings()


BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR.parent
settings = Settings()

logger_setup.configure_structlog(
    logstash_level=settings.logstash_logging_level,
    console_logging_level=settings.console_logging_level,
    logstash_host=settings.logstash.host,
    logstash_port=settings.logstash.port,
)
