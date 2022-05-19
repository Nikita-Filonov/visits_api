from typing import Optional

from pydantic import BaseModel, Field


class CreateCourse(BaseModel):
    title: str
    image: Optional[str]
    description: str


class DefaultCourse(CreateCourse):
    id: int
    content: Optional[str]
    editor_content: Optional[str] = Field(alias='editorContent')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UpdateCourse(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    content: Optional[str]
    editor_content: Optional[str] = Field(alias='editorContent')


class AuthenticationRequired(BaseModel):
    email: str
