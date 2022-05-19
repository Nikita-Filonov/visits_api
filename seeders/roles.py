import asyncio
import json

from models import Role
from seeders.utils import create_with_ensure_exists

BASE_PATH = './seeders/dumps'
roles = json.loads(open(f'{BASE_PATH}/roles.json').read())


async def seed_roles():
    await create_with_ensure_exists(Role, roles)


if __name__ == '__main__':
    asyncio.run(seed_roles())
