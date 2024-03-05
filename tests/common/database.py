from pytest_asyncio import fixture
from sqlalchemy import Table, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.domain.models.category import CategoryId
from costy.domain.models.user import UserId


async def create_category(session: AsyncSession, table: Table) -> CategoryId:
    created_category_record = await session.execute(insert(table).values(name="test"))
    await session.commit()
    return CategoryId(created_category_record.inserted_primary_key[0])


async def create_user(session: AsyncSession, table: Table, auth_id: str = "test") -> UserId:
    stmt = select(table).where(table.c.auth_id == auth_id)
    result = next((await session.execute(stmt)).mappings(), None)
    if result:
        return result["id"]
    created_user_record = await session.execute(insert(table).values(auth_id=auth_id))
    await session.commit()
    return UserId(created_user_record.inserted_primary_key[0])


@fixture
async def clean_up_db(db_session, db_tables):
    tables_order = ["operations", "categories", "users"]
    yield
    for table in tables_order:
        await db_session.execute(delete(db_tables[table]))
    await db_session.commit()
