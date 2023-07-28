"""
CRUD account methods
"""
from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from src.schemas.auth import TokenData


def create_access_token(data: dict) -> str:
    """
    Creates a JWT (JSON Web Token) that will be used to identify the logged-in user.
    It contains encrypted user's email and the expiration date for the token.

    :param data: Dictionary with the following template: {'sub': user.email}
    :return: JWT as a string.
    """
    # Час у хвилинах, під час якого токен дійсний
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_token_data(token: str) -> TokenData | None:
    """
    Decryption of JWT (JSON Web Token)
    :param token: Json Web Token
    :return: TokenData | None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return
        return TokenData(email=email)
    except JWTError:
        return
