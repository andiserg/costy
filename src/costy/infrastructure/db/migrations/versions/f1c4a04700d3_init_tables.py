"""init tables

Revision ID: f1c4a04700d3
Revises:
Create Date: 2024-01-30 22:55:38.115617

"""
import json
from importlib import resources
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from costy.infrastructure.db.main import get_metadata
from costy.infrastructure.db.tables import create_tables

# revision identifiers, used by Alembic.
revision: str = "f1c4a04700d3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("users",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("email", sa.String(), nullable=False),
    sa.Column("hashed_password", sa.String(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table("categories",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=True),
    sa.Column("kind", sa.String(), nullable=True),
    sa.Column("view", sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_table("operations",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("amount", sa.Integer(), nullable=False),
    sa.Column("description", sa.String(), nullable=True),
    sa.Column("time", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=True),
    sa.Column("category_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
    sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###

    metadata = get_metadata()
    tables = create_tables(metadata)

    with open(str(resources.files("costy.infrastructure.db") / "_default_categories.json")) as f:
        categories_data: list[dict] = json.load(f)

    categories = [
        {
            "name": item["name"],
            "kind": "general",
            "user_id": None,
            "view": item["view"],
        } for item in categories_data
    ]

    op.bulk_insert(tables["categories"], categories)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("operations")
    op.drop_table("categories")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
