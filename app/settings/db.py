from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import app_config

engine = create_async_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # noqa


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
