import uuid

from sqlalchemy import Column, UUID, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.base import Base


class GeoPoint(Base):
    __tablename__ = "GeoPoint"
    __table_args__ = (
        Index('idx_task_id', 'task_id'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("Task.id"))

    task = relationship("Task", back_populates="points")
