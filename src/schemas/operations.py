"""
Operations schemas
"""
from pydantic import BaseModel


class OperationCreateSchema(BaseModel):
    """
    Схема операції. Модель: src.models.operations.Operation
    """

    amount: int
    description: str | None
    mcc: int
    source_type: str


class OperationSchema(OperationCreateSchema):
    """
    Схема операції, яка виокристовується під час завантаження даних з БД
    """

    id: int
    unix_time: int

    class Config:
        orm_mode = True
