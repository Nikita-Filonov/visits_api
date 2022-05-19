from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Pair
from pairs.schemas.pairs import CreatePair, DefaultPair
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

pairs_router = APIRouter(prefix="/pairs")


@pairs_router.post('', tags=['pairs'], response_model=DefaultPair)
async def create_pair_view(
        create_pair: CreatePair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Pair.CREATE], session, user):
        return await Pair.create(session, **create_pair.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
