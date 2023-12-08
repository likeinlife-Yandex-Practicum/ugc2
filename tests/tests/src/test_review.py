import random
import uuid
from http import HTTPStatus

import httpx

from tests.enums import ApiRoute
from tests.settings import settings

from .misc import generate_string


def test_create(
    net_client: httpx.Client,
):
    content = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.REVIEW, json=content)
    assert response.status_code == HTTPStatus.CREATED
    review_id = response.json()["id"]

    response = net_client.get(ApiRoute.REVIEW)

    response = net_client.get(f"{ApiRoute.REVIEW}{review_id}/")
    response_json = response.json()
    assert response_json["id"] == review_id
    assert response_json["score"] == content["score"]
    assert response_json["film_id"] == str(content["film_id"])
    assert response_json["review"] == content["review"]
    assert response_json["user_id"] == str(settings.test_user.id)


def test_update(
    net_client: httpx.Client,
):
    content = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.REVIEW, json=content)
    assert response.status_code == HTTPStatus.CREATED
    review_id = response.json()["id"]

    params = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
    )
    response = net_client.patch(f"{ApiRoute.REVIEW}{review_id}/", params=params)  # type: ignore
    response_json = response.json()
    assert response_json["id"] == review_id
    assert response_json["score"] == params["score"]
    assert response_json["film_id"] == str(content["film_id"])
    assert response_json["review"] == params["review"]
    assert response_json["user_id"] == str(settings.test_user.id)


def test_delete(
    net_client: httpx.Client,
):
    content = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.REVIEW, json=content)
    assert response.status_code == HTTPStatus.CREATED
    review_id = response.json()["id"]

    response = net_client.delete(f"{ApiRoute.REVIEW}{review_id}/")
    assert response.status_code == HTTPStatus.OK

    response = net_client.get(f"{ApiRoute.REVIEW}{review_id}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_by_film_id(
    net_client: httpx.Client,
):
    content = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.REVIEW, json=content)
    assert response.status_code == HTTPStatus.CREATED
    review_id = response.json()["id"]

    response = net_client.get(f"{ApiRoute.REVIEW}film/{content['film_id']}/")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json) == 1
    r = response_json[0]
    assert r["id"] == review_id
