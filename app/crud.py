from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from . import models, schemas
from typing import List
from datetime import datetime, timedelta

# Vehicle CRUD
def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicle_by_id(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicle_by_name(db: Session, vehicle_name: str):
    return db.query(models.Vehicle).filter(models.Vehicle.name == vehicle_name).first()

def get_vehicle_with_details(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).options(
        joinedload(models.Vehicle.fillups),
        joinedload(models.Vehicle.maintenance_records),
        joinedload(models.Vehicle.trips)
    ).filter(models.Vehicle.id == vehicle_id).first()

def update_vehicle(db: Session, vehicle_id: int, vehicle_update: schemas.VehicleCreate):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        for key, value in vehicle_update.dict().items():
            setattr(db_vehicle, key, value)
        db.commit()
        db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return db_vehicle

# Fillup CRUD
def create_fillup(db: Session, fillup: schemas.FillupCreate):
    db_fillup = models.Fillup(**fillup.dict())
    db.add(db_fillup)
    db.commit()
    db.refresh(db_fillup)

    # Update vehicle current mileage if this fillup has higher mileage
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == fillup.vehicle_id).first()
    if vehicle and fillup.mileage > vehicle.current_mileage:
        vehicle.current_mileage = fillup.mileage
        db.commit()

    return db_fillup

def get_fillups_by_vehicle(db: Session, vehicle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Fillup).filter(models.Fillup.vehicle_id == vehicle_id).order_by(desc(models.Fillup.date)).offset(skip).limit(limit).all()

def get_all_fillups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Fillup).options(joinedload(models.Fillup.vehicle)).order_by(desc(models.Fillup.date)).offset(skip).limit(limit).all()

def update_fillup(db: Session, fillup_id: int, fillup_update: schemas.FillupCreate):
    db_fillup = db.query(models.Fillup).filter(models.Fillup.id == fillup_id).first()
    if db_fillup:
        for key, value in fillup_update.dict().items():
            setattr(db_fillup, key, value)
        db.commit()
        db.refresh(db_fillup)
    return db_fillup

def delete_fillup(db: Session, fillup_id: int):
    db_fillup = db.query(models.Fillup).filter(models.Fillup.id == fillup_id).first()
    if db_fillup:
        db.delete(db_fillup)
        db.commit()
    return db_fillup

# Maintenance Record CRUD
def create_maintenance_record(db: Session, record: schemas.MaintenanceRecordCreate):
    db_record = models.MaintenanceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_maintenance_records_by_vehicle(db: Session, vehicle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.vehicle_id == vehicle_id).order_by(desc(models.MaintenanceRecord.date)).offset(skip).limit(limit).all()

def get_all_maintenance_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MaintenanceRecord).options(joinedload(models.MaintenanceRecord.vehicle)).order_by(desc(models.MaintenanceRecord.date)).offset(skip).limit(limit).all()

def update_maintenance_record(db: Session, record_id: int, record_update: schemas.MaintenanceRecordCreate):
    db_record = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.id == record_id).first()
    if db_record:
        for key, value in record_update.dict().items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_maintenance_record(db: Session, record_id: int):
    db_record = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

# Trip CRUD
def create_trip(db: Session, trip: schemas.TripCreate):
    db_trip = models.Trip(**trip.dict())
    if trip.end_mileage and trip.start_mileage:
        db_trip.distance = trip.end_mileage - trip.start_mileage
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    # Eagerly load vehicle relationship
    db_trip = db.query(models.Trip).options(joinedload(models.Trip.vehicle)).filter(models.Trip.id == db_trip.id).first()
    return db_trip

def get_trip_by_id(db: Session, trip_id: int):
    return db.query(models.Trip).options(joinedload(models.Trip.vehicle)).filter(models.Trip.id == trip_id).first()

def get_trips_by_vehicle(db: Session, vehicle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).filter(models.Trip.vehicle_id == vehicle_id).order_by(desc(models.Trip.start_date)).offset(skip).limit(limit).all()

def get_all_trips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).options(joinedload(models.Trip.vehicle)).order_by(desc(models.Trip.start_date)).offset(skip).limit(limit).all()

def update_trip(db: Session, trip_id: int, trip_update: dict):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip:
        for key, value in trip_update.items():
            setattr(db_trip, key, value)
        # Recalculate distance if mileage changed
        if 'end_mileage' in trip_update or 'start_mileage' in trip_update:
            start = trip_update.get('start_mileage', db_trip.start_mileage)
            end = trip_update.get('end_mileage', db_trip.end_mileage)
            if start and end:
                db_trip.distance = end - start
        db.commit()
        db.refresh(db_trip)
    return db_trip

