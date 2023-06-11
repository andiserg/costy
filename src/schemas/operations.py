"""
Operations schemas
"""
from pydantic import BaseModel


class OperationCreateSchema(BaseModel):
    """Схема операції. Модель: src.domain.operations.Operation"""

    amount: int
    description: str | None
    source_type: str
    time: int | None
    category_id: int | None


class OperationSchema(OperationCreateSchema):
    """Схема операції, яка виокристовується під час завантаження даних з БД"""

    id: int
    subcategory_id: int | None

    class Config:
        orm_mode = True
