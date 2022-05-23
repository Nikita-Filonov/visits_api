from sqlalchemy import Column, Integer, String, JSON, Boolean, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import BaseModel


class User(BaseModel):
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
    async def update(cls, session: AsyncSession, user: 'User', **kwargs) -> None:
        await session.execute(update(cls).filter_by(id=user.id).values(**kwargs))
        await session.commit()
