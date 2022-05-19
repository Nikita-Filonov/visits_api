from sqlalchemy import Column, Integer, ForeignKey

from models.model import BaseModel


class UserRole(BaseModel):
    __tablename__ = 'user_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))
