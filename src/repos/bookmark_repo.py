import uuid
from typing import Any

import pymongo.errors
import structlog

from src.models import Bookmark

from .errors import BookmarkAlreadyExistsError, BookmarkNotFoundError


class BookmarkRepo:
    """Implement Bookmark CRUD."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger

    async def get(self, id_: uuid.UUID) -> Bookmark:
        bookmark = await Bookmark.get(id_)
        if not bookmark:
            raise BookmarkNotFoundError
        self._logger.info("Get", id=id_)
        return bookmark

    async def get_list(self, limit: int, offset: int) -> list[Bookmark]:
        bookmark_list = await Bookmark.find(limit=limit, skip=offset).to_list()
        self._logger.info("Get list")
        return bookmark_list

    async def get_list_by_user_id(
        self,
        user_id: uuid.UUID,
        limit: int,
        offset: int,
    ) -> list[Bookmark]:
        bookmark_list = await Bookmark.find(
            Bookmark.user_id == user_id,
            limit=limit,
            skip=offset,
        ).to_list()
        self._logger.info("Get list")
        return bookmark_list

    async def add(
        self,
        film_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> uuid.UUID:
        bookmark = Bookmark(
            film_id=film_id,
            user_id=user_id,
        )

        try:
            await bookmark.insert()
        except pymongo.errors.DuplicateKeyError:
            raise BookmarkAlreadyExistsError
        self._logger.info("Add", id=bookmark.id)
        return bookmark.id

    async def delete(self, id_: uuid.UUID) -> None:
        bookmark = await Bookmark.get(id_)
        if not bookmark:
            raise BookmarkNotFoundError
        self._logger.info("Delete", id=id_)
        await bookmark.delete()


def get_bookmark_repo() -> BookmarkRepo:
    logger = structlog.get_logger()
    return BookmarkRepo(logger=logger)
