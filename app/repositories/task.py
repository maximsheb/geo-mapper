import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constant.task_status_enum import TaskStatusEnum
from app.models import Task
from app.utils.logger import logger


class TaskRepository:
    @classmethod
    async def create(cls, db_session: AsyncSession) -> Task:
        """
        Creates task in db
        :param db_session: db session
        :return: function doesn't return anything after successful finishing
        """
        task = Task(status=TaskStatusEnum.RUNNING.value)
        db_session.add(task)
        try:
            await db_session.commit()
            return task
        except (IntegrityError, OperationalError, DatabaseError) as e:
            await db_session.rollback()
            logger.error(f"Database operation failed: {e}")
            raise

    @classmethod
    async def update(cls, task_id: uuid, db_session: AsyncSession) -> None:
        """
        Updates task status
        :param task_id: uuid of task
        :param db_session: db session
        :return: function doesn't return anything after successful finishing
        """
        db_task: Task = await cls.get_by_id(task_id, db_session)

        db_task.status = TaskStatusEnum.DONE.value
        db_session.add(db_task)
        try:
            await db_session.commit()
        except (IntegrityError, OperationalError, DatabaseError) as e:
            await db_session.rollback()
            logger.error(f"Database operation failed: {e}")
            raise

    @classmethod
    async def get_by_id(cls, task_id: uuid, db_session: AsyncSession) -> Task:
        """
        Get task by id
        :param task_id: uuid of task
        :param db_session: db session
        :return: Task db object
        """
        task: Task | None = (
            await db_session.scalars(
                select(Task)
                .options(selectinload(Task.points), selectinload(Task.links))
                .where(Task.id == task_id)
            )
        ).first()

        if not task:
            raise HTTPException(
                status_code=404, detail=f"Task not found with id: {task_id}"
            )

        return task


task_repository = TaskRepository()
