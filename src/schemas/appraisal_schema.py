import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, Field


class AppraisalSchema(BaseModel):
    score: Literal[0, 1] = Field()
    user_id: uuid.UUID = Field()
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class ReviewAppraisalSchema(BaseModel):
    id: uuid.UUID
    appraisal: AppraisalSchema


class AppraisalAddSchema(BaseModel):
    score: Literal[0, 1] = Field()


class AppraisalUpdateSchema(BaseModel):
    score: Literal[0, 1] = Field()
