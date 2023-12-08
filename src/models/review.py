import uuid

import pymongo
from pydantic import Field

from .appraisal import Appraisal
from .base import MongoBaseDocument


class Review(MongoBaseDocument):
    score: int = Field(ge=0, le=10)
    review: str = Field(max_length=500)
    film_id: uuid.UUID = Field()
    appraisals: list[Appraisal] = Field(default_factory=list)

    class Settings:
        indexes = [
            pymongo.IndexModel(
                ["film_id", "user_id"],
                unique=True,
            ),
        ]
