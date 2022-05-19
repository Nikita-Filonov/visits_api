from pydantic import BaseModel, Field


class CreateUserPair(BaseModel):
    user_id: int = Field(alias='userId')
    pair_id: int = Field(alias='pairId')


class DefaultUserPair(CreateUserPair):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
