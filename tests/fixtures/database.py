from pytest_asyncio import fixture
from sqlalchemy import delete, insert, select

from costy.domain.models.category import CategoryId
from costy.domain.models.user import UserId


@fixture
async def db_category_id(db_session, db_tables) -> CategoryId:
    created_category_record = await db_session.execute(insert(db_tables["categories"]).values(name="test"))
    await db_session.commit()
    return CategoryId(created_category_record.inserted_primary_key[0])


@fixture
async def db_user_id(db_session, db_tables) -> UserId:
    stmt = select(db_tables["users"]).where(db_tables["users"].c.auth_id == "test")
    result = next((await db_session.execute(stmt)).mappings(), None)
    if result:
        return result["id"]
    created_user_record = await db_session.execute(insert(db_tables["users"]).values(auth_id="test"))
    return UserId(created_user_record.inserted_primary_key[0])


@fixture()
async def created_auth_user(db_session, db_tables, auth_id) -> UserId:
    result = await db_session.execute(insert(db_tables["users"]).values(auth_id=auth_id))
    return UserId(result.inserted_primary_key[0])


@fixture
async def create_sub_user(db_session, db_tables, auth_sub) -> UserId:
    result = await db_session.execute(insert(db_tables["users"]).values(auth_id=auth_sub.replace("auth0|", "")))
    await db_session.commit()
    return UserId(result.inserted_primary_key[0])


@fixture
async def clean_up_db(db_session, db_tables):
    tables_order = ["operations", "categories", "users"]
    yield
    for table in tables_order:
        await db_session.execute(delete(db_tables[table]))
    await db_session.commit()
