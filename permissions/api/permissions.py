from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Permission
from permissions.schema.permissions import DefaultPermission

permissions_router = APIRouter(prefix="/permissions")


@permissions_router.get('', tags=['permissions'], response_model=List[DefaultPermission])
async def get_permissions_view(session: AsyncSession = Depends(get_session)):
    return await Permission.filter(session)
