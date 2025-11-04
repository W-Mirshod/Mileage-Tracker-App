from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, crud

app = FastAPI(title="Mileage Tracker")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(database.get_db)):
    """Get dashboard statistics."""
    return crud.get_dashboard_stats(db)

# Vehicle endpoints
@app.post("/api/vehicles", response_model=schemas.Vehicle)
async def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(database.get_db)):
    """Create a new vehicle."""
    db_vehicle = crud.get_vehicle_by_name(db, vehicle.name)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle with this name already exists")

    return crud.create_vehicle(db, vehicle)

@app.get("/api/vehicles", response_model=schemas.VehicleList)
async def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all vehicles."""
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return {"vehicles": vehicles, "total": len(vehicles)}

@app.get("/api/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
async def get_vehicle(vehicle_id: int, db: Session = Depends(database.get_db)):
    """Get a specific vehicle."""
    vehicle = crud.get_vehicle_by_id(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.get("/api/vehicles/{vehicle_id}/stats")
async def get_vehicle_statistics(vehicle_id: int, db: Session = Depends(database.get_db)):
    """Get statistics for a specific vehicle."""
    stats = crud.get_vehicle_stats(db, vehicle_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return stats

@app.put("/api/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(vehicle_id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(database.get_db)):
    """Update a vehicle."""
    db_vehicle = crud.update_vehicle(db, vehicle_id, vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@app.delete("/api/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Session = Depends(database.get_db)):
    """Delete a vehicle."""
    db_vehicle = crud.delete_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted successfully"}

# Fillup endpoints
@app.post("/api/fillups", response_model=schemas.Fillup)
async def create_fillup(fillup: schemas.FillupCreate, db: Session = Depends(database.get_db)):
    """Create a new fillup record."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, fillup.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Validate mileage is not less than current vehicle mileage (unless it's the first fillup)
    if vehicle.current_mileage > 0 and fillup.mileage < vehicle.current_mileage:
        raise HTTPException(status_code=400, detail="Mileage cannot be less than current vehicle mileage")

    return crud.create_fillup(db, fillup)

@app.get("/api/fillups", response_model=schemas.FillupList)
async def get_all_fillups(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all fillup records."""
    fillups = crud.get_all_fillups(db, skip=skip, limit=limit)
    return {"fillups": fillups, "total": len(fillups)}

@app.get("/api/vehicles/{vehicle_id}/fillups", response_model=schemas.FillupList)
async def get_vehicle_fillups(vehicle_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get fillup records for a specific vehicle."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    fillups = crud.get_fillups_by_vehicle(db, vehicle_id, skip=skip, limit=limit)
    return {"fillups": fillups, "total": len(fillups)}

@app.put("/api/fillups/{fillup_id}", response_model=schemas.Fillup)
async def update_fillup(fillup_id: int, fillup: schemas.FillupCreate, db: Session = Depends(database.get_db)):
    """Update a fillup record."""
    db_fillup = crud.update_fillup(db, fillup_id, fillup)
    if db_fillup is None:
        raise HTTPException(status_code=404, detail="Fillup record not found")
    return db_fillup

@app.delete("/api/fillups/{fillup_id}")
async def delete_fillup(fillup_id: int, db: Session = Depends(database.get_db)):
    """Delete a fillup record."""
    db_fillup = crud.delete_fillup(db, fillup_id)
    if db_fillup is None:
        raise HTTPException(status_code=404, detail="Fillup record not found")
    return {"message": "Fillup record deleted successfully"}

# Maintenance endpoints
@app.post("/api/maintenance", response_model=schemas.MaintenanceRecord)
async def create_maintenance_record(record: schemas.MaintenanceRecordCreate, db: Session = Depends(database.get_db)):
    """Create a new maintenance record."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, record.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return crud.create_maintenance_record(db, record)

@app.get("/api/maintenance", response_model=schemas.MaintenanceRecordList)
async def get_all_maintenance_records(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all maintenance records."""
    records = crud.get_all_maintenance_records(db, skip=skip, limit=limit)
    return {"records": records, "total": len(records)}

@app.get("/api/vehicles/{vehicle_id}/maintenance", response_model=schemas.MaintenanceRecordList)
async def get_vehicle_maintenance_records(vehicle_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get maintenance records for a specific vehicle."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    records = crud.get_maintenance_records_by_vehicle(db, vehicle_id, skip=skip, limit=limit)
    return {"records": records, "total": len(records)}

@app.put("/api/maintenance/{record_id}", response_model=schemas.MaintenanceRecord)
async def update_maintenance_record(record_id: int, record: schemas.MaintenanceRecordCreate, db: Session = Depends(database.get_db)):
    """Update a maintenance record."""
    db_record = crud.update_maintenance_record(db, record_id, record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return db_record

@app.delete("/api/maintenance/{record_id}")
async def delete_maintenance_record(record_id: int, db: Session = Depends(database.get_db)):
    """Delete a maintenance record."""
    db_record = crud.delete_maintenance_record(db, record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return {"message": "Maintenance record deleted successfully"}

# Trip endpoints
@app.post("/api/trips", response_model=schemas.Trip)
async def create_trip(trip: schemas.TripCreate, db: Session = Depends(database.get_db)):
    """Start a new trip."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, trip.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return crud.create_trip(db, trip)

@app.get("/api/trips", response_model=schemas.TripList)
async def get_all_trips(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get all trips."""
    trips = crud.get_all_trips(db, skip=skip, limit=limit)
    return {"trips": trips, "total": len(trips)}

@app.get("/api/trips/{trip_id}", response_model=schemas.Trip)
async def get_trip(trip_id: int, db: Session = Depends(database.get_db)):
    """Get a specific trip."""
    trip = crud.get_trip_by_id(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.get("/api/vehicles/{vehicle_id}/trips", response_model=schemas.TripList)
async def get_vehicle_trips(vehicle_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get trips for a specific vehicle."""
    # Verify vehicle exists
    vehicle = crud.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    trips = crud.get_trips_by_vehicle(db, vehicle_id, skip=skip, limit=limit)
    return {"trips": trips, "total": len(trips)}

@app.post("/api/trips/{trip_id}/complete")
async def complete_trip(trip_id: int, trip_data: schemas.TripComplete, db: Session = Depends(database.get_db)):
    """Complete a trip."""
    trip = crud.complete_trip(db, trip_id, trip_data.end_mileage, trip_data.end_location)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"message": "Trip completed successfully"}

@app.put("/api/trips/{trip_id}", response_model=schemas.Trip)
async def update_trip(trip_id: int, trip_update: dict, db: Session = Depends(database.get_db)):
    """Update a trip."""
    db_trip = crud.update_trip(db, trip_id, trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@app.delete("/api/trips/{trip_id}")
async def delete_trip(trip_id: int, db: Session = Depends(database.get_db)):
    """Delete a trip."""
    db_trip = crud.delete_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip deleted successfully"}
