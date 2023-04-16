from datetime import datetime, timedelta

from src.app.repositories.absctract.bank_api import (
    ABankManagerRepository,
    BankManagerRepositoryFactory,
)
from src.app.services.uow.abstract import AbstractUnitOfWork


async def get_bank_managers_by_user(
    uow: AbstractUnitOfWork, user_id: int
) -> list[ABankManagerRepository]:
    """
    Взяття об'єктів BankInfo та перетворення їх у BankManagerRepository
    :param uow: Unit of Work
    :param user_id: id користувача
    :return: список Bank Manager
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
    async with uow:
        costs = []
        for manager in managers:
            updated_time = get_updated_time(manager)
            if updated_time:
                costs.append(*await manager.get_costs(from_time=updated_time))
        for cost in costs:
            await uow.operations.add(cost)
        await uow.commit()


def get_updated_time(manager: ABankManagerRepository) -> int | None:
    """
    Визначення корректної дати оновлення за допомогою валідацій
    :param manager: BankManagerRepository
    :return:
        - date timestamp
        - None: Оновлення даних відбувалось менш ніж 1 хвилину тому
    """
    updated_time_prop = manager.properties.get("updated_time")
    max_update_period = datetime.now() - manager.MAX_UPDATE_PERIOD
    if updated_time_prop:
        updated_time = datetime.fromtimestamp(updated_time_prop)
        if not datetime.now() - updated_time < max_update_period:
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
