from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair, Visit


async def serialize_user_pairs(session: AsyncSession, user_pairs: List[UserPair]) -> List[UserPair]:
    for user_pair in user_pairs:
        visit = await Visit.get_to_day_visit(session, user_id=user_pair.user_id, pair_id=user_pair.pair_id)
        setattr(user_pair, 'visit', visit)

    return user_pairs
