from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)
