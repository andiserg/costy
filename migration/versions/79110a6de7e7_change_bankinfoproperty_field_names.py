"""change BankInfoProperty field names

Revision ID: 79110a6de7e7
Revises: 86f9d6304908
Create Date: 2023-05-02 23:57:37.004802

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "79110a6de7e7"
down_revision = "86f9d6304908"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "banks_info_properties", sa.Column("prop_name", sa.String(), nullable=False)
    )
    op.add_column(
        "banks_info_properties", sa.Column("prop_value", sa.String(), nullable=False)
    )
    op.add_column(
        "banks_info_properties", sa.Column("prop_type", sa.String(), nullable=False)
    )
    op.drop_column("banks_info_properties", "name")
    op.drop_column("banks_info_properties", "type")
    op.drop_column("banks_info_properties", "value")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "banks_info_properties",
        sa.Column("value", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "banks_info_properties",
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "banks_info_properties",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("banks_info_properties", "prop_type")
    op.drop_column("banks_info_properties", "prop_value")
    op.drop_column("banks_info_properties", "prop_name")
    # ### end Alembic commands ###