from sqlalchemy import Column, Integer, DateTime, func, ForeignKey

from models.model import BaseModel


class Visit(BaseModel):
    __tablename__ = 'visit'

    VIEW = 'View.Visit'
    CREATE = 'Create.Visit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    when = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), comment='User')
    pair_id = Column(Integer, ForeignKey('pair.id'), comment='Pair')
