"""
Технічні особливості побудови таблиць в ORM
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from src.app.domain.bank_api import BankInfo, BankInfoProperty
from src.app.domain.categories import Category
from src.app.domain.limits import Limit
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
            Column("time", Integer, nullable=False),
            # mcc - код виду операції
            Column("source_type", String, nullable=False),
            # Тип джерела.
            # value: "manual" | "<bank_name>"
            # Операція може бути або додана вручну або за допомогою API банку
            Column("user_id", Integer, ForeignKey("users.id")),
            Column("category_id", Integer, ForeignKey("categories.id"), nullable=True),
        ),
        "banks_info": Table(
            "banks_info",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("bank_name", String, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id")),
        ),
        "banks_info_properties": Table(
            "banks_info_properties",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("prop_name", String, nullable=False),
            Column("prop_value", String, nullable=False),
            Column("prop_type", String, nullable=False),
            Column("manager_id", Integer, ForeignKey("banks_info.id")),
        ),
        "categories": Table(
            "categories",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id"), nullable=True),
            Column("type", String, default="system"),
            Column("icon_name", String, nullable=True, default=None),
            Column("icon_color", String, nullable=True, default=None),
            Column("parent_id", Integer, ForeignKey("categories.id"), nullable=True),
        ),
        "limits": Table(
            "limits",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", Integer, ForeignKey("users.id")),
            Column("category_id", Integer, ForeignKey("categories.id"), nullable=True),
            Column("limit", Integer),
            Column("date_range", String),
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
        properties={"managers": relationship(BankInfo, backref="user")},
    )
    mapper_registry.map_imperatively(Operation, tables["operations"])
    mapper_registry.map_imperatively(
        BankInfo,
        tables["banks_info"],
        properties={"properties": relationship(BankInfoProperty, backref="manager")},
    )
    mapper_registry.map_imperatively(
        BankInfoProperty,
        tables["banks_info_properties"],
    )
    mapper_registry.map_imperatively(Category, tables["categories"])
    mapper_registry.map_imperatively(Limit, tables["limits"])
