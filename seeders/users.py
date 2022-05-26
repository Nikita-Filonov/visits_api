import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database import engine
from models import User, Token
from users.schemas.users import CreateUser

BASE_PATH = './seeders/dumps'
users = json.loads(open(f'{BASE_PATH}/users.json').read())


async def seed_users():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        for user in users:
            user_payload = CreateUser(**user).dict()
            user = await User.create(session, **user_payload, is_active=True, is_email_confirmed=True)
            await Token.create(session, user)


if __name__ == '__main__':
    asyncio.run(seed_users())
