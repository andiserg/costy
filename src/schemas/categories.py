from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str


class CategorySchema(CategoryCreateSchema):
    id: int
    user_id: int | None
    type: str
    icon_name: str | None
    icon_color: str | None

    class Config:
        orm_mode = True
