from fastapi import APIRouter, Depends, HTTPException, Query
from app.service import OrganizationsService
from fastapi import Request
from uuid import UUID
from typing import List, Optional

router = APIRouter(prefix="/organizations")

def get_service(request: Request) -> OrganizationsService:
    return request.app.state.service



@router.get("/by-building/{building_id}")
async def get_organizations_by_building(
    building_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по зданию"""
    return await service.get_organizations_by_building(building_id)

@router.get("/by-activity/{activity_id}")
async def get_organizations_by_activity(
    activity_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по активности"""
    return await service.get_organizations_by_activity(activity_id)

@router.get("/in-area")
async def get_organizations_in_area(
    latitude: float = Query(..., description="Широта"),
    longitude: float = Query(..., description="Долгота"),
    radius: float = Query(..., description="Радиус поиска в метрах"),
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации в радиусе от указанной точки"""
    return await service.get_organizations_in_area(latitude, longitude, radius)

@router.get("/by-id/{organization_id}")
async def get_organization_by_id(
    organization_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организацию по ID"""
    organization = await service.get_organization_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.get("/by-activity-type/{activity_id}")
async def get_organizations_by_activity_type(
    activity_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по типу активности"""
    return await service.get_organizations_by_activity_type(activity_id)

@router.get("/by-name/{name}")
async def get_organization_by_name(
    name: str,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организацию по имени"""
    organization = await service.get_organization_by_name(name)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

