from pydantic import BaseModel, Field

from groups.schema.group import DefaultGroup
from users.schemas.users import DefaultUser


class CreateGroupUser(BaseModel):
    email: str
    group_id: int = Field(alias='groupId')


class DefaultGroupUser(BaseModel):
    id: int
    user: DefaultUser
    group: DefaultGroup

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
