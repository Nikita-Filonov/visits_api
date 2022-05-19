from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Pair, UserRole
from pairs.schemas.pairs import CreatePair, DefaultPair
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

pairs_router = APIRouter(prefix="/pairs")


@pairs_router.post('', tags=['pairs'], response_model=DefaultPair)
async def create_pair_view(
        create_pair: CreatePair,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    user_role_query = await UserRole.get(session, user_id=user.id)
    print(user_role_query, 12345)
    return await Pair.create(session, **create_pair.dict())
