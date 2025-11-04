from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    license_plate = Column(String, nullable=True)
    vin = Column(String, nullable=True)
    fuel_type = Column(String, default="gasoline")  # gasoline, diesel, electric, hybrid
    tank_capacity_gallons = Column(Float, nullable=True)
    current_mileage = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    purchase_date = Column(DateTime, nullable=True)
    purchase_price = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    fillups = relationship("Fillup", back_populates="vehicle", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="vehicle", cascade="all, delete-orphan")

class Fillup(Base):
    __tablename__ = "fillups"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    date = Column(DateTime, default=func.now())
    mileage = Column(Float)
    gallons = Column(Float)
    price_per_gallon = Column(Float)
    total_cost = Column(Float)
    fuel_brand = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_full_tank = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="fillups")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    date = Column(DateTime, default=func.now())
    mileage = Column(Float)
    service_type = Column(String)  # oil_change, tire_rotation, brake_service, etc.
    description = Column(Text)
    cost = Column(Float, nullable=True)
    provider = Column(String, nullable=True)
    next_service_mileage = Column(Float, nullable=True)
    next_service_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_records")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    start_mileage = Column(Float)
    end_mileage = Column(Float, nullable=True)
    distance = Column(Float, nullable=True)
    purpose = Column(String, nullable=True)  # business, personal, commute, etc.
    start_location = Column(String, nullable=True)
    end_location = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="trips")
