"""
Operations schemas
"""
from pydantic import BaseModel


class OperationCreateSchema(BaseModel):
    """
    Схема операції. Модель: app.models.operations.Operation
    """

    amount: int
    description: str | None
    unix_time: int
    mcc: int
    source_type: str


class OperationSchema(OperationCreateSchema):
    """
    Схема операції, яка виокристовується під час завантаження даних з БД
    """

    id: int

    class Config:
        orm_mode = True
