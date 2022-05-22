from enum import Enum

from sqlalchemy import Column, Integer, String

from models.model import BaseModel


class Roles(Enum):
    LEARNER = 'Learner'
    INSTRUCTOR = 'Instructor'


class Role(BaseModel):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), comment='Name')
