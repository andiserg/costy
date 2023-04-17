from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.bank_api import add_bank_info
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
