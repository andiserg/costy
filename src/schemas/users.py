from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    password: str

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True
