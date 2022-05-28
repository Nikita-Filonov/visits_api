from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Role, UserRole, Permission, RolePermission
from users.schemas.users import DefaultUser


async def get_roles(session: AsyncSession, user: DefaultUser) -> List[Role]:
    """
    :param session: см. README.md ``Объекты``
    :param user: см. README.md ``Объекты``
    :return: Возвращает список из объектов ``Role``

    Используется, чтобыв получить список всех ролей пользователя ``user``
    """
    roles_query = select(Role) \
        .join(UserRole) \
        .filter(UserRole.user_id == user.id)
    return (await session.execute(roles_query)).scalars().all()


async def get_my_permissions(session: AsyncSession, user: DefaultUser) -> List[Permission]:
    """
    :param session: см. README.md ``Объекты``
    :param user: см. README.md ``Объекты``
    :return: Возвращает список из объектов ``Permission``

    Используется, чтобы получить список всех прав пользователя ``user``
    """
    roles = await get_roles(session, user)

    permissions_query = select(Permission) \
        .join(RolePermission) \
        .filter(RolePermission.role_id.in_(role.id for role in roles))
    return (await session.execute(permissions_query)).scalars().all()


async def is_action_allowed(scopes: List[str], session: AsyncSession, user: DefaultUser) -> bool:
    """
    :param scopes: Список из скоупов пермишенов, которые необходимо проверить
    :param session: см. README.md ``Объекты``
    :param user: см. README.md ``Объекты``
    :return: Возвращает boolean значение. True если пользователь имеются
    нужные ``scopes`` и False если пользователь не имеет нужных ``scopes``
    """
    permissions = await get_my_permissions(session, user)

    return any((permission.scope in scopes) for permission in permissions)
