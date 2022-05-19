import asyncio
import json

from models import Permission, RolePermission
from seeders.utils import create_with_ensure_exists

BASE_PATH = './seeders/dumps'
permissions = json.loads(open(f'{BASE_PATH}/permissions.json').read())
role_permissions = json.loads(open(f'{BASE_PATH}/role_permissions.json').read())


async def seed_permissions():
    await create_with_ensure_exists(Permission, permissions)
    await create_with_ensure_exists(RolePermission, role_permissions)


if __name__ == '__main__':
    asyncio.run(seed_permissions())
