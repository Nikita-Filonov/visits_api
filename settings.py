from pathlib import Path

from fastapi_mail import ConnectionConfig

DEBUG = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rq.calculator@gmail.com'
EMAIL_HOST_PASSWORD = 'urtsswubwcaqmbjo'

HOST = 'http://localhost:8000'

email_config = ConnectionConfig(
    MAIL_USERNAME=EMAIL_HOST_USER,
    MAIL_PASSWORD=EMAIL_HOST_PASSWORD,
    MAIL_FROM=EMAIL_HOST_USER,
    MAIL_PORT=EMAIL_PORT,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_FROM_NAME=EMAIL_HOST_USER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates/emails'
)
