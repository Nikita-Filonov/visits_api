import binascii
import os


async def generate_token() -> str:
    """
    Используется, чтобы сгенерировать хеш токена для пользователя

    :return: Возвращает сгенерированный токен в виде строки
    """
    return binascii.hexlify(os.urandom(20)).decode()
