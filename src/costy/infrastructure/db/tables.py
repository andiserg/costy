from sqlalchemy import JSON, Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()


operations = Table(
    "operations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("amount", Integer, nullable=False),
    Column("description", String),
    Column("time", Integer, nullable=False),
    Column("user_id", Integer),
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id"),
        nullable=True,
    ),
    Column("bank_name", String, nullable=True),
)

categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("user_id", Integer, nullable=True),
    Column("kind", String, default="general"),
    Column("view", JSON, nullable=True),
)

bankapis = Table(
    "bankapis",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("access_data", JSON),
    Column("updated_at", Integer, nullable=True),
    Column("user_id", Integer),
)

category_mcc = Table(
    "category_mcc",
    metadata,
    Column("category_id", Integer, ForeignKey("categories.id")),
    Column("mcc", Integer),
)
