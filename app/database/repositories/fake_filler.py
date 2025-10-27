from typing import List
from sqlalchemy import select, text

from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import (
    Building, 
    Activity, 
    Organization, 
    OrganizationPhone,
    organization_activities
)

class FakeFillerRepository:
    """Репозиторий для заполнения базы данных тестовыми данными"""
    
    def __init__(self, db_helper: AsyncDatabaseHelper):
        self.db_helper = db_helper

    async def create_activities(self, activities: List[Activity]) -> List[Activity]:
        """Создает виды деятельности в базе данных"""
        async with self.db_helper.session_only() as session:
            session.add_all(activities)
            await session.commit()
            return activities

    async def create_buildings(self, buildings: List[Building]) -> List[Building]:
        """Создает здания в базе данных"""
        async with self.db_helper.session_only() as session:
            session.add_all(buildings)
            await session.commit()
            return buildings

    async def create_organizations(self, organizations: List[Organization]) -> List[Organization]:
        """Создает организации в базе данных"""
        async with self.db_helper.session_only() as session:
            session.add_all(organizations)
            await session.flush()  # Получаем ID
            await session.commit()
            return organizations

    async def create_organization_phones(self, phones: List[OrganizationPhone]) -> List[OrganizationPhone]:
        """Создает телефоны организаций в базе данных"""
        async with self.db_helper.session_only() as session:
            session.add_all(phones)
            await session.commit()
            return phones

    async def create_organization_activity_relations(self, relations: List[dict]) -> None:
        """Создает связи между организациями и видами деятельности"""
        async with self.db_helper.session_only() as session:
            for relation in relations:
                stmt = organization_activities.insert().values(**relation)
                await session.execute(stmt)
            await session.commit()

    async def get_all_activities(self) -> List[Activity]:
        """Получает все виды деятельности из базы данных"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Activity))
            return result.scalars().all()

    async def get_all_buildings(self) -> List[Building]:
        """Получает все здания из базы данных"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Building))
            return result.scalars().all()

    async def get_all_organizations(self) -> List[Organization]:
        """Получает все организации из базы данных"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization))
            return result.scalars().all()

    async def clear_organization_activities(self) -> None:
        """Очищает таблицу связей организация-деятельность"""
        async with self.db_helper.session_only() as session:
            await session.execute(text("DELETE FROM organization_activities"))
            await session.commit()

    async def clear_organization_phones(self) -> None:
        """Очищает таблицу телефонов организаций"""
        async with self.db_helper.session_only() as session:
            await session.execute(text("DELETE FROM organization_phones"))
            await session.commit()

    async def clear_organizations(self) -> None:
        """Очищает таблицу организаций"""
        async with self.db_helper.session_only() as session:
            await session.execute(text("DELETE FROM organizations"))
            await session.commit()

    async def clear_activities(self) -> None:
        """Очищает таблицу видов деятельности"""
        async with self.db_helper.session_only() as session:
            await session.execute(text("DELETE FROM activities"))
            await session.commit()

    async def clear_buildings(self) -> None:
        """Очищает таблицу зданий"""
        async with self.db_helper.session_only() as session:
            await session.execute(text("DELETE FROM buildings"))
            await session.commit()

    async def clear_all_tables(self) -> None:
        """Очищает все таблицы в правильном порядке из-за внешних ключей"""
        await self.clear_organization_activities()
        await self.clear_organization_phones()
        await self.clear_organizations()
        await self.clear_activities()
        await self.clear_buildings()

    async def get_activities_count(self) -> int:
        """Получает количество видов деятельности"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(text("COUNT(*) FROM activities")))
            return result.scalar()

    async def get_buildings_count(self) -> int:
        """Получает количество зданий"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(text("COUNT(*) FROM buildings")))
            return result.scalar()

    async def get_organizations_count(self) -> int:
        """Получает количество организаций"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(text("COUNT(*) FROM organizations")))
            return result.scalar()

    async def get_organization_phones_count(self) -> int:
        """Получает количество телефонов организаций"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(text("COUNT(*) FROM organization_phones")))
            return result.scalar()

    async def get_organization_activities_count(self) -> int:
        """Получает количество связей организация-деятельность"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(text("COUNT(*) FROM organization_activities")))
            return result.scalar()
