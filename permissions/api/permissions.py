from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Permission
from permissions.controllers.permissions import get_my_permissions
from permissions.schema.permissions import DefaultPermission
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

permissions_router = APIRouter(prefix="/permissions")


@permissions_router.get('', tags=['permissions'], response_model=List[DefaultPermission])
async def get_permissions_view(session: AsyncSession = Depends(get_session)):
    return await Permission.filter(session)


@permissions_router.get('/me', tags=['permissions'], response_model=List[DefaultPermission])
async def get_my_permissions_view(
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await get_my_permissions(session, user)
