"""
Operation models
"""
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

from app.core.database import Base


class Operation(Base):
    """
    Модель операції (транзакції, витрати).
    """

    __tablename__ = "operations"

    id: Mapped[int] = Column(Integer, primary_key=True)
    amount: Mapped[int] = Column(Integer)
    description: Mapped[Optional[str]] = Column(String)
    unix_time: Mapped[int] = Column(Integer)
    # Код виду операції
    mcc: Mapped[Optional[int]] = Column(Integer)

    # Тип джерела. "manual" | "<bank_name>"
    # Операція може бути або додана вручну або за допомогою API банку
    source_type: Mapped[str] = Column(String)

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
