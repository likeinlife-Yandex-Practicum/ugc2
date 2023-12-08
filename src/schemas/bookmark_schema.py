import datetime
import uuid

from pydantic import BaseModel, Field


class BookmarkSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)  # type: ignore
    film_id: uuid.UUID = Field()
    user_id: uuid.UUID = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class BookmarkAddSchema(BaseModel):
    film_id: uuid.UUID = Field()


class BookmarkCreatedSchema(BaseModel):
    id: uuid.UUID
