from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.limits import create_limit, delete_limit, get_limits
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow
from src.schemas.limits import LimitCreateSchema, LimitSchema

router = APIRouter(prefix="/limits")


@router.post("/create/", response_model=LimitSchema, status_code=201)
async def create_limit_view(
    limit_schema: LimitCreateSchema,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return await create_limit(uow, current_user.id, limit_schema)


@router.get("/list/", response_model=list[LimitSchema])
async def read_limits_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return await get_limits(uow, current_user.id)


@router.delete("/delete/", status_code=204)
async def delete_limit_view(
    limit_id: int,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    await delete_limit(uow, limit_id)
    await uow.commit()
