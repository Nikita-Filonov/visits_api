from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.pairs.visit import VisitStates


class CreateVisit(BaseModel):
    when: datetime
    state: VisitStates
    score: Optional[float]
    user_id: int = Field(alias='userId')
    pair_id: int = Field(alias='pairId')


class DefaultVisit(CreateVisit):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
