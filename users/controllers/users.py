from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from users.schemas.users import UserNotFound


async def safely_get_user(session: AsyncSession, email: str) -> User:
    user = await User.get(session, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UserNotFound(email=email).dict()
        )

    return user
