from typing import Optional, List

from pydantic import BaseModel, Field

from pairs.schemas.pairs import DefaultPair
from pairs.schemas.visitis import DefaultVisit
from users.schemas.users import DefaultUser


class CreateUserPair(BaseModel):
    users: List[int]
    pair_id: int = Field(alias='pairId')


class CreateGroupUserPair(BaseModel):
    groups: List[int] = Field(alias='groups')
    pair_id: int = Field(alias='pairId')


class DefaultUserPair(BaseModel):
    id: int
    user: DefaultUser
    pair: DefaultPair
    visit: Optional[DefaultVisit]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
