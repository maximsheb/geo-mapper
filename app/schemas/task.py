from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.constant.task_status_enum import TaskStatusEnum
from app.schemas.geo_point import GeoPointSchema
from app.schemas.linked_distance import LinkedDistanceSchema


class TaskDataSchema(BaseModel):
    points: list[GeoPointSchema] | None = None
    links: list[LinkedDistanceSchema] | None = None

    class Config:
        from_attributes = True


class TaskResponseSchema(BaseModel):
    task_id: UUID = Field(..., alias='id')
    status: str

    class Config:
        from_attributes = True


class ExtendedTaskResponseSchema(BaseModel):
    task_id: UUID = Field(..., alias='id')
    status: str
    data: TaskDataSchema | dict = {}

    @model_validator(mode="after")
    def check_status_and_modify_data(cls, values):
        if values.status != TaskStatusEnum.DONE.value:
            values.data = {}
        return values

    class Config:
        from_attributes = True
