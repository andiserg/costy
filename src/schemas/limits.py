from pydantic import BaseModel


class LimitCreateSchema(BaseModel):
    category_id: int
    limit: int
    date_range: str


class LimitSchema(LimitCreateSchema):
    id: int

    class Config:
        orm_mode = True
