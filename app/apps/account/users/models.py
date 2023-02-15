"""
Моделі сутностей користувачів
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    hashed_password: Mapped[str] = Column(String)
