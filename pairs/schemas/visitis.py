from pydantic import BaseModel


class CreateVisit(BaseModel):
    when: str
    user_id: int


class DefaultVisit(CreateVisit):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
