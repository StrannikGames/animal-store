from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from animal_store.models import Base


class DatabaseManager:
    def __init__(self, db_url: str):
        self.__db_url = db_url

    async def __aenter__(self):
        self.__engine = create_async_engine(self.__db_url)
        self.__session_maker = async_sessionmaker(
            self.__engine, autoflush=False, expire_on_commit=False
        )

        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.__engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        async with self.__session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def session_dependency(self):
        """Зависимость FastAPI: одна сессия на запрос."""
        async with self.get_session() as session:
            yield session
