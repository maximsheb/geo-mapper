import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship

from app.constant.task_status_enum import TaskStatusEnum
from app.models.base import Base


class Task(Base):
    __tablename__ = "Task"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, nullable=False)

    points = relationship("GeoPoint", back_populates="task")
    links = relationship("LinkedDistance", back_populates="task")

    @property
    def data(self):
        return {
            "points": [
                {"name": point.name, "address": point.address} for point in
                self.points
            ],
            "links": [
                {"name": link.name, "distance": link.distance} for link in
                self.links
            ],
        } if self.status == TaskStatusEnum.DONE.value else {}
