from pydantic import BaseModel


class OperationCreateSchema(BaseModel):
    amount: int
    description: str | None
    source_type: str
    time: int | None
    category_id: int | None


class OperationSchema(OperationCreateSchema):
    id: int
    subcategory_id: int | None
    is_exceeded_limit: bool | None

    class Config:
        orm_mode = True
