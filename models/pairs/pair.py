from sqlalchemy import Column, Integer, String, Time

from models.model import BaseModel


class Pair(BaseModel):
    __tablename__ = 'pair'

    CREATE = 'Create.Pair'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), comment='Name')
    room = Column(String(250), comment='Room', default=None)
    start_at = Column(Time, default=None, comment='When the pair starts')
    end_at = Column(Time, default=None, comment='When the pair ends')
