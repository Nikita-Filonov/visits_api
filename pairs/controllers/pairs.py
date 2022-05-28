from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair, Pair


async def get_learner_pairs(session: AsyncSession, user_id: int) -> List[Pair]:
    """
    :param session: см. README.md ``Объекты``
    :param user_id: Integer значение id пользователя
    :return: Возвращает список объектов ``Pair`` для данного ``user_id``

    Используется, чтобы получить пары для студента. В отличие от преподавателя
    студент видит, только пары, в которые он был добавлен
    """
    query = select(Pair).join(UserPair).filter(UserPair.user_id == user_id)
    return (await session.execute(query)).scalars().all()
