from sqlalchemy import Column, Integer, ForeignKey

from models.model import BaseModel


class RolePermission(BaseModel):
    __tablename__ = 'role_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), comment='Permission')
    role_id = Column(Integer, ForeignKey('role.id'), comment='Role')
