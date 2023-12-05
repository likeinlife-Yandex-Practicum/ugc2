import uuid

import pymongo
from pydantic import Field

from .base import MongoBaseDocument


class Bookmark(MongoBaseDocument):
    film_id: uuid.UUID = Field()

    class Settings:
        indexes = [
            pymongo.IndexModel(
                ["film_id", "user_id"],
                unique=True,
            ),
        ]
