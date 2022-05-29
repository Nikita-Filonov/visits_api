from typing import List

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def safely_get_users(session: AsyncSession, limit: int, username: str = None, email: str = None) -> List[User]:
    if (not username) and (not email):
        return []

    clause_filter = ()
    if username:
        clause_filter += (User.username.contains(username),)

    if email:
        clause_filter += (User.email.contains(email),)

    return await User.filter(session, clause_filter=(or_(*clause_filter),), limit=limit)
