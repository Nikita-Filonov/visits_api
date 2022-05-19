from sqlalchemy import Column, Integer, String

from models.model import BaseModel


class Permission(BaseModel):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scope = Column(String(250), comment='Scope to allow')
