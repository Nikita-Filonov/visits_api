from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Pair
from pairs.schemas.pairs import CreatePair, DefaultPair

pairs_router = APIRouter(prefix="/pairs")


@pairs_router.post('', tags=['pairs'], response_model=DefaultPair)
async def create_pair_view(create_pair: CreatePair, session: AsyncSession = Depends(get_session)):
    return await Pair.create(session, **create_pair.dict())
