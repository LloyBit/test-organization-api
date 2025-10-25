from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import Organization
from sqlalchemy import select
from uuid import UUID

class OrganizationsRepository:
    def __init__(self, db_helper: AsyncDatabaseHelper):
        self.db_helper = db_helper

    async def organizations_by_building(self, building_id: UUID):
        ...
        
    async def organizations_by_activity(self, activity_id: UUID):
        ...
        
    async def organizations_in_area(self, location: float, latitude: float, longitude: float, radius: float):
        ...
        
    async def organizations_by_id(self, organization_id: UUID):
        ...
        
    async def organisations_by_activity_type(self, activity_id: UUID):
        ...
        
    async def organisation_by_name(self, name: str):
        ...
        
    