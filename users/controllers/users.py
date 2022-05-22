from fastapi import status, HTTPException
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
