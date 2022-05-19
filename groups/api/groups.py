from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from groups.schema.group import CreateGroup, DefaultGroup
from models import Group
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

groups_router = APIRouter(prefix="/groups")


@groups_router.get('', tags=['groups'], response_model=List[DefaultGroup])
async def get_groups_view(
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Group.VIEW], session, user):
        return await Group.filter(session)

    return Response(status_code=status.HTTP_403_FORBIDDEN)


@groups_router.post('', tags=['groups'], response_model=DefaultGroup)
async def create_group_view(
        create_group: CreateGroup,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Group.CREATE], session, user):
        return await Group.create(session, **create_group.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
