"""
Технічні особливості побудови таблиць в ORM
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table

from src.app.account.users.models import User
from src.app.operations.models import Operation


def create_tables(mapper_registry) -> dict[str, Table]:
    return {
        "users": Table(
            "users",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("email", String, unique=True, index=True, nullable=False),
            Column("hashed_password", String, nullable=False),
        ),
        "operations": Table(
            "operations",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("amount", Integer, nullable=False),
            Column("description", String),
            Column("unix_time", Integer, nullable=False),
            Column("mcc", Integer),
            # mcc - код виду операції
            Column("source_type", String, nullable=False),
            # Тип джерела.
            # value: "manual" | "<bank_name>"
            # Операція може бути або додана вручну або за допомогою API банку
            Column("user_id", Integer, ForeignKey("users.id")),
        ),
    }


def start_mappers(mapper_registry, tables):
    """
    Прив'язка класів до таблиць. ORM буде з ними працювати як з моделями
    Такий підхід відповідє SOLID, інверсуючи залежності.
    Таким чином, частини програми нижчого рівня стають залежними від вищого рівня
    """
    mapper_registry.map_imperatively(User, tables["users"])
    mapper_registry.map_imperatively(Operation, tables["operations"])
