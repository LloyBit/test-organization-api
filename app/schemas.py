from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class LocationResponse(BaseModel):
    """Схема для геолокации"""
    latitude: float = Field(description="Широта")
    longitude: float = Field(description="Долгота")

class BuildingResponse(BaseModel):
    """Схема для здания"""
    id: UUID
    address: str
    location: Optional[LocationResponse] = None

    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    """Схема для вида деятельности"""
    id: UUID
    name: str
    parent_id: Optional[UUID] = None
    level: int

class OrganizationPhoneResponse(BaseModel):
    """Схема для телефона организации"""
    id: UUID
    phone: str

class OrganizationResponse(BaseModel):
    """Схема для организации"""
    id: UUID
    name: str
    building_id: UUID
    building: Optional[BuildingResponse] = None
    phones: List[OrganizationPhoneResponse] = []
    activities: List[ActivityResponse] = []

    class Config:
        from_attributes = True
