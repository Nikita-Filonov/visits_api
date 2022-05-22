from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Pair
from models.roles.role import Roles
from pairs.controllers.pairs import get_learner_pairs
from pairs.schemas.pairs import CreatePair, DefaultPair
from permissions.controllers.permissions import is_action_allowed, get_roles
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

pairs_router = APIRouter(prefix="/pairs")


@pairs_router.get('', tags=['pairs'], response_model=List[DefaultPair])
async def get_pairs_view(
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([Pair.VIEW], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    is_learner = any((role.name == Roles.LEARNER.value) for role in await get_roles(session, user))
    if is_learner:
        return await get_learner_pairs(session, user_id=user.id)

    return await Pair.filter(session, created_by_user_id=user.id)


@pairs_router.post('', tags=['pairs'], response_model=DefaultPair)
async def create_pair_view(
        create_pair: CreatePair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Pair.CREATE], session, user):
        return await Pair.create(session, **create_pair.dict(), created_by_user_id=user.id)

    return Response(status_code=status.HTTP_403_FORBIDDEN)


@pairs_router.delete('/{pair_id}/', tags=['pairs'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_pair_view(
        pair_id: int,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([Pair.DELETE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await Pair.delete(session, id=pair_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@pairs_router.patch('/{pair_id}/', tags=['pairs'], response_model=DefaultPair)
async def update_pair_view(
        pair_id: int,
        update_pair: CreatePair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if not await is_action_allowed([Pair.UPDATE], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    pair = await Pair.get(session, id=pair_id, user_id=user.id)
    if pair is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await pair.update(session, entity_id=pair_id, **update_pair.dict(exclude_unset=True))
    return pair
