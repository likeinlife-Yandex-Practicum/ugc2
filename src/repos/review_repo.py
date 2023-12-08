import datetime
import uuid
from typing import Any, Optional

import pymongo.errors
import structlog

from src.models import Review

from .errors import ReviewAlreadyExistsError, ReviewNotFoundError


class ReviewRepo:
    """Implement review CRUD."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger

    async def get(self, id_: uuid.UUID) -> Review:
        review = await Review.get(id_)
        if not review:
            raise ReviewNotFoundError
        self._logger.info("Get", id=id_)
        return review

    async def get_list(self, limit: int, offset: int) -> list[Review]:
        review_list = await Review.find(limit=limit, skip=offset).to_list()
        self._logger.info("Get list")
        return review_list

    async def get_list_by_user_id(
        self,
        user_id: uuid.UUID,
        limit: int,
        offset: int,
    ) -> list[Review]:
        review_list = await Review.find(
            Review.user_id == user_id,
            limit=limit,
            skip=offset,
        ).to_list()
        self._logger.info("Get list by user-id")
        return review_list

    async def get_list_by_film_id(
        self,
        film_id: uuid.UUID,
        limit: int,
        offset: int,
    ) -> list[Review]:
        review_list = await Review.find(
            Review.film_id == film_id,
            limit=limit,
            skip=offset,
        ).to_list()
        self._logger.info("Get list by film-id")
        return review_list

    async def add(
        self,
        score: int,
        review_string: str,
        film_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> uuid.UUID:
        review = Review(
            score=score,
            review=review_string,
            film_id=film_id,
            user_id=user_id,
        )
        try:
            await review.insert()
        except pymongo.errors.DuplicateKeyError:
            raise ReviewAlreadyExistsError
        self._logger.info("Add", id=review.id)
        return review.id

    async def delete(self, id_: uuid.UUID) -> None:
        review = await Review.get(id_)
        if not review:
            raise ReviewNotFoundError
        self._logger.info("Delete", id=id_)
        await review.delete()

    async def update(
        self,
        id_: uuid.UUID,
        score: Optional[int] = None,
        review_string: Optional[str] = None,
    ) -> Review:
        review = await Review.get(id_)
        if not review:
            raise ReviewNotFoundError
        if score:
            review.score = score
        if review_string:
            review.review = review_string
        review.updated_at = datetime.datetime.now()

        await review.save()
        self._logger.info("Update", id=id_)
        return review


def get_review_repo() -> ReviewRepo:
    logger = structlog.get_logger()
    return ReviewRepo(logger=logger)
