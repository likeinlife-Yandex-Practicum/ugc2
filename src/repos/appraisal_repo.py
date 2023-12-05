import datetime
import uuid
from typing import Any, Literal

import structlog
from beanie.operators import NE, And, Pull, Push, Set
from fastapi import Depends
from motor.core import AgnosticClient, AgnosticCollection
from pydantic import TypeAdapter

from src.db.mongo import get_mongo_client
from src.models import Appraisal

from .errors import AppraisalNotFoundError, ReviewNotFoundError


class AppraisalRepo:
    """Implement appraisal CRUD."""

    def __init__(self, logger: Any, collection: AgnosticCollection) -> None:
        self._logger = logger
        self.collection = collection

    async def get_by_review_id(
        self,
        review_id: uuid.UUID,
        limit: int,
        offset: int,
    ) -> list[Appraisal]:
        review_list = await self.collection.aggregate(
            [
                {
                    "$match": {"_id": review_id},
                },
                {
                    "$project": {
                        "_id": 0,
                        "appraisals": {
                            "$slice": ["$appraisals", offset, limit],
                        },
                    },
                },
            ],
        ).to_list(1)
        if not review_list:
            raise ReviewNotFoundError
        appraisal_list = TypeAdapter(list[Appraisal]).validate_python(review_list[0].get("appraisals"))

        self._logger.info("Get list by review")
        self._logger.debug(review_list)
        return appraisal_list

    async def add(
        self,
        review_id: uuid.UUID,
        score: Literal[0, 1],
        user_id: uuid.UUID,
    ) -> uuid.UUID:
        appraisal = Appraisal(
            score=score,
            review_id=review_id,
            user_id=user_id,
        )

        result = await self.collection.update_one(
            And({"_id": review_id}, NE("appraisals.user_id", user_id)),
            Push(
                {
                    "appraisals": appraisal.model_dump(),
                },
            ),
        )

        self._logger.debug(result)
        if not result.modified_count:
            raise ReviewNotFoundError

        self._logger.info("Add", id=appraisal.id)
        return appraisal.id

    async def delete(
        self,
        review_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        result = await self.collection.update_one(
            {"_id": review_id},
            Pull(
                {
                    "appraisals": {"user_id": user_id},
                },
            ),
        )
        self._logger.debug(result)
        if not result.modified_count:
            raise AppraisalNotFoundError
        self._logger.info("Delete", user_id=user_id)

    async def update(
        self,
        review_id: uuid.UUID,
        user_id: uuid.UUID,
        score: Literal[0, 1],
    ) -> None:
        result = await self.collection.update_one(
            {
                "appraisals.user_id": user_id,
                "_id": review_id,
            },
            Set(
                {
                    "appraisals.$.score": score,
                    "appraisals.$.updated_at": datetime.datetime.now(),
                },
            ),
        )
        self._logger.debug(result)
        if not result.modified_count:
            raise AppraisalNotFoundError
        self._logger.info("Update", id=user_id)


def get_appraisal_repo(
    client: AgnosticClient = Depends(get_mongo_client),
) -> AppraisalRepo:
    logger = structlog.get_logger()
    collection = client.get_database("ugc").get_collection("Review")
    return AppraisalRepo(logger=logger, collection=collection)  # type: ignore
