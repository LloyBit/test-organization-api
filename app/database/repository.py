from app.database.db_helper import AsyncDatabaseHelper
from app.database.models import Organization, organization_activities
from sqlalchemy import select
from uuid import UUID

class OrganizationsRepository:
    def __init__(self, db_helper: AsyncDatabaseHelper):
        self.db_helper = db_helper

    async def organizations_by_building(self, building_id: UUID):
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.building_id == building_id))
            return result.scalars().all()
        
    async def organizations_by_activity(self, activity_id: UUID):
        async with self.db_helper.session_only() as session:
            result = await session.execute(
                select(Organization)
                .join(organization_activities)
                .where(organization_activities.c.activity_id == activity_id)
            )
            return result.scalars().all()
        
    async def organizations_in_area(self, location: float, latitude: float, longitude: float, radius: float):
        ...
        
    async def organization_by_id(self, organization_id: UUID):
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.id == organization_id))
            return result.scalar_one_or_none()
        
    async def organisations_by_activity_type(self, activity_id: UUID):
        ...
        
    async def organisation_by_name(self, name: str):
        async with self.db_helper.session_only() as session:
            result = await session.execute(select(Organization).where(Organization.name == name))
            return result.scalar_one_or_none()
        
    