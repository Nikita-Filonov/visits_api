from sqlalchemy import Column, Integer, String, Time, ForeignKey, Float

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
    visit_score = Column(Float, comment='Score for each pair visit', default=None)
    missed_score = Column(Float, comment='Score for each pair miss', default=None)
    sick_score = Column(Float, comment='Score when user were sick', default=None)
    created_by_user_id = Column(Integer, ForeignKey('user.id'), default=None, comment='Who has created the pair')
