from pydantic import BaseModel


class CreatePair(BaseModel):
    name: str


class DefaultPair(CreatePair):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
