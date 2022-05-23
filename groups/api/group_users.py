from typing import List

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from groups.schema.group_user import CreateGroupUser, DefaultGroupUser
from models import GroupUser
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.controllers.users import safely_get_user
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

    user = await safely_get_user(session, email=create_group_user.email, username=create_group_user.username)

    group_user = await GroupUser.create(session, group_id=create_group_user.group_id, user_id=user.id)
    return await GroupUser.get(session, id=group_user.id, load=(GroupUser.user, GroupUser.group))


@group_users_router.delete('/{group_user_id}/', tags=['groups'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_group_user_view(
        group_user_id: int,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([GroupUser.DELETE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await GroupUser.delete(session, id=group_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
