from fastapi import APIRouter, UploadFile, File, Depends

from app.managers.file import file_manager
from app.models import Task
from app.repositories.task import task_repository
from app.schemas.task import TaskResponseSchema
from app.services.task import process_file_task
from app.settings.db import get_session

router = APIRouter(
    prefix="",
    tags=["Distance"],
)


@router.post("/calculateDistance", response_model=TaskResponseSchema)
async def calculate_distance(
        file: UploadFile = File(...),
        db_session=Depends(get_session)
):
    file_path = await file_manager.save(file)
    task: Task = await task_repository.create(db_session)

    process_file_task.delay(file_path, task.id)

    return task
