from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from groups.schema.group_user import CreateGroupUser
from models import GroupUser


async def create_multiple_group_users(session: AsyncSession, create_group_user: CreateGroupUser) -> List[GroupUser]:
    group_users = [
        (await GroupUser.get_or_create(session, group_id=create_group_user.group_id, user_id=user_id))[1].id
        for user_id in create_group_user.users
    ]

    return await GroupUser.filter(
        session, clause_filter=(GroupUser.id.in_(group_users),), load=(GroupUser.user, GroupUser.group))
