from sqlalchemy import Column, Integer, ForeignKey

from models.model import BaseModel


class GroupUser(BaseModel):
    __tablename__ = 'group_user'

    VIEW = 'View.GroupUser'
    CREATE = 'Create.GroupUser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), comment='User')
    group_id = Column(Integer, ForeignKey('group.id'), comment='Group')
