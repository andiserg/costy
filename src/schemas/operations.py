"""
Operations schemas
"""
from pydantic import BaseModel


class OperationCreateSchema(BaseModel):
    """Схема операції. Модель: src.domain.operations.Operation"""

    amount: int
    description: str | None
    mcc: int
    source_type: str
    time: int | None


class OperationSchema(OperationCreateSchema):
    """Схема операції, яка виокристовується під час завантаження даних з БД"""

    id: int

    class Config:
        orm_mode = True
