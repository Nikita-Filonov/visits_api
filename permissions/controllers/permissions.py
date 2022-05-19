from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Role, UserRole, Permission, RolePermission
from users.schemas.users import DefaultUser


async def is_action_allowed(scopes: List[str], session: AsyncSession, user: DefaultUser) -> bool:
    roles_query = select(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id)
    roles: List[Role] = (await session.execute(roles_query)).scalars().all()

    permissions_query = select(Permission) \
        .join(RolePermission) \
        .filter(RolePermission.role_id.in_(role.id for role in roles))
    permissions: List[Permission] = (await session.execute(permissions_query)).scalars().all()

    return any((permission.scope in scopes) for permission in permissions)
