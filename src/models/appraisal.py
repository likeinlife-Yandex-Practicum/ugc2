from typing import Literal

from pydantic import BaseModel, Field

from .common import HasTimeStamp, HasUserId, HasUUIDId


class Appraisal(HasTimeStamp, HasUserId, HasUUIDId, BaseModel):
    score: Literal[0, 1] = Field()
