from enum import Enum
from functools import lru_cache
from uuid import UUID

import jwt

from src.core.settings import settings

from .errors import InvalidJWTScopeError


class Scope(str, Enum):
    ACCESS_TOKEN = "access_token"  # noqa: S105


class JWTService:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def get_user_id(self, access_token: str) -> UUID:
        user_payload = self.decode_access_token(access_token)
        user_id = UUID(user_payload["sub"])
        return user_id

    def decode_access_token(self, access_token: str) -> dict:
        payload: dict = jwt.decode(access_token, self.public_key, algorithms=["RS256"])
        if payload["scope"] == Scope.ACCESS_TOKEN:
            return payload
        raise InvalidJWTScopeError


@lru_cache
def get_jwt_service() -> JWTService:
    with open(settings.rsa_public_path, "r") as pub_obj:
        return JWTService(public_key=pub_obj.read())
