from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.operations import get_operations
from src.app.services.statistic import get_statistic
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow
from src.schemas.statistic import StatisticSchema

router = APIRouter(prefix="/statistic")


@router.get("/", response_model=StatisticSchema, status_code=200)
async def get_statistic_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
    from_time: int = None,
    to_time: int = None,
):
    from_time = from_time if from_time else datetime.today().timestamp()
    to_time = to_time if to_time else (datetime.today() + timedelta(days=1)).timestamp()
    operations = await get_operations(uow, current_user.id, from_time, to_time)
    return get_statistic(operations)
