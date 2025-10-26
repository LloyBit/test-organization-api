""" Точка входа в основное приложение """
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.config import Settings

from app.presentation.api import router as organizations_router
from app.presentation.middleware import AuthMiddleware
from app.service import OrganizationsService
from app.database.repository import OrganizationsRepository
from app.database.db_helper import AsyncDatabaseHelper

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Обработчик событий жизненного цикла FastAPI"""

    db_helper = AsyncDatabaseHelper(settings.db_url)
    
    await db_helper.connect()
    
    app.state.repository = OrganizationsRepository(db_helper)
    app.state.service = OrganizationsService(repository=app.state.repository)
    
    yield

    await db_helper.close()

    
app = FastAPI(title="QR-Blockchain Server", version="1.0.0", lifespan=lifespan)

# Middleware для аутентификации
app.add_middleware(AuthMiddleware)

# Подключаем предварительно собранные роуты
app.include_router(organizations_router)
