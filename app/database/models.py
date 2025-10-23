"""ORM для Postgres"""
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Organization(Base):
    __tablename__ = "organizations"
    
class Building(Base):
    __tablename__ = "buildings"
    
class Activity(Base):
    __tablename__ = "activities"
    
