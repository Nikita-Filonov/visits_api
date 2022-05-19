from pydantic import BaseModel


class DefaultPermission(BaseModel):
    id: int
    scope: str

    class Config:
        orm_mode = True
