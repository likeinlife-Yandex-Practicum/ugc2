import random
import uuid
from dataclasses import dataclass
from http import HTTPStatus

import httpx
import pytest

from tests.enums import ApiRoute
from tests.settings import settings

from .misc import generate_string


@dataclass
class Review:
    id: str
    score: int
    review: str
    film_id: str


@pytest.fixture
def review_fixture(net_client: httpx.Client) -> Review:
    content = dict(
        score=random.randint(0, 10),
        review=generate_string(15),
        film_id=str(uuid.uuid4()),
    )

    response = net_client.post(ApiRoute.REVIEW, json=content)
    review_id = response.json()["id"]
    return Review(id=review_id, **content)  # type: ignore


def test_create(
    net_client: httpx.Client,
    review_fixture: Review,
):
    content = dict(
        score=random.randint(0, 1),
    )

    response = net_client.post(f"{ApiRoute.APPRAISAL}{review_fixture.id}/", json=content)
    assert response.status_code == HTTPStatus.CREATED

    params = dict(limit=50, offset=0)
    response = net_client.get(f"{ApiRoute.APPRAISAL}{review_fixture.id}/", params=params)
    assert len(response.json()) == 1
    r = response.json()[0]
    assert r["score"] == content["score"]
    assert r["user_id"] == str(settings.test_user.id)


def test_update(
    net_client: httpx.Client,
    review_fixture: Review,
):
    content = dict(
        score=random.randint(0, 1),
    )

    response = net_client.post(f"{ApiRoute.APPRAISAL}{review_fixture.id}/", json=content)
    assert response.status_code == HTTPStatus.CREATED

    content = dict(score=random.randint(0, 1))
    response = net_client.patch(f"{ApiRoute.APPRAISAL}{review_fixture.id}/", json=content)
    assert response.status_code == HTTPStatus.OK

    response = net_client.get(f"{ApiRoute.APPRAISAL}{review_fixture.id}/")
    assert response.status_code == HTTPStatus.OK
    r = response.json()[0]
    assert r["score"] == content["score"]
    assert r["user_id"] == str(settings.test_user.id)


def test_delete(
    net_client: httpx.Client,
    review_fixture: Review,
):
    content = dict(
        score=random.randint(0, 1),
    )

    response = net_client.post(f"{ApiRoute.APPRAISAL}{review_fixture.id}/", json=content)
    assert response.status_code == HTTPStatus.CREATED

    content = dict(score=random.randint(0, 1))
    response = net_client.delete(f"{ApiRoute.APPRAISAL}{review_fixture.id}/")
    assert response.status_code == HTTPStatus.OK

    response = net_client.get(f"{ApiRoute.APPRAISAL}{review_fixture.id}/")
    assert response.status_code == HTTPStatus.NOT_FOUND
