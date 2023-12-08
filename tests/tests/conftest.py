import uuid
from typing import Any, Callable

import httpx
import pytest

from .jwt_service import get_jwt_service
from .settings import settings


@pytest.fixture
def access_token() -> str:
    jwt_service = get_jwt_service()
    return jwt_service.encode_access_token(
        str(settings.test_user.id),
        settings.test_user.email,
        settings.test_user.roles,
    )


@pytest.fixture
def net_client(access_token) -> httpx.Client:
    cookies = dict(access_token=access_token)
    return httpx.Client(
        base_url=settings.api_base_url,
        cookies=cookies,
    )
