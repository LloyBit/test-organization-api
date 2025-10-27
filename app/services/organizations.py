from app.database.repositories.organisations import OrganizationsRepository
from app.schemas import OrganizationResponse
from uuid import UUID
from geoalchemy2.elements import WKBElement

class OrganizationsService: 
    def __init__(self, repository: OrganizationsRepository):
        self.repository = repository
    
    async def get_organizations_by_building(self, building_id: UUID):
        """Получить организации по зданию"""
        organizations = await self.repository.organizations_by_building(building_id)
        return self._convert_organizations_to_response(organizations)
        
    async def get_organizations_by_activity(self, activity_id: UUID):
        """Получить организации по активности"""
        organizations = await self.repository.organizations_by_activity(activity_id)
        return self._convert_organizations_to_response(organizations)
        
    async def get_organizations_in_circle(self, latitude: float, longitude: float, radius: float):
        """Получить организации в радиусе от указанной точки"""
        organizations = await self.repository.organizations_in_circle(latitude, longitude, radius)
        return self._convert_organizations_to_response(organizations)
        
    async def get_organizations_in_rectangle(self, center_latitude: float, center_longitude: float, width: float, height: float):
        """Получить организации в прямоугольной области от указанной точки"""
        organizations = await self.repository.organizations_in_rectangle(center_latitude, center_longitude, width, height)
        return self._convert_organizations_to_response(organizations)
        
    async def get_organization_by_id(self, organization_id: UUID):
        """Получить организацию по ID"""
        organization = await self.repository.organization_by_id(organization_id)
        if organization:
            return self._convert_organizations_to_response([organization])[0]
        return None
        
    async def get_organizations_by_activity_type(self, activity_id: UUID):
        """Получить организации по типу активности"""
        organizations = await self.repository.organizations_by_activity_type(activity_id)
        return self._convert_organizations_to_response(organizations)
        
    async def get_organization_by_name(self, name: str):
        """Получить организацию по имени"""
        organization = await self.repository.organization_by_name(name)
        if organization:
            return self._convert_organizations_to_response([organization])[0]
        return None
    
    def _convert_organizations_to_response(self, organizations):
        """Преобразуем SQLAlchemy объекты в Pydantic модели"""
        result = []
        for org in organizations:
            org_data = {
                'id': org.id,
                'name': org.name,
                'building_id': org.building_id,
                'phones': [{'id': phone.id, 'phone': phone.phone} for phone in org.phones],
                'activities': [{'id': activity.id, 'name': activity.name, 'parent_id': activity.parent_id, 'level': activity.level} for activity in org.activities],
                'building': None
            }
            
            if org.building:
                building_data = {
                    'id': org.building.id,
                    'address': org.building.address,
                    'location': None
                }
                
                # Обрабатываем WKBElement
                if isinstance(org.building.location, WKBElement):
                    try:
                        # Используем правильный метод для извлечения координат
                        # WKBElement содержит бинарные данные, нужно их правильно обработать
                        wkb_data = org.building.location.data
                        
                        # Преобразуем WKB в координаты используя PostGIS функции
                        # Или используем встроенные методы geoalchemy2
                        if hasattr(org.building.location, 'desc'):
                            # Попробуем получить WKT из WKB
                            wkt = str(org.building.location.desc)
                            
                            # Если это все еще бинарные данные, попробуем другой подход
                            if wkt.startswith('0101000020'):
                                # Это WKB в hex формате, нужно декодировать
                                import struct
                                # Убираем префикс и декодируем hex
                                hex_data = wkt[18:]  # Убираем '0101000020e6100000'
                                # Декодируем координаты (little-endian double)
                                lon_bytes = bytes.fromhex(hex_data[:16])
                                lat_bytes = bytes.fromhex(hex_data[16:32])
                                longitude = struct.unpack('<d', lon_bytes)[0]
                                latitude = struct.unpack('<d', lat_bytes)[0]
                                
                                building_data['location'] = {
                                    'latitude': latitude,
                                    'longitude': longitude
                                }
                            elif wkt.startswith('POINT('):
                                # Это уже WKT строка
                                coords = wkt[6:-1].split()
                                longitude, latitude = float(coords[0]), float(coords[1])
                                building_data['location'] = {
                                    'latitude': latitude,
                                    'longitude': longitude
                                }
                    except (ValueError, IndexError, AttributeError, struct.error) as e:
                        building_data['location'] = None
                
                org_data['building'] = building_data
            
            result.append(OrganizationResponse(**org_data))
        
        return result