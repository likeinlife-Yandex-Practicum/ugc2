import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from ..models.appraisal import Appraisal


class ReviewSchema(BaseModel):
    id: uuid.UUID
    score: int
    review: str = Field(max_length=500)
    film_id: uuid.UUID
    user_id: uuid.UUID
    appraisals: list[Appraisal]
    created_at: datetime.datetime
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class ReviewAddSchema(BaseModel):
    score: int
    review: str = Field(max_length=500)
    film_id: uuid.UUID


class ReviewUpdateSchema(BaseModel):
    score: Optional[int] = None
    review: Optional[str] = Field(None, max_length=500)


class ReviewCreatedSchema(BaseModel):
    id: uuid.UUID
