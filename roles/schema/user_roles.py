from pydantic import BaseModel, Field


class CreateUserRole(BaseModel):
    user_id: int = Field(alias='userId')
    role_id: int = Field(alias='roleId')


class DefaultUserRole(CreateUserRole):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
