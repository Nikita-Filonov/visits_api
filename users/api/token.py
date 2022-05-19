from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Token
from users.authentications.authenticators import is_user_authenticated, authenticate
from users.schemas.users import LoginUser

token_router = APIRouter(prefix="/token")


@token_router.post("/", tags=['token'])
async def get_token(login_user: LoginUser, session: AsyncSession = Depends(get_session)):
    user = await authenticate(session, login_user)

    if user is not None:
        token = await Token.get(session, user_id=user.id)
        return {'token': token.value}

    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@token_router.post("/google/", tags=['token'])
async def get_token_google(current_user: LoginUser = Depends(is_user_authenticated)):
    return current_user
