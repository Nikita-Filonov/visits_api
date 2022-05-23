from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.model import BaseModel


class UserPair(BaseModel):
    __tablename__ = 'user_pair'

    VIEW = 'View.UserPair'
    CREATE = 'Create.UserPair'
    DELETE = 'Delete.UserPair'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), comment='User')
    user = relationship('User')
    pair_id = Column(Integer, ForeignKey('pair.id', ondelete='CASCADE'), comment='Pair')
    pair = relationship('Pair')
