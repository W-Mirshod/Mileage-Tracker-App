# 🚗 Mileage Tracker

A comprehensive web application for tracking vehicle mileage, fuel consumption, maintenance records, and trip logging.

## Features

- **Vehicle Management**: Add and manage multiple vehicles with detailed information
- **Fuel Tracking**: Record fill-ups with price, location, and MPG calculations
- **Maintenance Records**: Track service history, costs, and schedule future maintenance
- **Trip Logging**: Log trips with start/end mileage and automatic distance calculation
- **Statistics Dashboard**: View fuel efficiency, costs, and maintenance schedules
- **Real-time Updates**: Live dashboard with key metrics

## Tech Stack

- **Backend**: FastAPI with SQLAlchemy
- **Frontend**: Vanilla JavaScript with modern CSS
- **Database**: SQLite
- **Deployment**: Docker & Docker Compose

## Quick Start

1. **Navigate to the app**:
   ```bash
   cd "Mileage Tracker App"
   ```

2. **Start the application**:
   ```bash
   docker compose up -d
   ```

3. **Open your browser**:
   Navigate to `http://localhost:8003`

## Usage

### Managing Vehicles
- Click "Add Vehicle" to create a new vehicle profile
- Enter make, model, year, fuel type, and other details
- View vehicle statistics and maintenance history

### Tracking Fuel
- Select "Fill-ups" tab and click "Add Fill-up"
- Enter mileage, gallons, price per gallon, and location
- View MPG calculations and fuel cost trends

### Maintenance Records
- Go to "Maintenance" tab and add service records
- Track costs, providers, and schedule future services
- View upcoming maintenance alerts

### Trip Logging
- Use "Trips" tab to start and complete trips
- Record purpose, locations, and mileage
- Automatic distance calculations

## API Endpoints

### Vehicles
- `POST /api/vehicles` - Create a vehicle
- `GET /api/vehicles` - List all vehicles
- `GET /api/vehicles/{id}` - Get vehicle details
- `GET /api/vehicles/{id}/stats` - Get vehicle statistics
- `PUT /api/vehicles/{id}` - Update a vehicle
- `DELETE /api/vehicles/{id}` - Delete a vehicle

### Fill-ups
- `POST /api/fillups` - Create a fill-up record
- `GET /api/fillups` - List all fill-ups
- `GET /api/vehicles/{id}/fillups` - Get vehicle fill-ups
- `PUT /api/fillups/{id}` - Update a fill-up
- `DELETE /api/fillups/{id}` - Delete a fill-up

### Maintenance
- `POST /api/maintenance` - Create a maintenance record
- `GET /api/maintenance` - List all maintenance records
- `GET /api/vehicles/{id}/maintenance` - Get vehicle maintenance
- `PUT /api/maintenance/{id}` - Update a maintenance record
- `DELETE /api/maintenance/{id}` - Delete a maintenance record

### Trips
- `POST /api/trips` - Start a new trip
- `GET /api/trips` - List all trips
- `GET /api/vehicles/{id}/trips` - Get vehicle trips
- `POST /api/trips/{id}/complete` - Complete a trip
- `PUT /api/trips/{id}` - Update a trip
- `DELETE /api/trips/{id}` - Delete a trip

### Statistics
- `GET /api/dashboard/stats` - Get dashboard statistics

## Data Models

### Vehicle
- Basic info: make, model, year, license plate, VIN
- Fuel type and tank capacity
- Current mileage and purchase details

### Fillup
- Mileage, gallons, price per gallon, total cost
- Fuel brand, location, full tank indicator
- Automatic MPG calculations

### Maintenance Record
- Service type, description, cost, provider
- Mileage at service, next service scheduling
- Categories: oil changes, tires, brakes, etc.

### Trip
- Start/end dates and mileage
- Purpose, locations, distance calculation
- Automatic distance computation

## Features in Detail

### Fuel Efficiency Tracking
- Automatic MPG calculations from fill-up data
- Cost per mile analysis
- Fuel brand and location tracking
- Historical fuel price trends

### Maintenance Scheduling
- Service type categorization
- Next service mileage/due dates
- Cost tracking and provider history
- Maintenance interval recommendations

### Trip Management
- Real-time trip tracking
- Purpose-based categorization
- Location logging
- Distance and duration calculations

### Statistics & Analytics
- Overall fuel costs and efficiency
- Vehicle-specific performance metrics
- Maintenance scheduling alerts
- Trip summaries and patterns

### Data Validation
- Mileage progression validation
- Fuel efficiency calculations
- Service interval recommendations
- Date and location tracking
