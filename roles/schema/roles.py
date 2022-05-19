from pydantic import BaseModel


class CreateRole(BaseModel):
    name: str


class DefaultRole(CreateRole):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
