from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from src.app.domain.bank_api import BankInfo, BankInfoProperty
from src.app.repositories.absctract.bank_api import ABankInfoRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class BankInfoRepository(SqlAlchemyRepository, ABankInfoRepository):
    async def get(self, field, value) -> BankInfo:
        return await self._get(BankInfo, field, value)

    async def get_all_by_user(self, user_id):
        return list(
            await self.session.scalars(
                select(BankInfo)
                .filter_by(user_id=user_id)
                .options(subqueryload(BankInfo.properties))
            )
        )

    async def get_properties(self, manager: BankInfo) -> dict[str, str | int | float]:
        result_dict = {
            "id": manager.id,
            "user_id": manager.user_id,
            "bank_name": manager.bank_name,
        }
        properties = await self.session.scalars(
            select(BankInfoProperty).filter_by(manager_id=manager.id)
        )
        result_dict.update({prop.name: prop.value for prop in properties})
        return result_dict

    async def add_property(
        self, manager: BankInfo, name: str, value: str | int | float
    ):
        types = {str: "str", int: "int", float: "float"}
        self.session.add(
            BankInfoProperty(
                name=name,
                value=str(value),
                value_type=types[type(value)],
                manager_id=manager.id,
            )
        )
