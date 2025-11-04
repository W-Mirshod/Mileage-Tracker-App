from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VehicleBase(BaseModel):
    name: str
    make: str
    model: str
    year: int
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    fuel_type: str = "gasoline"
    tank_capacity_gallons: Optional[float] = None
    current_mileage: float = 0.0
    is_active: bool = True
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    notes: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class VehicleList(BaseModel):
    vehicles: List[Vehicle]
    total: int

class FillupBase(BaseModel):
    vehicle_id: int
    date: Optional[datetime] = None
    mileage: float
    gallons: float
    price_per_gallon: float
    total_cost: float
    fuel_brand: Optional[str] = None
    location: Optional[str] = None
    is_full_tank: bool = True
    notes: Optional[str] = None

class FillupCreate(FillupBase):
    pass

class Fillup(FillupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FillupList(BaseModel):
    fillups: List[Fillup]
    total: int

class MaintenanceRecordBase(BaseModel):
    vehicle_id: int
    date: Optional[datetime] = None
    mileage: float
    service_type: str
    description: str
    cost: Optional[float] = None
    provider: Optional[str] = None
    next_service_mileage: Optional[float] = None
    next_service_date: Optional[datetime] = None
    notes: Optional[str] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MaintenanceRecordList(BaseModel):
    records: List[MaintenanceRecord]
    total: int

class TripBase(BaseModel):
    vehicle_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_mileage: float
    end_mileage: Optional[float] = None
    distance: Optional[float] = None
    purpose: Optional[str] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    notes: Optional[str] = None

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TripList(BaseModel):
    trips: List[Trip]
    total: int

class TripComplete(BaseModel):
    end_mileage: float
    end_location: Optional[str] = None

class VehicleStats(BaseModel):
    vehicle_id: int
    vehicle_name: str
    total_mileage: float
    total_fillups: int
    total_fuel_cost: float
    average_mpg: Optional[float]
    last_fillup_mileage: Optional[float]
    last_service_mileage: Optional[float]
    next_service_due: Optional[float]

class DashboardStats(BaseModel):
    total_vehicles: int
    total_mileage: float
    total_fuel_cost: float
    average_mpg: Optional[float]
    recent_fillups: int
    upcoming_services: int
