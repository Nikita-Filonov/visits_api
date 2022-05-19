from sqlalchemy import Column, Integer, DateTime, func, ForeignKey

from models.model import BaseModel


class Visit(BaseModel):
    __tablename__ = 'visit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    when = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
