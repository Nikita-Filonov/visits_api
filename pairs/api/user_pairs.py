from typing import List

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import UserPair, GroupUser
from pairs.schemas.user_pairs import CreateUserPair, DefaultUserPair, CreateGroupUserPair
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.controllers.users import safely_get_user
from users.schemas.users import DefaultUser

user_pairs_router = APIRouter(prefix="/user-pairs")


@user_pairs_router.get('', tags=['user-pairs'], response_model=List[DefaultUserPair])
async def get_user_pairs_view(
        pair_id: int = Query(..., alias='pairId'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([UserPair.VIEW], session, user):
        return await UserPair.filter(session, pair_id=pair_id, load=(UserPair.user, UserPair.pair))

    return Response(status_code=status.HTTP_403_FORBIDDEN)


@user_pairs_router.post('', tags=['user-pairs'], response_model=DefaultUserPair)
async def create_user_pair_view(
        create_user_pair: CreateUserPair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.CREATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    user = await safely_get_user(session, email=create_user_pair.email)

    user_pair = await UserPair.create(session, user_id=user.id, pair_id=create_user_pair.pair_id)
    return await UserPair.get(session, id=user_pair.id, load=(UserPair.user, UserPair.pair))


@user_pairs_router.post('/groups', tags=['user-pairs'], response_model=List[DefaultUserPair])
async def create_user_pair_group_view(
        create_user_pair: CreateGroupUserPair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.CREATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    group_users = await GroupUser.filter(session, group_id=create_user_pair.group_id)
    user_pairs = [
        (await UserPair.create(session, user_id=group_user.user_id, pair_id=create_user_pair.pair_id)).id
        for group_user in group_users
    ]
    return await UserPair.filter(
        session, clause_filter=(UserPair.id.in_(user_pairs),), load=(UserPair.user, UserPair.pair))
