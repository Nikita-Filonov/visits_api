from typing import List, Optional

from fastapi import Depends, APIRouter, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User, Token
from permissions.controllers.permissions import is_action_allowed
from users.authentications.authenticators import is_user_authenticated
from users.controllers.users import safely_get_users
from users.emails.users_emails import send_user_confirm_email
from users.schemas.users import CreateUser, DefaultUser, ConfirmUser

users_router = APIRouter(prefix="/user")


@users_router.get("/me/", tags=['user'], response_model=DefaultUser)
async def read_users_me(current_user: DefaultUser = Depends(is_user_authenticated)):
    """
    :param current_user: Объект ``DefaultUser`` текущий пользователь
    :return: Возвращает объект ``DefaultUser``
    """
    return current_user


@users_router.get("/query", tags=['user'], response_model=List[DefaultUser])
async def get_users_query(
        username: Optional[str] = Query(default=None),
        email: Optional[str] = Query(default=None),
        limit: int = Query(default=10, description='Number of users to be returned'),
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated),
):
    """
    :param username: String параметр ``username``, который передается в query params
    :param email: String параметр ``email``, который передается в query params
    :param limit: Integer параметр запроса, который передается в query params.
    Отвечает за количество возвращаемый пользователей
    :param session: см. README.md ``Объекты``
    :param user: см. README.md ``Объекты``
    :return: Возвращает список объектов ``DefaultUser``
    """
    if not await is_action_allowed([User.VIEW], session, user):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    return await safely_get_users(session, limit=limit, username=username, email=email)


@users_router.post("/", tags=['user'], response_model=DefaultUser)
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    """
    :param user: см. README.md ``Объекты``
    :param session: см. README.md ``Объекты``
    :return: Возвращает объект ``DefaultUser``
    """
    user = await User.create(session, **user.dict())
    await send_user_confirm_email(session, user)
    return user


@users_router.post("/send-confirm-email/", tags=['user'])
async def send_confirm_email(user: ConfirmUser, session: AsyncSession = Depends(get_session)):
    """
    :param user: Объект ``ConfirmUser``
    :param session: см. README.md ``Объекты``
    :return: Возвращает статус код 202, если письмо для подтверждения почты
    было учпешно отправлено. Код 403, если пользователя с почтой ``ConfirmUser.email``
    не существует или он уже активирован
    """
    user = await User.get(session, email=user.email)
    if user is None:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if user.is_email_confirmed or user.is_active:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await send_user_confirm_email(session, user)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@users_router.post("/confirm-email/", tags=['user'])
async def confirm_email(user_confirm: ConfirmUser, session: AsyncSession = Depends(get_session)):
    """
    :param user_confirm: Объект ``ConfirmUser``
    :param session: см. README.md ``Объекты``
    :return: Возвращает токен если активация пользователя прошла успешно.
    Если код подтвержения не верный или пользователь уже активирован, то
    возвращает 403 код
    """
    user = await User.get(session, email=user_confirm.email)
    if user is None or user.is_email_confirmed:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if user_confirm.code not in user.confirmation_codes:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await user.update(session, user, is_email_confirmed=True, is_active=True)

    token = await Token.create(session, user)
    return {'token': token.value}
