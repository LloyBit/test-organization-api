from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

class AsyncDatabaseHelper:
    """Асинхронный хелпер для работы с БД и управлением сессиями."""

    def __init__(self, database_url: str):
        self.database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

        self.engine = None
        self.async_session_factory = None
        self.Base = declarative_base()

    async def connect(self):
        """Создает подключение и инициализирует пул соединений."""
        if self.engine:
            return  # уже инициализирован

        self.engine = create_async_engine(
            self.database_url,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_timeout=30
        )
        
        self.async_session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session_only(self) -> AsyncGenerator[AsyncSession, None]:
        """Контекстный менеджер для работы с сессией"""
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self):
        """Закрывает соединения и пул."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.async_session_factory = None
