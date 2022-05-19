from sqlalchemy import Column, Integer, String

from models.model import BaseModel


class Pair(BaseModel):
    __tablename__ = 'pair'

    CREATE = 'Create.Pair'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), comment='Name')
