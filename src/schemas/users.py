"""
User schemas
"""
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    """User base class"""

    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    """Class used for user create"""

    password: str

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    """Class used for read user info"""

    id: int

    class Config:
        orm_mode = True
