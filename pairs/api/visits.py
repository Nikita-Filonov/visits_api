from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Visit
from pairs.schemas.visitis import CreateVisit, DefaultVisit

visits_router = APIRouter(prefix="/visits")


@visits_router.post('', tags=['visits'], response_model=DefaultVisit)
async def create_visit_view(create_visit: CreateVisit, session: AsyncSession = Depends(get_session)):
    return await Visit.create(session, **create_visit.dict())
