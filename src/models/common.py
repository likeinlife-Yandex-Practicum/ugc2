import datetime
import uuid

from pydantic import BaseModel, Field


class HasTimeStamp(BaseModel):
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class HasUUIDId(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)  # type: ignore


class HasUserId(BaseModel):
    user_id: uuid.UUID = Field()
