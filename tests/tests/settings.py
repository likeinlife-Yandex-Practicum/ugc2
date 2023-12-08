import uuid
from datetime import timedelta
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestUserSettings(BaseSettings):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str = Field("example@mail.ru")
    roles: list[str] = Field(["user"])


class JWTSettings(BaseSettings):
    access_token_lifetime: timedelta = timedelta(hours=6)
    rsa_private_path: str = Field()


class ApiSettings(BaseSettings):
    root_url: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_")


class Settings(BaseSettings):
    api: ClassVar = ApiSettings()
    jwt: ClassVar = JWTSettings()
    test_user: ClassVar = TestUserSettings()

    api_base_url: str = f"{api.root_url}/api/v1"


settings = Settings()
