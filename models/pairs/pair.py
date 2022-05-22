from sqlalchemy import Column, Integer, String, Time, ForeignKey

from models.model import BaseModel


class Pair(BaseModel):
    __tablename__ = 'pair'

    VIEW = 'View.Pair'
    CREATE = 'Create.Pair'
    DELETE = 'Delete.Pair'
    UPDATE = 'Update.Pair'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), comment='Name')
    room = Column(String(250), comment='Room', default=None)
    start_at = Column(Time, default=None, comment='When the pair starts')
    end_at = Column(Time, default=None, comment='When the pair ends')
    created_by_user_id = Column(Integer, ForeignKey('user.id'), default=None, comment='Who has created the pair')
