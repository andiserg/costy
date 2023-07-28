from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    name: str
    icon_name: str | None
    icon_color: str | None


class CategorySchema(CategoryCreateSchema):
    id: int
    parent_id: int | None
    user_id: int | None
    type: str

    class Config:
        orm_mode = True
