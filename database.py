import logging
import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import DEBUG

logger = logging.getLogger(__name__)

DRIVER = 'postgresql+asyncpg'
POSTGRES_DB = 'postgres' if DEBUG else 'automation_api'  # automation_api
POSTGRES_USER = 'postgres' if DEBUG else 'say_what'  # say_what
POSTGRES_PASSWORD = 'postgres' if DEBUG else 'vtngjwfut'  # vtngjwfut
POSTGRES_PORT = 5432
POSTGRES_SERVER = 'visits_api_db' if DEBUG else 'localhost'
DATABASE_URL = f"{DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(os.environ.get('DATABASE_URL'), 23455555)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
metadata = MetaData()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
