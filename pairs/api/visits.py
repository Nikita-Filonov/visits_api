from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Visit
from pairs.schemas.visitis import CreateVisit, DefaultVisit
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

visits_router = APIRouter(prefix="/visits")


@visits_router.post('', tags=['visits'], response_model=DefaultVisit)
async def create_visit_view(
        create_visit: CreateVisit,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    if await is_action_allowed([Visit.CREATE], session, user):
        return await Visit.create(session, **create_visit.dict())

    return Response(status_code=status.HTTP_403_FORBIDDEN)
