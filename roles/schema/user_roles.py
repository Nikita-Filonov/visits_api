from pydantic import BaseModel


class CreateUserRole(BaseModel):
    user_id: int
    role_id: int


class DefaultUserRole(CreateUserRole):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
