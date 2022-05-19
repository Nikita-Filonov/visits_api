import asyncio
import json

from models import Permission
from seeders.utils import create_with_ensure_exists

BASE_PATH = './seeders/dumps'
permissions = json.loads(open(f'{BASE_PATH}/permissions.json').read())


async def seed_permissions():
    await create_with_ensure_exists(Permission, permissions)


if __name__ == '__main__':
    asyncio.run(seed_permissions())