def complete_trip(db: Session, trip_id: int, end_mileage: float, end_location: str = None):
    update_data = {
        "end_mileage": end_mileage,
        "end_date": datetime.now(),
        "distance": end_mileage - db.query(models.Trip).filter(models.Trip.id == trip_id).first().start_mileage
    }
    if end_location:
        update_data["end_location"] = end_location
    return update_trip(db, trip_id, update_data)

def delete_trip(db: Session, trip_id: int):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip:
        db.delete(db_trip)
        db.commit()
    return db_trip

# Statistics and calculations
def calculate_mpg(fillups: List[models.Fillup]) -> float:
    """Calculate average MPG from fillup data."""
    if len(fillups) < 2:
        return None

    # Sort fillups by mileage
    sorted_fillups = sorted(fillups, key=lambda x: x.mileage)
    total_miles = 0
    total_gallons = 0

    for i in range(1, len(sorted_fillups)):
        if sorted_fillups[i].is_full_tank and sorted_fillups[i-1].is_full_tank:
            miles = sorted_fillups[i].mileage - sorted_fillups[i-1].mileage
            gallons = sorted_fillups[i-1].gallons
            if miles > 0 and gallons > 0:
                total_miles += miles
                total_gallons += gallons

    return total_miles / total_gallons if total_gallons > 0 else None

def get_vehicle_stats(db: Session, vehicle_id: int) -> schemas.VehicleStats:
    """Get comprehensive statistics for a vehicle."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        return None

    fillups = db.query(models.Fillup).filter(models.Fillup.vehicle_id == vehicle_id).order_by(models.Fillup.mileage).all()
    maintenance = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.vehicle_id == vehicle_id).order_by(desc(models.MaintenanceRecord.mileage)).first()

    total_fillups = len(fillups)
    total_fuel_cost = sum(f.total_cost for f in fillups)
    average_mpg = calculate_mpg(fillups) if len(fillups) >= 2 else None

    last_fillup = fillups[-1] if fillups else None
    last_fillup_mileage = last_fillup.mileage if last_fillup else None

    last_service_mileage = maintenance.mileage if maintenance else None

    # Find upcoming service
    upcoming_service = db.query(models.MaintenanceRecord).filter(
        models.MaintenanceRecord.vehicle_id == vehicle_id,
        models.MaintenanceRecord.next_service_mileage.isnot(None),
        models.MaintenanceRecord.next_service_mileage > (last_fillup_mileage or vehicle.current_mileage)
    ).order_by(models.MaintenanceRecord.next_service_mileage).first()

    next_service_due = upcoming_service.next_service_mileage if upcoming_service else None

    return schemas.VehicleStats(
        vehicle_id=vehicle_id,
        vehicle_name=vehicle.name,
        total_mileage=vehicle.current_mileage,
        total_fillups=total_fillups,
        total_fuel_cost=round(total_fuel_cost, 2),
        average_mpg=round(average_mpg, 1) if average_mpg else None,
        last_fillup_mileage=last_fillup_mileage,
        last_service_mileage=last_service_mileage,
        next_service_due=next_service_due
    )

def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    """Get overall dashboard statistics."""
    vehicles = db.query(models.Vehicle).filter(models.Vehicle.is_active == True).all()
    total_vehicles = len(vehicles)

    total_mileage = sum(v.current_mileage for v in vehicles)

    # Recent fillups (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_fillups = db.query(func.count(models.Fillup.id)).filter(models.Fillup.date >= thirty_days_ago).scalar()

    # All fillups for fuel cost calculation
    all_fillups = db.query(models.Fillup).all()
    total_fuel_cost = sum(f.total_cost for f in all_fillups)

    # Calculate average MPG across all vehicles
    vehicle_mpgs = []
    for vehicle in vehicles:
        fillups = db.query(models.Fillup).filter(models.Fillup.vehicle_id == vehicle.id).all()
        mpg = calculate_mpg(fillups)
        if mpg:
            vehicle_mpgs.append(mpg)

    average_mpg = sum(vehicle_mpgs) / len(vehicle_mpgs) if vehicle_mpgs else None

    # Upcoming services (next service due within 1000 miles of current mileage)
    upcoming_services = 0
    for vehicle in vehicles:
        upcoming = db.query(models.MaintenanceRecord).filter(
            models.MaintenanceRecord.vehicle_id == vehicle.id,
            models.MaintenanceRecord.next_service_mileage.isnot(None),
            models.MaintenanceRecord.next_service_mileage <= vehicle.current_mileage + 1000
        ).first()
        if upcoming:
            upcoming_services += 1

    return schemas.DashboardStats(
        total_vehicles=total_vehicles,
        total_mileage=round(total_mileage, 1),
        total_fuel_cost=round(total_fuel_cost, 2),
        average_mpg=round(average_mpg, 1) if average_mpg else None,
        recent_fillups=recent_fillups,
        upcoming_services=upcoming_services
    )
