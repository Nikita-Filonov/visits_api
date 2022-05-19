from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str


class DefaultGroup(CreateGroup):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
