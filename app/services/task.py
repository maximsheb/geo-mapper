import asyncio
import os

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.managers.file import FileManager
from app.repositories.result import ResultRepository
from app.repositories.task import TaskRepository
from app.settings.db import get_session_context
from celery_worker import celery_app


@celery_app.task
def process_file_task(file_path: str, task_id: UUID) -> None:
    """
    Process file task and save results to db
    :param file_path: str path to csv file object
    :param task_id: uuid of task
    :return: function doesn't return anything after successful finishing
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_process_file(file_path, task_id))


async def run_process_file(file_path: str, task_id: UUID):
    """
    Run process file task and save results to db
    :param file_path: str path to csv file object
    :param task_id: uuid task id
    :return: function doesn't return anything after successful finishing
    """
    async with get_session_context() as db_session:
        await process_file(file_path, task_id, db_session)


async def process_file(
        file_path: str,
        task_id: UUID,
        db_session: AsyncSession
) -> None:
    """
    Process file task and save results to db
    :param file_path: path to csv file object
    :param task_id: uuid of task
    :param db_session: db session
    :return: function doesn't return anything after successful finishing
    """
    try:
        task_repository = TaskRepository()
        result_repository = ResultRepository()
        file_manager = FileManager()

        async for chunk in file_manager.read_in_chunks(file_path):
            geo_points, linked_distances = await file_manager.process_chunk(
                chunk, task_id
            )
            await result_repository.create(geo_points, linked_distances, db_session)
        await task_repository.finish(task_id, db_session)
    finally:
        # remove file after processing
        # os.remove(file_path)
        ...
