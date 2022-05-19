from typing import Optional

from sqlalchemy import Column, Integer, String, JSON, Boolean, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base
from users.schemas.users import CreateUser


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(70), comment='Username', nullable=False)
    email = Column(String(70), comment='Email', nullable=False, unique=True)
    password = Column(String(200), comment='Пароль', nullable=False)
    token = Column(String(500), comment='Push notification token', default=None)
    confirmation_codes = Column(JSON, comment='Коды подтверждений', default=[])
    staff = Column(Boolean, default=False)  # a admin user; non super-user
    admin = Column(Boolean, default=False)  # a superuser+
    is_active = Column(Boolean, default=False)
    is_email_confirmed = Column(Boolean, default=False)

    @classmethod
    async def create(cls, session: AsyncSession, user: CreateUser) -> 'User':
        model = cls(**user.dict())
        session.add(model)
        await session.commit()

        return model

    @classmethod
    async def get(cls, session: AsyncSession, *args, **kwargs) -> Optional['User']:
        result = await session.execute(select(cls).filter_by(**kwargs).filter(*args))
        return result.scalars().first()

    @classmethod
    async def update(cls, session: AsyncSession, user: 'User', **kwargs) -> None:
        await session.execute(update(cls).filter_by(id=user.id).values(**kwargs))
        await session.commit()
