from typing import Optional, List, Union, Tuple

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from database import Base


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            clause_filter=None,
            load: Union[list, tuple, None] = None,
            **kwargs
    ) -> Optional['BaseModel']:
        query = select(cls).filter_by(**kwargs)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        if clause_filter:
            query = query.filter(*clause_filter)

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            select_values: Union[list, tuple, None] = None,
            order_by: Union[list, tuple, None] = None,
            clause_filter=None,
            slice_query: Union[list, tuple, None] = None,
            load: Union[list, tuple, None] = None,
            **kwargs
    ) -> List['BaseModel']:
        query = select(select_values or cls).filter_by(**kwargs)
        if order_by:
            query = query.order_by(*order_by)

        if slice_query:
            query = query.slice(*slice_query)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        if clause_filter:
            query = query.filter(*clause_filter)

        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> 'BaseModel':
        model = cls(**kwargs)
        session.add(model)
        await session.commit()

        return model

    @classmethod
    async def get_or_create(cls, session: AsyncSession, **kwargs) -> Tuple[bool, 'BaseModel']:
        model = await cls.get(session, **kwargs)
        if model is None:
            return True, await cls.create(session, **kwargs)

        return False, model

    @classmethod
    async def delete(cls, session: AsyncSession, **kwargs) -> None:
        model = await cls.get(session, **kwargs)

        if model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(model)
        await session.commit()

    @classmethod
    async def update(cls, session: AsyncSession, entity_id, **kwargs) -> None:
        query = update(cls).returning(cls).filter_by(id=entity_id).values(**kwargs)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def create_multiple(cls, session: AsyncSession, instances: List['BaseModel']):
        session.add_all(instances)
        await session.commit()

    @classmethod
    async def save_json(cls, session: AsyncSession, instance: 'BaseModel', json_field: str):
        flag_modified(instance, json_field)
        await session.commit()
