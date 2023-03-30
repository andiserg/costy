from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped

from app.core.database import Base


class MonobankManager(Base):
    """
    Модель Monobank менеджера, який містить інформацію для роботи
    """

    __tablename__ = "monobank_managers"

    id: Mapped[int] = Column(Integer, primary_key=True)
    token: Mapped[str] = Column(String)
    last_update: Mapped[int] = Column(Integer)
    # Остання дата обновлення операцій в unix форматі

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
