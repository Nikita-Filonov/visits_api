from typing import List

from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Visit
from pairs.schemas.visitis import CreateVisit, DefaultVisit
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

visits_router = APIRouter(prefix="/visits")


@visits_router.get('', tags=['visits'], response_model=List[DefaultVisit])
async def get_visits_view(
        pair_id: int = Query(..., alias='pairId'),
        user_id: int = Query(..., alias='userId'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Visit.VIEW], session, user):
        return await Visit.filter(session, pair_id=pair_id, user_id=user_id)

    return Response(status_code=status.HTTP_403_FORBIDDEN)


@visits_router.get('/me', tags=['visits'], response_model=List[DefaultVisit])
async def get_my_visits_view(
        pair_id: int = Query(..., alias='pairId'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Visit.filter(session, pair_id=pair_id, user_id=user.id)


@visits_router.post('', tags=['visits'], response_model=DefaultVisit)
async def create_visit_view(
        create_visit: CreateVisit,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Visit.CREATE], session, user):
        return await Visit.create(session, **create_visit.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
