# app/database/repository.py
from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import Organization, Building, organization_activities
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from uuid import UUID
from typing import List, Optional

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
            center_point = self._create_point(latitude, longitude)
            query = self._build_organizations_with_building_query().where(
                func.ST_DWithin(Building.location, center_point, radius)
            )
            
            result = await session.execute(query)
            return result.scalars().all()
        
    async def organizations_in_rectangle(self, center_latitude: float, center_longitude: float, width: float, height: float):
        """Получить организации в прямоугольной области от указанной точки"""
        async with self.db_helper.session_only() as session:
            rectangle = self._create_rectangle(center_latitude, center_longitude, width, height)
            query = self._build_organizations_with_building_query().where(
                func.ST_Within(Building.location, rectangle)
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
    def _create_point(self, latitude: float, longitude: float):
        """Создать точку с SRID 4326"""
        return func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
    
    def _create_rectangle(self, center_latitude: float, center_longitude: float, width: float, height: float):
        """Создать прямоугольник по центру и размерам в метрах"""
        # Преобразуем метры в градусы
        lat_degrees = height / 111320.0
        lon_degrees = width / (111320.0 * func.cos(func.radians(center_latitude)))
        
        # Вычисляем границы прямоугольника
        min_lat = center_latitude - lat_degrees / 2
        max_lat = center_latitude + lat_degrees / 2
        min_lon = center_longitude - lon_degrees / 2
        max_lon = center_longitude + lon_degrees / 2
        
        return func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
    
    def _build_organizations_with_building_query(self):
        """Создать базовый запрос для организаций с загрузкой зданий"""
        return (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .options(joinedload(Organization.building))
        )
    
    def _meters_to_degrees(self, meters: float, latitude: float = None):
        """Преобразовать метры в градусы"""
        lat_degrees = meters / 111320.0
        if latitude is not None:
            lon_degrees = meters / (111320.0 * func.cos(func.radians(latitude)))
            return lat_degrees, lon_degrees
        return lat_degrees