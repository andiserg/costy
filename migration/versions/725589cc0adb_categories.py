"""categories

Revision ID: 725589cc0adb
Revises: 79110a6de7e7
Create Date: 2023-05-10 11:00:59.952790

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "725589cc0adb"
down_revision = "79110a6de7e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("operations", sa.Column("category_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "operations", "categories", ["category_id"], ["id"])
    op.drop_column("operations", "mcc")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "operations", sa.Column("mcc", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "operations", type_="foreignkey")
    op.drop_column("operations", "category_id")
    op.drop_table("categories")
    # ### end Alembic commands ###
