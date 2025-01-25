from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import tables as auth_tables
from costy.domain.models.category import CategoryId
from costy.infrastructure.db import tables as costy_tables


async def create_category(session: AsyncSession) -> CategoryId:
    created_category_record = await session.execute(insert(costy_tables.categories).values(name="test"))
    await session.commit()
    return CategoryId(created_category_record.inserted_primary_key[0])


async def create_user(session: AsyncSession, auth_id: str = "test") -> int:
    stmt = select(auth_tables.users).where(auth_tables.users.c.auth_id == auth_id)
    result = next((await session.execute(stmt)).mappings(), None)
    if result:
        return result["id"]

    created_user_record = await session.execute(insert(auth_tables.users).values(auth_id=auth_id))
    await session.commit()
    return created_user_record.inserted_primary_key[0]
