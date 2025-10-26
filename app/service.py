from app.database.repository import OrganizationsRepository
from uuid import UUID
from typing import List, Optional

class OrganizationsService: 
    def __init__(self, repository: OrganizationsRepository):
        self.repository = repository
    
    async def get_organizations_by_building(self, building_id: UUID):
        """Получить организации по зданию"""
        return await self.repository.organizations_by_building(building_id)
        
    async def get_organizations_by_activity(self, activity_id: UUID):
        """Получить организации по активности"""
        return await self.repository.organizations_by_activity(activity_id)
        
    async def get_organizations_in_circle(self, latitude: float, longitude: float, radius: float):
        """Получить организации в радиусе от указанной точки"""
        return await self.repository.organizations_in_circle(latitude, longitude, radius)
        
    async def get_organizations_in_rectangle(self, center_latitude: float, center_longitude: float, width: float, height: float):
        """Получить организации в прямоугольной области от указанной точки"""
        return await self.repository.organizations_in_rectangle(center_latitude, center_longitude, width, height)
        
    async def get_organization_by_id(self, organization_id: UUID):
        """Получить организацию по ID"""
        return await self.repository.organization_by_id(organization_id)
        
    async def get_organizations_by_activity_type(self, activity_id: UUID):
        """Получить организации по типу активности"""
        return await self.repository.organisations_by_activity_type(activity_id)
        
    async def get_organization_by_name(self, name: str):
        """Получить организацию по имени"""
        return await self.repository.organisation_by_name(name)