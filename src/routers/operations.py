from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from src.app.domain.users import User
from src.app.services.operations import create_operation, get_operations
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.depends import get_current_user, get_uow
from src.schemas.operations import OperationCreateSchema, OperationSchema

router = APIRouter(prefix="/operations")


@router.post("/", response_model=OperationSchema, status_code=201)
async def create_operation_view(
    operation_schema: OperationCreateSchema,
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    """
    Create and return an operation.

    :param uow: Unit of Work
    :param operation_schema: JSON, which will be parsed into OperationCreateSchema.
    :param current_user: User decrypted from the token in the Authorization header.
    :return: Operation object or Error 400.
    """
    return await create_operation(uow, current_user.id, operation_schema)


@router.get("/", response_model=list[OperationSchema])
async def read_operations_view(
    current_user: User = Depends(get_current_user),
    uow: AbstractUnitOfWork = Depends(get_uow),
    from_time: int | None = None,
    to_time: int | None = None,
):
    """
    Returns a list of operations for the current user.

    :param uow: Unit of Work
    :param current_user: User decrypted from the token in the Authorization header.
    :param from_time: Starting time in Unix format.
    :param to_time: Ending time in Unix format.
    :return: List of operations.
    """
    from_time = (
        from_time
        if from_time
        else int((datetime.now() - timedelta(minutes=1)).timestamp())
    )
    to_time = to_time if to_time else int(datetime.now().timestamp())
    return await get_operations(uow, current_user.id, from_time, to_time)
