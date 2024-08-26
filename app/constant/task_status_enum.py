from enum import Enum


class TaskStatusEnum(str, Enum):
    RUNNING = "running"
    DONE = "done"
