from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.organizations import OrganizationsService
from app.schemas import OrganizationResponse
from fastapi import Request
from uuid import UUID
from typing import List

router = APIRouter(prefix="/organizations")

def get_service(request: Request) -> OrganizationsService:
    return request.app.state.service

@router.get("/by-building/{building_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_building(
    building_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по зданию"""
    return await service.get_organizations_by_building(building_id)

@router.get("/by-activity/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity(
    activity_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по активности"""
    return await service.get_organizations_by_activity(activity_id)

@router.get("/in-circle", response_model=List[OrganizationResponse])
async def get_organizations_in_circle(
    latitude: float = Query(..., description="Широта"),
    longitude: float = Query(..., description="Долгота"),
    radius: float = Query(..., description="Радиус поиска в метрах"),
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации в радиусе от указанной точки"""
    return await service.get_organizations_in_circle(latitude, longitude, radius)

@router.get("/in-rectangle", response_model=List[OrganizationResponse])
async def get_organizations_in_rectangle(
    center_latitude: float = Query(..., description="Широта центра, например: 55.7558"),
    center_longitude: float = Query(..., description="Долгота центра, например: 37.6176"),
    width: float = Query(..., description="Ширина в метрах"),
    height: float = Query(..., description="Высота в метрах"),
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации в прямоугольной области от указанной точки"""
    return await service.get_organizations_in_rectangle(center_latitude, center_longitude, width, height)

@router.get("/by-id/{organization_id}", response_model=OrganizationResponse)
async def get_organization_by_id(
    organization_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организацию по ID"""
    organization = await service.get_organization_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.get("/by-activity-type/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity_type(
    activity_id: UUID,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организации по типу активности"""
    return await service.get_organizations_by_activity_type(activity_id)

@router.get("/by-name/{name}", response_model=OrganizationResponse)
async def get_organization_by_name(
    name: str,
    service: OrganizationsService = Depends(get_service)
):
    """Получить организацию по имени"""
    organization = await service.get_organization_by_name(name)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

