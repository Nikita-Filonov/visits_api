from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database import engine


async def create_with_ensure_exists(entity, payload: List[dict]):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        for race in payload:
            result = await session.execute(select(entity).filter_by(**race))
            is_exists = result.scalars().all()

            if is_exists:
                continue

            model = entity(**race)
            session.add(model)
            await session.commit()
