import contextlib
from typing import AsyncIterable, Annotated
from config import config as app_config
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._session_maker: AsyncSession | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._session_maker = async_sessionmaker(bind=self._engine, autocommit=False)

    async def close(self):
        if self._engine is None:
            raise Exception(
                f"DatabaseSessionManager is not initialized {'(in close method)' if app_config.DEBUG else ''}"
            )
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterable[AsyncConnection]:
        if self._engine is None:
            raise Exception(
                f"DatabaseSessionManager is not initialized {'(in connect method)' if app_config.DEBUG else ''}"
            )

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterable[AsyncSession]:
        if self._session_maker is None:
            raise Exception(
                f"DatabaseSessionManager is not initialized {'(in session method)' if app_config.DEBUG else ''}"
            )
        session = self._session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DatabaseSessionManager()


async def get_db():
    async with session_manager.session() as session:
        yield session


db_session = Annotated[AsyncSession, Depends(get_db)]
