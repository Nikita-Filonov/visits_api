from typing import List

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import UserPair
from pairs.schemas.user_pairs import CreateUserPair, DefaultUserPair
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
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
    if await is_action_allowed([UserPair.CREATE], session, user):
        return await UserPair.create(session, **create_user_pair.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
