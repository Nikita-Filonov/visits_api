from pydantic import BaseModel, Field


class CreateUserPair(BaseModel):
    user_id: int = Field(alias='userId')
    pair_id: int = Field(alias='pairId')
