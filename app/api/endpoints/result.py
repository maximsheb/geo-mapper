from uuid import UUID

from fastapi import APIRouter, Query, Depends

from app.repositories.task import TaskRepository
from app.schemas.task import ExtendedTaskResponseSchema
from app.settings.db import get_session

router = APIRouter(
    prefix="",
    tags=["Result"],
)


@router.get("/getResult", response_model=ExtendedTaskResponseSchema)
async def get_result_by_task_id(
        task_id: UUID = Query(),
        db_session=Depends(get_session)
):
    task_repository = TaskRepository()
    return await task_repository.get_by_id(task_id, db_session)
