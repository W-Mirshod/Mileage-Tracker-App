import re
from typing import Optional
from datetime import datetime

def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:.2f}"

def format_mileage(mileage: float) -> str:
    """Format mileage with commas."""
    return f"{mileage:,.1f}"

def calculate_fuel_efficiency(miles: float, gallons: float) -> float:
    """Calculate MPG (miles per gallon)."""
    return miles / gallons if gallons > 0 else 0

def get_fuel_type_icon(fuel_type: str) -> str:
    """Get icon emoji for fuel type."""
    fuel_icons = {
        "gasoline": "⛽",
        "diesel": "🛢️",
        "electric": "⚡",
        "hybrid": "🔋"
    }
    return fuel_icons.get(fuel_type.lower(), "⛽")

def get_service_type_icon(service_type: str) -> str:
    """Get icon emoji for service type."""
    service_icons = {
        "oil_change": "🛢️",
        "tire_rotation": "🛞",
        "brake_service": "🛑",
        "transmission": "⚙️",
        "cooling_system": "❄️",
        "battery": "🔋",
        "inspection": "🔍",
        "other": "🔧"
    }
    return service_icons.get(service_type.lower(), "🔧")

def format_date(date: datetime) -> str:
    """Format date for display."""
    return date.strftime("%b %d, %Y")

def format_datetime(date: datetime) -> str:
    """Format datetime for display."""
    return date.strftime("%b %d, %Y %I:%M %p")

def validate_license_plate(plate: str) -> bool:
    """Basic validation for license plate format."""
    # Allow alphanumeric characters, spaces, and common separators
    return bool(re.match(r'^[A-Z0-9\s\-\.]+$', plate.upper()))

def validate_vin(vin: str) -> bool:
    """Basic VIN validation (17 characters, alphanumeric)."""
    return bool(re.match(r'^[A-Z0-9]{17}$', vin.upper()))

def get_vehicle_age_years(purchase_date: Optional[datetime]) -> Optional[float]:
    """Calculate vehicle age in years."""
    if not purchase_date:
        return None
    return (datetime.now() - purchase_date).days / 365.25

def get_mileage_per_year(current_mileage: float, purchase_date: Optional[datetime]) -> Optional[float]:
    """Calculate average mileage per year."""
    age_years = get_vehicle_age_years(purchase_date)
    if not age_years or age_years <= 0:
        return None
    return current_mileage / age_years

def categorize_service_type(service_type: str) -> str:
    """Categorize service types for better organization."""
    categories = {
        "maintenance": ["oil_change", "filter_change", "fluid_check"],
        "tires": ["tire_rotation", "tire_replacement", "tire_repair"],
        "brakes": ["brake_service", "brake_pad_replacement"],
        "engine": ["transmission", "cooling_system", "battery", "spark_plugs"],
        "inspection": ["inspection", "emissions_test"],
        "other": []
    }

    for category, types in categories.items():
        if service_type in types:
            return category

    return "other"

def get_service_interval(service_type: str) -> Optional[int]:
    """Get typical service interval in miles for different service types."""
    intervals = {
        "oil_change": 3000,
        "tire_rotation": 6000,
        "brake_service": 25000,
        "inspection": 12000,
        "transmission": 30000,
        "cooling_system": 24000,
        "battery": 40000
    }
    return intervals.get(service_type.lower())

def calculate_service_due(current_mileage: float, last_service_mileage: float, service_type: str) -> Optional[float]:
    """Calculate when next service is due."""
    interval = get_service_interval(service_type)
    if not interval:
        return None
    return last_service_mileage + interval

def get_trip_purpose_icon(purpose: str) -> str:
    """Get icon emoji for trip purpose."""
    purpose_icons = {
        "business": "💼",
        "personal": "🏠",
        "commute": "🚗",
        "vacation": "🏖️",
        "errand": "🛒",
        "other": "📍"
    }
    return purpose_icons.get(purpose.lower(), "📍")

def calculate_cost_per_mile(fillups) -> Optional[float]:
    """Calculate average cost per mile from fillup data."""
    if not fillups:
        return None

    total_cost = sum(f.total_cost for f in fillups)
    total_miles = sum(f.mileage for f in fillups[1:]) - sum(f.mileage for f in fillups[:-1]) if len(fillups) > 1 else 0

    return total_cost / total_miles if total_miles > 0 else None
