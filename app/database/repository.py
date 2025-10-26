from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import Organization, Building, organization_activities
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import List, Optional
import math

class OrganizationsRepository:
    def __init__(self, db_helper: AsyncDatabaseHelper):
        self.db_helper = db_helper

    async def organizations_by_building(self, building_id: UUID):
        """Получить организации по зданию"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.building_id == building_id))
            return result.scalars().all()
        
    async def organizations_by_activity(self, activity_id: UUID):
        """Получить организации по определенной активности"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(
                select(Organization)
                .join(organization_activities)
                .where(organization_activities.c.activity_id == activity_id)
            )
            return result.scalars().all()
        
    async def organizations_in_circle(self, latitude: float, longitude: float, radius: float):
        """Получить организации в радиусе от указанной точки"""
        async with self.db_helper.session_only() as session:
            center_point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            
            # Используем ST_DWithin с правильными единицами
            query = self._build_organizations_with_building_query().where(
                func.ST_DWithin(
                    func.ST_Transform(Building.location, 3857), 
                    func.ST_Transform(center_point, 3857),       
                    radius  # радиус в метрах
                )
            )
            
            result = await session.execute(query)
            return result.scalars().all()
        
    async def organizations_in_rectangle(self, center_latitude: float, center_longitude: float, width: float, height: float):
        """Получить организации в прямоугольной области от указанной точки"""
        async with self.db_helper.session_only() as session:
            # Создаем центр в Web Mercator проекции
            center_point = func.ST_Transform(
                func.ST_SetSRID(func.ST_MakePoint(center_longitude, center_latitude), 4326),
                3857
            )
            
            # Создаем прямоугольник в Web Mercator (единицы - метры)
            half_width = width / 2
            half_height = height / 2
            
            rectangle = func.ST_MakeEnvelope(
                func.ST_X(center_point) - half_width,
                func.ST_Y(center_point) - half_height,
                func.ST_X(center_point) + half_width,
                func.ST_Y(center_point) + half_height,
                3857
            )
            
            query = self._build_organizations_with_building_query().where(
                func.ST_Within(
                    func.ST_Transform(Building.location, 3857),
                    rectangle
                )
            )
            
            result = await session.execute(query)
            return result.scalars().all()
        
    async def organization_by_id(self, organization_id: UUID):
        """Получить организацию по ID"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.id == organization_id))
            return result.scalar_one_or_none()
        
    async def organisations_by_activity_type(self, activity_id: UUID):
        # TODO: Реализовать поиск по дереву деятельностей
        pass
        
    async def organisation_by_name(self, name: str):
        """Получить организацию по имени"""
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.name == name))
            return result.scalar_one_or_none()

    # Приватные методы     
    def _build_organizations_with_building_query(self):
        """Создать базовый запрос для организаций с загрузкой зданий"""
        return (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .options(joinedload(Organization.building))
        )
