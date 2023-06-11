from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str


class CategorySchema(CategoryCreateSchema):
    id: int
    user_id: int | None
    type: str
    icon_name: str | None
    icon_color: str | None
    parent_id: int | None

    class Config:
        orm_mode = True
