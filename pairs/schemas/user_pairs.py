from typing import Optional

from pydantic import BaseModel, Field

from pairs.schemas.pairs import DefaultPair
from pairs.schemas.visitis import DefaultVisit
from users.schemas.users import DefaultUser


class CreateUserPair(BaseModel):
    email: str
    pair_id: int = Field(alias='pairId')


class CreateGroupUserPair(BaseModel):
    group_id: int = Field(alias='groupId')
    pair_id: int = Field(alias='pairId')


class DefaultUserPair(BaseModel):
    id: int
    user: DefaultUser
    pair: DefaultPair
    visit: Optional[DefaultVisit]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
