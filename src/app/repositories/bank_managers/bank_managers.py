from sqlalchemy import select

from src.app.domain.bank_managers import Manager, ManagerProperty
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class ManagerRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> Manager:
        return await self._get(Manager, field, value)

    async def get_all_by_user(self, user_id):
        return list(
            await self.session.scalars(select(Manager).filter_by(user_id=user_id))
        )

    async def get_properties(self, manager: Manager) -> dict[str, str | int | float]:
        result_dict = {
            "id": manager.id,
            "user_id": manager.user_id,
            "bank_name": manager.bank_name,
        }
        properties = await self.session.scalars(
            select(ManagerProperty).filter_by(manager_id=manager.id)
        )
        result_dict.update({prop.name: prop.value for prop in properties})
        return result_dict

    async def add_property(self, manager: Manager, name: str, value: str | int | float):
        types = {str: "str", int: "int", float: "float"}
        self.session.add(
            ManagerProperty(
                name=name,
                value=str(value),
                value_type=types[type(value)],
                manager_id=manager.id,
            )
        )
