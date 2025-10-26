"""ORM для Postgres"""
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, Table, UUID, Float
from sqlalchemy.orm import relationship, declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

# Связующая таблица для организации и деятельности (многие ко многим)
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", UUID, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", UUID, ForeignKey("activities.id"), primary_key=True)
)

# Связующая таблица для организации и телефонов (можно хранить несколько телефонов)
class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    id = Column(UUID, primary_key=True, default=uuid4)
    organization_id = Column(UUID, ForeignKey("organizations.id"), nullable=False)
    phone = Column(String, nullable=False)

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    building_id = Column(UUID, ForeignKey("buildings.id"), nullable=False)
    
    building = relationship("Building", back_populates="organizations")
    phones = relationship("OrganizationPhone", backref="organization", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary=organization_activities, back_populates="organizations")


class Building(Base):
    __tablename__ = "buildings"
    id = Column(UUID, primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326)) 
    
    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    parent_id = Column(UUID, ForeignKey("activities.id"), nullable=True)
    
    children = relationship("Activity", backref="parent", remote_side=[id])
    organizations = relationship("Organization", secondary=organization_activities, back_populates="activities")
