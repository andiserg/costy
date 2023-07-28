from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.bank_api import (
    add_bank_info,
    get_bank_managers_by_user,
    update_banks_costs,
)
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow

router = APIRouter(prefix="/bankapi")


@router.post("/", status_code=201)
async def create_bank_info_view(
    props: dict,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Create bank info record
    :param props: bank info props
    :param current_user: user
    :param uow: unit of work
    :return: 201 | 400
    """
    await add_bank_info(uow, current_user.id, props)
    return {"status": "created"}


@router.put("/costs/", status_code=200)
async def update_costs_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Update costs by banks API
    :param current_user: user
    :param uow: unit of work
    :return: 200
    """
    managers = await get_bank_managers_by_user(uow, user_id=current_user.id)
    await update_banks_costs(uow, managers)
    return {"status": "ok"}


@router.get("/", status_code=200)
async def get_connected_banks_names(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> list[str]:
    """
    Get connected banks
    :param current_user:
    :param uow:
    :return: 200, banks list
    """
    async with uow:
        managers = await uow.banks_info.get_all_by_user(current_user.id)
        return [manager.bank_name for manager in managers]


@router.delete("/", status_code=204)
async def delete_bank(
    bank_name: str,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Delete bank info record
    :param bank_name: bank name
    :param current_user: user
    :param uow: unit of work
    :return: 204
    """
    await uow.banks_info.delete(current_user.id, bank_name)
    await uow.commit()
