from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.model import BaseModel


class GroupUser(BaseModel):
    __tablename__ = 'group_user'

    VIEW = 'View.GroupUser'
    CREATE = 'Create.GroupUser'
    DELETE = 'Delete.GroupUser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), comment='User')
    user = relationship('User')
    group_id = Column(Integer, ForeignKey('group.id'), comment='Group')
    group = relationship('Group')
