from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair
from pairs.schemas.user_pairs import CreateUserPair


async def create_multiple_user_pairs(session: AsyncSession, create_user_pair: CreateUserPair) -> List[UserPair]:
    user_pairs = [
        (await UserPair.get_or_create(session, user_id=user_id, pair_id=create_user_pair.pair_id))[1].id
        for user_id in create_user_pair.users
    ]

    return await UserPair.filter(
        session,
        clause_filter=(UserPair.id.in_(user_pairs),),
        load=(UserPair.user, UserPair.pair)
    )
