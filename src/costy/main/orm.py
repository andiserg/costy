from typing import Type

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

from costy.domain.models.category import Category
from costy.domain.models.operation import Operation
from costy.domain.models.user import User


def create_tables(mapper_registry: registry) -> dict[Type, Table]:
    return {
        User: Table(
            "users",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("email", String, unique=True, index=True, nullable=False),
            Column("hashed_password", String, nullable=False),
        ),
        Operation: Table(
            "operations",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("amount", Integer, nullable=False),
            Column("description", String),
            Column("time", Integer, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id")),
            Column("category_id", Integer, ForeignKey("categories.id"), nullable=True),
        ),
        Category: Table(
            "categories",
            mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id"), nullable=True),
            Column("kind", String, default="general"),
        ),
    }


def map_tables_to_models(mapper_registry: registry, tables: dict[Type, Table]):
    for model, table in tables.items():
        mapper_registry.map_imperatively(model, table)
