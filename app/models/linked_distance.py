import uuid

from sqlalchemy import Column, UUID, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class LinkedDistance(Base):
    __tablename__ = "LinkedDistance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    distance = Column(Float, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("Task.id"))

    task = relationship("Task", back_populates="links")
