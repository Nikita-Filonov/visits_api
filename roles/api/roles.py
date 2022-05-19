from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Role
from roles.schema.roles import CreateRole, DefaultRole
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

roles_router = APIRouter(prefix="/roles")


@roles_router.get('', tags=['roles'], response_model=List[DefaultRole])
async def get_roles_view(
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Role.filter(session)


@roles_router.post('', tags=['roles'], response_model=DefaultRole)
async def create_role_view(
        create_role: CreateRole,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Role.create(session, **create_role.dict())
