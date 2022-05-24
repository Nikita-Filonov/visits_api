from typing import List

from fastapi import status, HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from users.schemas.users import UserNotFound


async def safely_get_user(session: AsyncSession, **user_fields) -> User:
    safe_values = {key: value for key, value in user_fields.items() if value is not None}

    user = await User.get(session, **safe_values)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFound(args=list(safe_values.values())).dict()
        )

    return user


async def safely_get_users(session: AsyncSession, limit: int, username: str = None, email: str = None) -> List[User]:
    if (not username) and (not email):
        return []

    clause_filter = ()
    if username:
        clause_filter += (User.username.contains(username),)

    if email:
        clause_filter += (User.email.contains(email),)

    return await User.filter(session, clause_filter=(or_(*clause_filter),), limit=limit)
