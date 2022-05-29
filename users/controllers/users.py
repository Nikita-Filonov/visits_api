from typing import List

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def safely_get_users(session: AsyncSession, limit: int, username: str = None, email: str = None) -> List[User]:
    """
    :param session: см. README.md ``Объекты``
    :param limit: Integer значение, которое обозначает максимальное количество
    возвращаемых пользователей
    :param username: String значение имени пользователя
    :param email: String значение электронного адреса пользователя
    :return: Возвращает список объектов ``User``

    Используется, чтобы осуществлять поиск пользователей по их ``username``, ``email``
    """
    if (not username) and (not email):
        return []

    clause_filter = ()
    if username:
        clause_filter += (User.username.contains(username),)

    if email:
        clause_filter += (User.email.contains(email),)

    return await User.filter(session, clause_filter=(or_(*clause_filter),), limit=limit)
