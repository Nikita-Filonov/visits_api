from fastapi import Depends, APIRouter, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User, Token
from users.authentications.authenticators import is_user_authenticated
from users.emails.users_emails import send_user_confirm_email
from users.schemas.users import LoginUser, CreateUser, DefaultUser, ConfirmUser

users_router = APIRouter(prefix="/user")


@users_router.get("/me/", tags=['user'])
async def read_users_me(current_user: LoginUser = Depends(is_user_authenticated)):
    return current_user


@users_router.post("/", tags=['user'], response_model=DefaultUser)
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    user = await User.create(session, user)
    await send_user_confirm_email(session, user)
    return user


@users_router.post("/send-confirm-email/", tags=['user'])
async def send_confirm_email(user: ConfirmUser, session: AsyncSession = Depends(get_session)):
    user = await User.get(session, email=user.email)
    if user is None:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if user.is_email_confirmed or user.is_active:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await send_user_confirm_email(session, user)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@users_router.post("/confirm-email/", tags=['user'])
async def confirm_email(user_confirm: ConfirmUser, session: AsyncSession = Depends(get_session)):
    user = await User.get(session, email=user_confirm.email)
    if user is None or user.is_email_confirmed:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if user_confirm.code not in user.confirmation_codes:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await user.update(session, user, is_email_confirmed=True, is_active=True)

    token = await Token.create(session, user)
    return {'token': token.value}
