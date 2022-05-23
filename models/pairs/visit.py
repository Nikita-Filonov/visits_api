from datetime import datetime, timedelta
from enum import Enum as LibEnum
from typing import Optional

from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Float
from sqlalchemy.ext.asyncio import AsyncSession

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
    score = Column(Float, default=None, comment='Score')
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), comment='User')
    pair_id = Column(Integer, ForeignKey('pair.id', ondelete='CASCADE'), comment='Pair')

    @classmethod
    async def get_to_day_visit(cls, session: AsyncSession, user_id: int, pair_id: int) -> Optional['Visit']:
        today = datetime.now()
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        return await Visit.get(
            session,
            user_id=user_id,
            pair_id=pair_id,
            clause_filter=(Visit.when >= start, Visit.when <= end)
        )
