import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database import engine
from models import User, Token, UserRole
from users.schemas.users import CreateUser

BASE_PATH = './seeders/dumps'
users = json.loads(open(f'{BASE_PATH}/users.json').read())
user_roles = json.loads(open(f'{BASE_PATH}/user_roles.json').read())


async def seed_users():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        for user, user_role in zip(users, user_roles):
            is_user_exists = await User.get(session, email=user['email'])
            if is_user_exists:
                return

            user_payload = CreateUser(**user).dict()
            user = await User.create(session, **user_payload, is_active=True, is_email_confirmed=True)
            await Token.create(session, user)
            await UserRole.create(session, user_id=user.id, role_id=user_role['role_id'])


if __name__ == '__main__':
    asyncio.run(seed_users())
