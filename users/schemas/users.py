from typing import Optional

from pydantic import BaseModel, Field, validator

from users.authentications.password import get_password_hash


class LoginUser(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    email: str = Field(min_length=8, max_length=70)
    username: str = Field(min_length=6, max_length=70)
    password: str

    # TODO добавить кастомный валидатор для пароля
    @validator('password')
    def validate_password(cls, value):
        return get_password_hash(value)


class DefaultUser(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True


class ConfirmUser(BaseModel):
    email: str
    code: Optional[str]


class UserNotFound(BaseModel):
    level: str = 'error'
    message: str = 'User with email "{0}" not found'
    args: list
