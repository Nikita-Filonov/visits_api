from sqlalchemy import Column, Integer, String

from models.model import BaseModel


class Group(BaseModel):
    __tablename__ = 'group'

    VIEW = 'View.Group'
    CREATE = 'Create.Group'
    DELETE = 'Delete.Group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), comment='Name')
