"""
Methods of password hashing and their comparison.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comparing the plain password with the hashed password.

    :param plain_password: The password entered by the user during login.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Encrypting the password.

    :param password: The password that needs to be encrypted.
    :return: The encrypted password.
    """
    return pwd_context.hash(password)
