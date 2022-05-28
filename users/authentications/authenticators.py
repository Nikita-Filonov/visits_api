from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User, Token
from users.authentications.password import verify_password
from users.schemas.users import LoginUser, DefaultUser

API_KEY_HEADER = APIKeyHeader(name='Authorization')


async def authenticate(session: AsyncSession, login_user: LoginUser) -> Optional[User]:
    """
    :param session: см. README.md ``Объекты``
    :param login_user: Объект ``LoginUser`` переданный в теле запроса
    :return: Возвращает объект ``User`` или ``None``
    """
    user = await User.get(session, email=login_user.email, is_active=True)
    if user is None:
        return

    is_password_valid = await verify_password(login_user.password, user.password)
    return user if is_password_valid else None


async def is_user_authenticated(
        session: AsyncSession = Depends(get_session),
        api_key: str = Depends(API_KEY_HEADER)
) -> DefaultUser:
    """
    :param session: см. README.md ``Объекты``
    :param api_key: Заголовок с токеном, который передается в запроса для аутентификации и
    идентификации пользователя. Выглядит как: ``Token <token_goes_here>``
    :return: Возвращает объект ``DefaultUser``
    :raises: Поднимает ``HTTPException`` если токен некорректный или пользователь не активен
    """
    prefix, token = api_key.split()
    if prefix != 'Token':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Prefix")

    token = await Token.get(session, value=token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

    if not token.user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User inactive or deleted.')

    return DefaultUser(id=token.user.id, username=token.user.username, email=token.user.email)
