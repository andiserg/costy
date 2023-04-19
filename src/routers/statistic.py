from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.operations import get_operations
from src.app.services.statistic import get_statistic
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user_depend, get_uow
from src.schemas.statistic import StatisticSchema

router = APIRouter(prefix="/statistic")


@router.get("/", response_model=StatisticSchema, status_code=200)
async def get_statistic_view(
    current_user: User = Depends(get_current_user_depend),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    operations = await get_operations(uow, current_user.id)
    return get_statistic(operations)
