from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair, Pair


async def get_self_pairs(session: AsyncSession, user_id: int) -> List[Pair]:
    query = select(Pair).join(UserPair).filter(UserPair.user_id == user_id)
    return (await session.execute(query)).scalars().all()
