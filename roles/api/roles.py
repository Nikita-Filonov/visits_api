from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Role
from roles.schema.roles import CreateRole, DefaultRole

roles_router = APIRouter(prefix="/roles")


@roles_router.post('', tags=['roles'], response_model=DefaultRole)
async def create_role_view(create_role: CreateRole, session: AsyncSession = Depends(get_session)):
    return await Role.create(session, **create_role.dict())
