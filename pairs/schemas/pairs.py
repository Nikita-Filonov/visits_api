from datetime import time
from typing import Optional

from pydantic import BaseModel, Field


class CreatePair(BaseModel):
    name: str
    room: Optional[str]
    start_at: Optional[time] = Field(alias='startAt')
    end_at: Optional[time] = Field(alias='endAt')


class DefaultPair(CreatePair):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
