from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT schema along with the keyword.
    As a result, for user authentication during a request,
    you need to provide the following field in headers:
    Authorization: <token_type> <access_token>
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Date schema obtained from the decrypted JWT."""

    email: str | None = None
