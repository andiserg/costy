"""
Методи хешування паролів та їх порівняння
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    :param plain_password: Пароль, який користувач увів під час логіну
    :param hashed_password: Зашифрований пароль, який зберігається у БД
    :return: True якщо паролі співпадають, False якщо ні
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    :param password: Пароль, який потрібно зашифрувати
    :return: Зашифрований пароль
    """
    return pwd_context.hash(password)
