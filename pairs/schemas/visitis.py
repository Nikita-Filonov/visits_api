from datetime import datetime

from pydantic import BaseModel, Field


class CreateVisit(BaseModel):
    when: datetime
    user_id: int = Field(alias='userId')
    pair_id: int = Field(alias='pairId')


class DefaultVisit(CreateVisit):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
