from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    :param plain_password: Пароль, который передает нам пользователь
    :param hashed_password: Захешированный пароль из базы данных
    :return: Возвразает boolean значение.
    - True если при хеш пароля совпал с переданным паролем.
    - False если хеш пароля не совпадает с переданным паролем
    """
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    :param password: Пароль переданный пользователем
    :return: Возвращает хеш пароля
    """
    return password_context.hash(password)
