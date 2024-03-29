from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import Token
from users.authentications.authenticators import authenticate
from users.schemas.users import LoginUser

token_router = APIRouter(prefix="/token")


@token_router.post("/", tags=['token'])
async def get_token(login_user: LoginUser, session: AsyncSession = Depends(get_session)):
    """
    :param login_user: Объект ``LoginUser``, который передается в теле запроса
    :param session: см. README.md ``Объекты``
    :return: Возвращает токен пользователя или 401 код если
    пользователь не прошел аутентификацию
    """
    user = await authenticate(session, login_user)

    if user is not None:
        token = await Token.get(session, user_id=user.id)
        return {'token': token.value}

    return Response(status_code=status.HTTP_401_UNAUTHORIZED)
