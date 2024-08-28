from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import GeoPoint, LinkedDistance
from app.utils.logger import logger


class ResultRepository:
    @classmethod
    async def create(
            cls,
            geo_points: list[GeoPoint],
            linked_distances: list[LinkedDistance],
            db_session: AsyncSession,
    ) -> None:
        """
        Create geo points and linked distances in db
        :param geo_points: list of geo points objects
        :param linked_distances: list of linked distances objects
        :param db_session: db session
        :return: function doesn't return anything after successful finishing
        """
        db_session.add_all(geo_points)
        db_session.add_all(linked_distances)
        try:
            await db_session.flush()
        except (IntegrityError, OperationalError, DatabaseError) as e:
            await db_session.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
