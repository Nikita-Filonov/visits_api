from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import UserPair
from pairs.controllers.user_pairs import create_multiple_user_pairs, create_multiple_user_pairs_group
from pairs.schemas.user_pairs import CreateUserPair, DefaultUserPair, CreateGroupUserPair
from pairs.serializers.user_pairs import serialize_user_pairs
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser
from utils.api import resolve_query_params

user_pairs_router = APIRouter(prefix="/user-pairs")


@user_pairs_router.get('', tags=['user-pairs'], response_model=List[DefaultUserPair])
async def get_user_pairs_view(
        pair_id: int = Query(..., alias='pairId'),
        user_id: Optional[int] = Query(default=None, alias='userId'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.VIEW], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    query = await resolve_query_params(pair_id=pair_id, user_id=user_id)
    user_pairs = await UserPair.filter(session, **query, load=(UserPair.user, UserPair.pair))

    return await serialize_user_pairs(session, user_pairs)


@user_pairs_router.post('', tags=['user-pairs'], response_model=List[DefaultUserPair])
async def create_user_pair_view(
        create_user_pair: CreateUserPair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.CREATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    return await create_multiple_user_pairs(session, create_user_pair)


@user_pairs_router.post('/groups', tags=['user-pairs'], response_model=List[DefaultUserPair])
async def create_user_pair_group_view(
        create_user_pair: CreateGroupUserPair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.CREATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    return await create_multiple_user_pairs_group(session, create_user_pair)


@user_pairs_router.delete('/{user_pair_id}/', tags=['user-pairs'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_pair_view(
        user_pair_id: int,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([UserPair.DELETE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await UserPair.delete(session, id=user_pair_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
