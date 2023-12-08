import random
import uuid
from http import HTTPStatus

import httpx

from tests.enums import ApiRoute
from tests.settings import settings


def test_pipeline(
    net_client: httpx.Client,
):
    content = dict(
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.BOOKMARK, json=content)
    assert response.status_code == HTTPStatus.CREATED
    bookmark_id = response.json()["id"]

    response = net_client.get(f"{ApiRoute.BOOKMARK}{bookmark_id}/")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == bookmark_id
    assert response_json["film_id"] == str(content["film_id"])
    assert response_json["user_id"] == str(settings.test_user.id)

    response = net_client.delete(f"{ApiRoute.BOOKMARK}{bookmark_id}/")
    assert response.status_code == HTTPStatus.OK

    response = net_client.get(f"{ApiRoute.BOOKMARK}{bookmark_id}/")
    assert response.status_code == HTTPStatus.NOT_FOUND
