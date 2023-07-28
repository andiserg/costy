from datetime import datetime, timedelta

from src.app.domain.bank_api import BankInfo, BankInfoProperty
from src.app.domain.operations import Operation
from src.app.repositories.absctract.bank_api import (
    ABankManagerRepository,
    BankManagerRepositoryFactory,
)
from src.app.repositories.categories import CategoryMccFacade
from src.app.services.categories import get_categories_in_values
from src.app.services.uow.abstract import AbstractUnitOfWork


async def add_bank_info(uow: AbstractUnitOfWork, user_id: int, props: dict):
    """
    Storing a BankInfo instance and saving it to the database.

    :param uow: Unit of Work
    :param user_id: User ID
    :param props: Properties. Must include bank_name.
    :return: BankInfo instance.
    """
    async with uow:
        bank_info = BankInfo(props.get("bank_name"), user_id)
        await uow.banks_info.add(bank_info)
        del props["bank_name"]
        for key, value in props.items():
            # All other properties, except bank_name,
            # are stored as BankInfoProperty with a foreign key to BankInfo.
            await uow.banks_info.add(
                BankInfoProperty(
                    prop_name=key, prop_value=value, prop_type="str", manager=bank_info
                )
            )
        # TEMP
        await uow.banks_info.add(
            BankInfoProperty(
                prop_name="updated_time",
                prop_value=str(int((datetime.now() - timedelta(30)).timestamp())),
                prop_type="int",
                manager=bank_info,
            )
        )
        await uow.commit()


async def get_bank_managers_by_user(
    uow: AbstractUnitOfWork, user_id: int
) -> list[ABankManagerRepository]:
    """
    Converting BankInfo objects into BankManagerRepository.

    :param uow: Unit of Work
    :param user_id: User ID
    :return: List of Bank Managers.
    """
    async with uow:
        bank_info_list = await uow.banks_info.get_all_by_user(user_id)
        properties_list = [bank.get_properties_as_dict() for bank in bank_info_list]
        return [
            BankManagerRepositoryFactory.create_bank_manager(properties)
            for properties in properties_list
        ]


async def update_banks_costs(
    uow: AbstractUnitOfWork, managers: list[ABankManagerRepository]
):
    """
    Updating the list of financial expenses using the banks' APIs.
    :param uow: unit of work (fastapi depend)
    :param managers: list of an ABankManagerRepository implements objects
    :return: None
    """
    if len(managers) == 0:
        return
    async with uow:
        costs = []
        updated_managers = []
        for manager in managers:
            bank_costs = await get_costs_by_bank(manager)
            if bank_costs:
                costs += bank_costs
                updated_managers.append(manager)
        mcc_categories = await get_categories_id_by_mcc(uow, costs)
        operations = create_operations_by_bank_costs(costs, mcc_categories)
        for operation in operations:
            await uow.operations.add(operation)
        await uow.banks_info.set_update_time_to_managers(
            [manager.properties["id"] for manager in updated_managers]
        )
        await uow.commit()


async def get_costs_by_bank(manager) -> list[Operation] | None:
    updated_time = get_updated_time(manager)
    if updated_time:
        bank_costs = await manager.get_costs(from_time=updated_time)
        if bank_costs:
            return bank_costs


async def get_categories_id_by_mcc(uow: AbstractUnitOfWork, costs) -> dict[int, int]:
    """Створення та повернення словника вигляду {mcc: category_id}"""
    categories_names_dct = {
        cost["mcc"]: CategoryMccFacade.get_category_name_by_mcc(cost["mcc"])
        for cost in costs
    }
    categories_list = await get_categories_in_values(
        uow, "name", list(categories_names_dct.values())
    )
    result_dct = {}
    for key, value in categories_names_dct.items():
        result_dct[key] = next(
            category.id for category in categories_list if category.name == value
        )
    return result_dct


def create_operations_by_bank_costs(costs, mcc_categories) -> list[Operation]:
    return [
        Operation(
            amount=cost["amount"],
            description=cost["description"],
            time=cost["time"],
            source_type=cost["source_type"],
            user_id=cost["user_id"],
            category_id=mcc_categories[cost["mcc"]],
        )
        for cost in costs
    ]


def get_updated_time(manager: ABankManagerRepository) -> int | None:
    """
    Determining the correct update date using validations.

     :param manager: BankManagerRepository
     :return:
         - date timestamp
         - None: Data was updated less than 1 minute ago.
    """
    updated_time_prop = manager.properties.get("updated_time")
    max_update_period = datetime.now() - manager.MAX_UPDATE_PERIOD
    if updated_time_prop:
        updated_time = datetime.fromtimestamp(updated_time_prop)
        if not datetime.now() - updated_time < manager.MAX_UPDATE_PERIOD:
            # Якщо остання дата оновлення перевищує максимальний період оновлення
            updated_time = max_update_period
            # У кожного банка є максиммальна дата, на яку можна запитувати витрати
            # Якщо менеджер оновляв дані раніше цієї дати,
            # то максимальною датою ставиться та, яка в обмеженні
    else:
        updated_time = max_update_period
    if updated_time < datetime.now() - timedelta(minutes=1):
        # Відкат в 1 хвилину за для запобігання непотрібної загрузки даних
        return int(updated_time.timestamp())
    return None
