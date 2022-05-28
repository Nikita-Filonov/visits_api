from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models import UserPair, GroupUser
from pairs.schemas.user_pairs import CreateUserPair, CreateGroupUserPair


async def create_multiple_user_pairs(session: AsyncSession, create_user_pair: CreateUserPair) -> List[UserPair]:
    """
    :param session: см. README.md ``Объекты``
    :param create_user_pair: Объект ``CreateUserPair`` передаваемый в теле запроса
    :return: Возвращает список объектов ``UserPair``

    Используется, чтобы добавить в пару сразу несколько студентов. Также может быть добавлен
    только один студент.
    """
    user_pairs = [
        (await UserPair.get_or_create(session, user_id=user_id, pair_id=create_user_pair.pair_id))[1].id
        for user_id in create_user_pair.users
    ]

    return await UserPair.filter(
        session, clause_filter=(UserPair.id.in_(user_pairs),), load=(UserPair.user, UserPair.pair))


async def create_multiple_user_pairs_group(
        session: AsyncSession,
        create_user_pair: CreateGroupUserPair
) -> List[UserPair]:
    """
    :param session: см. README.md ``Объекты``
    :param create_user_pair: Объект ``CreateGroupUserPair`` передаваемый в теле запроса
    :return: Возвращает список объектов ``UserPair``

    Используется чтобы добавить студентов из нескольких групп сразу. То есть если
    мы выбрали две группы, то в пару будут добавлены все студенты находящиеся в
    выбранных группах
    """
    group_users = await GroupUser.filter(session, clause_filter=(GroupUser.group_id.in_(create_user_pair.groups),))
    user_pairs = [
        (await UserPair.get_or_create(session, user_id=group_user.user_id, pair_id=create_user_pair.pair_id))[1].id
        for group_user in group_users
    ]
    return await UserPair.filter(
        session, clause_filter=(UserPair.id.in_(user_pairs),), load=(UserPair.user, UserPair.pair))
