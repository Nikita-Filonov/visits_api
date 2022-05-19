from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import UserRole
from roles.schema.user_roles import CreateUserRole, DefaultUserRole

user_roles_router = APIRouter(prefix="/user-roles")


@user_roles_router.post('', tags=['user-roles'], response_model=DefaultUserRole)
async def create_user_role_view(create_user_role: CreateUserRole, session: AsyncSession = Depends(get_session)):
    return await UserRole.create(session, **create_user_role.dict())
