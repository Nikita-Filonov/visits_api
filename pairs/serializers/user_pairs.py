from datetime import datetime, timedelta
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair, Visit


async def get_start_and_end():
    today = datetime.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    return start, end


async def serialize_user_pairs(session: AsyncSession, user_pairs: List[UserPair]) -> List[UserPair]:
    start, end = await get_start_and_end()
    for user_pair in user_pairs:
        visit = await Visit.get(
            session,
            user_id=user_pair.user_id,
            pair_id=user_pair.pair_id,
            clause_filter=(Visit.when >= start, Visit.when <= end)
        )
        setattr(user_pair, 'visit', visit)

    return user_pairs
