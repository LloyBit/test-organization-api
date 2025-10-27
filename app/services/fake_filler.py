import random
from uuid import uuid4
from faker import Faker
from geoalchemy2 import WKTElement

from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import (
    Building, 
    Activity, 
    Organization, 
    OrganizationPhone
)
from app.database.repositories.fake_filler import FakeFillerRepository


class FakeFiller():
    def __init__(self, db_helper: AsyncDatabaseHelper):
        self.fake = Faker(['ru_RU'])  # Русская локализация
        self.db_helper = db_helper
        self.repository = FakeFillerRepository(db_helper)

    async def create_activities(self, count: int = 50):
        """Создает виды деятельности с иерархической структурой"""
        activities = []
        
        # Создаем основные категории (родительские)
        main_categories = [
            "Образование", "Медицина", "Торговля", "Общепит", "Услуги",
            "Производство", "Строительство", "Транспорт", "Финансы", "IT"
        ]
        
        parent_activities = []
        for category in main_categories:
            activity = Activity(
                id=uuid4(),
                name=category,
                parent_id=None,
                level=1
            )
            activities.append(activity)
            parent_activities.append(activity)
        
        # Создаем подкатегории для каждой основной категории
        subcategories_per_category = count // len(main_categories)
        for parent in parent_activities:
            for _ in range(subcategories_per_category):
                subcategory = Activity(
                    id=uuid4(),
                    name=self.fake.catch_phrase(),
                    parent_id=parent.id,
                    level=2
                )
                activities.append(subcategory)
        
        created_activities = await self.repository.create_activities(activities)
        print(f"Создано {len(created_activities)} видов деятельности")
        
        # Выводим первые 5 UUID видов деятельности
        print("📋 Примеры UUID видов деятельности:")
        for i, activity in enumerate(created_activities[:5]):
            print(f"   {i+1}. {activity.id}")
        
        return created_activities

    async def create_buildings(self, count: int = 2000):
        """Создает здания с адресами и геолокацией"""
        buildings = []
        
        # Координаты для Москвы (примерно)
        moscow_lat_range = (55.5, 55.9)
        moscow_lon_range = (37.3, 37.9)
        
        for _ in range(count):
            # Генерируем случайные координаты в пределах Москвы
            latitude = random.uniform(*moscow_lat_range)
            longitude = random.uniform(*moscow_lon_range)
            
            # Создаем геометрию точки
            location = WKTElement(f'POINT({longitude} {latitude})', srid=4326)
            
            building = Building(
                id=uuid4(),
                address=self.fake.address(),
                location=location
            )
            buildings.append(building)
        
        created_buildings = await self.repository.create_buildings(buildings)
        print(f"Создано {len(created_buildings)} зданий")
        
        # Выводим первые 5 UUID зданий
        print("🏢 Примеры UUID зданий:")
        for i, building in enumerate(created_buildings[:5]):
            print(f"   {i+1}. {building.id}")
        
        return created_buildings

    async def create_organizations(self, buildings: list, activities: list, count: int = 10000):
        """Создает организации с телефонами и связями с видами деятельности"""
        organizations = []
        organization_phones = []
        org_activity_relations = []
        
        # Получаем все активности из БД
        all_activities = await self.repository.get_all_activities()
        
        for i in range(count):
            # Выбираем случайное здание
            building = random.choice(buildings)
            
            # Создаем организацию
            organization = Organization(
                id=uuid4(),
                name=self.fake.company(),
                building_id=building.id
            )
            organizations.append(organization)
            
            # Добавляем 1-3 телефона для каждой организации
            phone_count = random.randint(1, 3)
            for _ in range(phone_count):
                phone = OrganizationPhone(
                    id=uuid4(),
                    organization_id=organization.id,
                    phone=self.fake.phone_number()
                )
                organization_phones.append(phone)
            
            # Связываем организацию с 1-5 видами деятельности
            activity_count = random.randint(1, 5)
            selected_activities = random.sample(all_activities, activity_count)
            
            for activity in selected_activities:
                relation = {
                    'organization_id': organization.id,
                    'activity_id': activity.id
                }
                org_activity_relations.append(relation)
        
        # Создаем все данные через репозиторий
        created_organizations = await self.repository.create_organizations(organizations)
        await self.repository.create_organization_phones(organization_phones)
        await self.repository.create_organization_activity_relations(org_activity_relations)
        
        print(f"Создано {len(created_organizations)} организаций с телефонами и связями")
        
        # Выводим первые 5 UUID организаций
        print("🏢 Примеры UUID организаций:")
        for i, organization in enumerate(created_organizations[:5]):
            print(f"   {i+1}. {organization.id}")
        
        return created_organizations

    async def clear_database(self):
        """Очищает базу данных от существующих данных"""
        await self.repository.clear_all_tables()
        print("База данных очищена")

    async def fill_database(self, organizations_count: int = 10000):
        """Основной метод для заполнения базы данных"""
        try:
            # Очищаем базу данных
            await self.clear_database()
            
            # Создаем данные
            print("Создание видов деятельности...")
            activities = await self.create_activities(50)
            
            print("Создание зданий...")
            buildings = await self.create_buildings(2000)
            
            print("Создание организаций...")
            organizations = await self.create_organizations(buildings, activities, organizations_count)
            
            print(f"\n✅ Заполнение базы данных завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка при заполнении базы данных: {e}")
            raise