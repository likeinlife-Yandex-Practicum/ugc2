from fastapi import Query
from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    limit: int = Field(Query(ge=1, le=200, default=50))
    offset: int = Field(Query(ge=0, default=0))
