from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.bank_api import (
    add_bank_info,
    get_bank_managers_by_user,
    update_banks_costs,
)
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user_depend, get_uow

router = APIRouter(prefix="/bankapi")


@router.post("/add/", status_code=201)
async def add_bank_info_view(
    props: dict,
    current_user: User = Depends(get_current_user_depend),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    await add_bank_info(uow, current_user.id, props)
    return {"status": "created"}


@router.put("/update_costs/", status_code=200)
async def update_costs_view(
    current_user: User = Depends(get_current_user_depend),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    managers = await get_bank_managers_by_user(uow, user_id=current_user.id)
    await update_banks_costs(uow, managers)
    return


@router.get("/list/", status_code=200)
async def get_connected_banks_names(
    current_user: User = Depends(get_current_user_depend),
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> list[str]:
    async with uow:
        managers = await uow.banks_info.get_all_by_user(current_user.id)
        return [manager.bank_name for manager in managers]
