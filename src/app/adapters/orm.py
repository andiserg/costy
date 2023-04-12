"""
Технічні особливості побудови таблиць в ORM
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from src.app.domain.bank_managers import Manager, ManagerProperty
from src.app.domain.operations import Operation
from src.app.domain.users import User


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
        "managers": Table(
            "managers",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("bank_name", String, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id")),
        ),
        "manager_properties": Table(
            "manager_properties",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, nullable=False),
            Column("value", String, nullable=False),
            Column("type", String, nullable=False),
            Column("manager_id", Integer, ForeignKey("managers.id")),
        ),
    }


def start_mappers(mapper_registry: registry, tables: dict[str, Table]):
    """
    Прив'язка класів до таблиць. ORM буде з ними працювати як з моделями
    Такий підхід відповідє SOLID, інверсуючи залежності.
    Таким чином, частини програми нижчого рівня стають залежними від вищого рівня
    """
    mapper_registry.map_imperatively(
        User,
        tables["users"],
        properties={"managers": relationship(Manager, backref="user")},
    )
    mapper_registry.map_imperatively(Operation, tables["operations"])
    mapper_registry.map_imperatively(
        Manager,
        tables["managers"],
        properties={"properties": relationship(ManagerProperty, backref="manager")},
    )
    mapper_registry.map_imperatively(ManagerProperty, tables["manager_properties"])
