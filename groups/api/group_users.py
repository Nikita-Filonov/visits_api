from typing import List

from fastapi import APIRouter, Depends, Response, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from groups.schema.group_user import CreateGroupUser, UserNotFound, DefaultGroupUser
from models import User, GroupUser
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

group_users_router = APIRouter(prefix="/group-users")


@group_users_router.get('', tags=['group-users'], response_model=List[DefaultGroupUser])
async def get_group_users(
        group_id: int = Query(..., alias='groupId'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([GroupUser.VIEW], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    return await GroupUser.filter(session, group_id=group_id, load=(GroupUser.user, GroupUser.group))


@group_users_router.post('', tags=['group-users'], response_model=DefaultGroupUser)
async def create_group_user_view(
        create_group_user: CreateGroupUser,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([GroupUser.CREATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    user = await User.get(session, email=create_group_user.email)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=UserNotFound(email=create_group_user.email).dict()
        )

    group_user = await GroupUser.create(session, group_id=create_group_user.group_id, user_id=user.id)
    return await GroupUser.get(session, id=group_user.id, load=(GroupUser.user, GroupUser.group))
