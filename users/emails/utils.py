from random import choice, randint
from string import ascii_letters, digits

from fastapi_mail import FastMail, MessageSchema

from settings import email_config


async def random_string():
    """
    :return:
    """
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(9, 15)))


async def send_email_async(subject: str, email_to: str, body: dict, template: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )

    fm = FastMail(email_config)
    await fm.send_message(message, template_name=template)
