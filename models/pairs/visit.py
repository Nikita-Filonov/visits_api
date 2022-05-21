from enum import Enum as LibEnum

from sqlalchemy import Column, Integer, DateTime, func, ForeignKey

from models.model import BaseModel


class VisitStates(int, LibEnum):
    WAS_ON_PAIR = 1
    MISSED_PAIR = 2
    ON_SICK_LEAVE = 3


class Visit(BaseModel):
    __tablename__ = 'visit'

    VIEW = 'View.Visit'
    CREATE = 'Create.Visit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(Integer, default=VisitStates.MISSED_PAIR.value, comment='State')
    when = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), comment='User')
    pair_id = Column(Integer, ForeignKey('pair.id'), comment='Pair')
