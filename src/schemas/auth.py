from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема JWT разом з ключовим словом.
    В результаті, для аутентифікації користувача під час запиту,
    потрібно вказати наступне поле в headers:
        Authorization: <token_type> <access_token>
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема дати, яка отримана з розшифрованого JWT."""

    email: str | None = None
