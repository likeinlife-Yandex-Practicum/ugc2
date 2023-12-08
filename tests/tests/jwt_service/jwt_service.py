import uuid
from datetime import datetime, timedelta

import jwt

from tests.settings import settings


class JWTService:
    def __init__(
        self,
        private_key: str,
        access_token_lifetime: timedelta,
    ) -> None:
        self.private_key = private_key
        self.access_token_lifetime = access_token_lifetime

    def encode_access_token(self, user_id: str, email: str, roles: list[str]) -> str:
        payload = {
            "exp": datetime.utcnow() + self.access_token_lifetime,
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": user_id,
            "email": email,
            "roles": roles,
            "jti": str(uuid.uuid4()),
        }

        return jwt.encode(
            payload=payload,
            key=self.private_key,
            algorithm="RS256",
        )


def get_jwt_service() -> JWTService:
    with open(settings.jwt.rsa_private_path, "r") as priv_obj:
        return JWTService(
            private_key=priv_obj.read(),
            access_token_lifetime=settings.jwt.access_token_lifetime,
        )
