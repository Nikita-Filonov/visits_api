from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from settings import HOST
from users.emails.utils import send_email_async, random_string


async def send_user_confirm_email(session: AsyncSession, user: User):
    subject = f'[Visits] Your confirmation code'
    code = await random_string()
    await user.update(session, user, confirmation_codes=[*user.confirmation_codes, code])

    context = {'username': user.username, 'code': code, 'link': HOST + f'/confirm-email?email={user.email}'}
    await send_email_async(subject, user.email, context, 'activation_code_ru.html')
