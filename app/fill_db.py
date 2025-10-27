import asyncio
from app.config import Settings
from app.database.db_helper import AsyncDatabaseHelper
from app.services.fake_filler import FakeFiller

async def main():
    settings = Settings()
    db_helper = AsyncDatabaseHelper(settings.db_url)
    
    try:
        await db_helper.connect()
        print("Подключение к базе данных установлено")
        
        filler = FakeFiller(db_helper)
        await filler.fill_database(10000)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        await db_helper.close()
        print("Соединение с базой данных закрыто")

if __name__ == "__main__":
    asyncio.run(main())