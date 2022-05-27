from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

from database import Base
from users.authentications.token import generate_token


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(40), comment='Значение токена', nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), comment='Пользователь', default=None)
    user = relationship('User')

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs) -> Optional['Token']:
        result = await session.execute(select(cls).filter_by(**kwargs).options(selectinload(cls.user)))
        return result.scalars().first()

    @classmethod
    async def create(cls, session: AsyncSession, user) -> 'Token':
        token = await generate_token()
        model = cls(value=token, user_id=user.id)
        session.add(model)
        await session.commit()

        return model
