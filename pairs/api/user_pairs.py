from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Pair, UserPair
from pairs.schemas.pairs import DefaultPair
from pairs.schemas.user_pairs import CreateUserPair
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

pairs_router = APIRouter(prefix="/user-pairs")


@pairs_router.post('', tags=['pairs'], response_model=DefaultPair)
async def create_user_pair_view(
        create_user_pair: CreateUserPair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([UserPair.CREATE], session, user):
        return await UserPair.create(session, **create_user_pair.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
