const API_BASE = window.location.origin;

// Global state
let currentVehicles = [];
let activeTrip = null;

// DOM Elements
const tabs = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

// Dashboard stats elements
const totalVehiclesEl = document.getElementById('total-vehicles');
const totalMileageEl = document.getElementById('total-mileage');
const totalFuelCostEl = document.getElementById('total-fuel-cost');
const avgMpgEl = document.getElementById('avg-mpg');

// Utility functions
function showTab(tabName) {
    // Update tab buttons
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.textContent.toLowerCase().includes(tabName)) {
            tab.classList.add('active');
        }
    });

    // Update tab content
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message`;
    messageDiv.textContent = message;

    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.querySelector('main'));

    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function hideElement(element) {
    element.classList.add('hidden');
}

function showElement(element) {
    element.classList.remove('hidden');
}

function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
}

function formatMileage(mileage) {
    return mileage.toLocaleString('en-US', { maximumFractionDigits: 1 });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function getFuelTypeIcon(fuelType) {
    const icons = {
        'gasoline': '⛽',
        'diesel': '🛢️',
        'electric': '⚡',
        'hybrid': '🔋'
    };
    return icons[fuelType] || '⛽';
}

function getServiceTypeIcon(serviceType) {
    const icons = {
        'oil_change': '🛢️',
        'tire_rotation': '🛞',
        'brake_service': '🛑',
        'transmission': '⚙️',
        'cooling_system': '❄️',
        'battery': '🔋',
        'inspection': '🔍',
        'other': '🔧'
    };
    return icons[serviceType] || '🔧';
}

function getTripPurposeIcon(purpose) {
    const icons = {
        'business': '💼',
        'personal': '🏠',
        'commute': '🚗',
        'vacation': '🏖️',
        'errand': '🛒',
        'other': '📍'
    };
    return icons[purpose] || '📍';
}

// Dashboard functions
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard/stats`);
        if (response.ok) {
            const stats = await response.json();
            totalVehiclesEl.textContent = stats.total_vehicles;
            totalMileageEl.textContent = `${formatMileage(stats.total_mileage)} mi`;
            totalFuelCostEl.textContent = formatCurrency(stats.total_fuel_cost);
            avgMpgEl.textContent = stats.average_mpg ? `${stats.average_mpg} mpg` : 'N/A';
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// Vehicle functions
function showVehicleForm() {
    showElement(document.getElementById('vehicle-form'));
    document.getElementById('add-vehicle-btn').classList.add('hidden');
}

function hideVehicleForm() {
    hideElement(document.getElementById('vehicle-form'));
    document.getElementById('add-vehicle-btn').classList.remove('hidden');
    document.getElementById('create-vehicle-form').reset();
}

async function createVehicle(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const vehicleData = {
        name: formData.get('vehicle-name'),
        make: formData.get('vehicle-make'),
        model: formData.get('vehicle-model'),
        year: formData.get('vehicle-year') ? parseInt(formData.get('vehicle-year')) : null,
        license_plate: formData.get('license-plate') || null,
        vin: formData.get('vin') || null,
        fuel_type: formData.get('fuel-type'),
        tank_capacity_gallons: formData.get('tank-capacity') ? parseFloat(formData.get('tank-capacity')) : null,
        notes: formData.get('vehicle-notes') || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/vehicles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(vehicleData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create vehicle');
        }

        showMessage('Vehicle added successfully!');
        hideVehicleForm();
        loadVehicles();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadVehicles() {
    try {
        const response = await fetch(`${API_BASE}/api/vehicles`);
        if (response.ok) {
            const data = await response.json();
            currentVehicles = data.vehicles;
            displayVehicles(data.vehicles);
        }
    } catch (error) {
        console.error('Error loading vehicles:', error);
        showMessage('Failed to load vehicles', 'error');
    }
}

function displayVehicles(vehicles) {
    const container = document.getElementById('vehicles-container');
    const loading = document.getElementById('vehicles-loading');
    const empty = document.getElementById('vehicles-empty');
    const list = document.getElementById('vehicles-list');

    hideElement(loading);

    if (vehicles.length === 0) {
        showElement(empty);
        hideElement(list);
        return;
    }

    hideElement(empty);
    list.innerHTML = '';

    vehicles.forEach(vehicle => {
        const vehicleCard = document.createElement('div');
        vehicleCard.className = 'vehicle-card';

        const fuelIcon = getFuelTypeIcon(vehicle.fuel_type);

        vehicleCard.innerHTML = `
            <div class="vehicle-name">${vehicle.name}</div>
            <div class="vehicle-details">
                ${vehicle.year} ${vehicle.make} ${vehicle.model} ${fuelIcon}
                ${vehicle.license_plate ? `• ${vehicle.license_plate}` : ''}
            </div>
            <div class="vehicle-stats">
                <div class="vehicle-stat-item">
                    <div class="vehicle-stat-label">Mileage</div>
                    <div class="vehicle-stat-value">${formatMileage(vehicle.current_mileage)} mi</div>
                </div>
                <div class="vehicle-stat-item">
                    <div class="vehicle-stat-label">Fuel Type</div>
                    <div class="vehicle-stat-value">${vehicle.fuel_type}</div>
                </div>
            </div>
            <div class="vehicle-actions">
                <button onclick="viewVehicleStats(${vehicle.id})" class="secondary-btn">View Stats</button>
                <button onclick="deleteVehicle(${vehicle.id})" class="secondary-btn" style="background: #fee2e2; color: #ef4444; border-color: #ef4444;">Delete</button>
            </div>
        `;

        list.appendChild(vehicleCard);
    });

    showElement(list);
}

async function viewVehicleStats(vehicleId) {
    try {
        const response = await fetch(`${API_BASE}/api/vehicles/${vehicleId}/stats`);
        if (response.ok) {
            const stats = await response.json();
            showVehicleStatsModal(stats);
        }
    } catch (error) {
        showMessage('Failed to load vehicle stats', 'error');
    }
}

function showVehicleStatsModal(stats) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${stats.vehicle_name} - Statistics</h3>
                <button onclick="this.parentElement.parentElement.parentElement.remove()" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                    <div class="stat-card">
                        <div class="stat-number">${formatMileage(stats.total_mileage)}</div>
                        <div class="stat-label">Total Mileage</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.total_fillups}</div>
                        <div class="stat-label">Fill-ups</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${formatCurrency(stats.total_fuel_cost)}</div>
                        <div class="stat-label">Fuel Cost</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${stats.average_mpg || 'N/A'}</div>
                        <div class="stat-label">Avg MPG</div>
                    </div>
                </div>
                ${stats.last_fillup_mileage ? `<p><strong>Last Fill-up:</strong> ${formatMileage(stats.last_fillup_mileage)} mi</p>` : ''}
                ${stats.next_service_due ? `<p><strong>Next Service Due:</strong> ${formatMileage(stats.next_service_due)} mi</p>` : ''}
            </div>
        </div>
    `;

    document.body.appendChild(modal);
}

async function deleteVehicle(vehicleId) {
    if (!confirm('Are you sure you want to delete this vehicle? This will also delete all associated records.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/vehicles/${vehicleId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete vehicle');
        }

        showMessage('Vehicle deleted successfully');
        loadVehicles();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Fillup functions
function showFillupForm() {
    loadVehiclesForSelect('fillup-vehicle');
    showElement(document.getElementById('fillup-form'));
    document.getElementById('add-fillup-btn').classList.add('hidden');
}

function hideFillupForm() {
    hideElement(document.getElementById('fillup-form'));
    document.getElementById('add-fillup-btn').classList.remove('hidden');
    document.getElementById('create-fillup-form').reset();
}

async function createFillup(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const fillupData = {
        vehicle_id: parseInt(formData.get('fillup-vehicle')),
        mileage: parseFloat(formData.get('fillup-mileage')),
        gallons: parseFloat(formData.get('fillup-gallons')),
        price_per_gallon: parseFloat(formData.get('fillup-price')),
        total_cost: parseFloat(formData.get('fillup-gallons')) * parseFloat(formData.get('fillup-price')),
        fuel_brand: formData.get('fuel-brand') || null,
        location: formData.get('fillup-location') || null,
        is_full_tank: formData.get('full-tank') === 'on',
        notes: formData.get('fillup-notes') || null
    };

    const dateValue = formData.get('fillup-date');
    if (dateValue) {
        fillupData.date = new Date(dateValue).toISOString();
    }

    try {
        const response = await fetch(`${API_BASE}/api/fillups`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(fillupData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add fill-up');
        }

        showMessage('Fill-up added successfully!');
        hideFillupForm();
        loadFillups();
        loadVehicles();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadFillups() {
    const container = document.getElementById('fillups-container');
    const loading = document.getElementById('fillups-loading');
    const empty = document.getElementById('fillups-empty');
    const list = document.getElementById('fillups-list');

    try {
        showElement(loading);
        hideElement(empty);
        hideElement(list);

        const response = await fetch(`${API_BASE}/api/fillups`);
        if (!response.ok) {
            throw new Error('Failed to load fill-ups');
        }

        const data = await response.json();
        hideElement(loading);

        if (data.fillups.length === 0) {
            showElement(empty);
        } else {
            displayFillups(data.fillups);
        }
    } catch (error) {
        hideElement(loading);
        showMessage('Failed to load fill-ups', 'error');
        console.error('Error loading fill-ups:', error);
    }
}

function displayFillups(fillups) {
    const list = document.getElementById('fillups-list');
    list.innerHTML = '';

    fillups.forEach(fillup => {
        const fillupItem = document.createElement('div');
        fillupItem.className = 'fillup-item';

        const mpg = fillup.gallons > 0 ? (fillup.mileage / fillup.gallons).toFixed(1) : 'N/A';

        fillupItem.innerHTML = `
            <div class="fillup-header">
                <div>
                    <div class="fillup-vehicle">${fillup.vehicle.name}</div>
                    <div class="fillup-date">${formatDateTime(fillup.date)}</div>
                </div>
                <div class="fillup-mpg">${mpg} mpg</div>
            </div>

            <div class="fillup-details">
                <div class="fillup-detail-item">
                    <div class="fillup-detail-label">Mileage</div>
                    <div class="fillup-detail-value">${formatMileage(fillup.mileage)} mi</div>
                </div>
                <div class="fillup-detail-item">
                    <div class="fillup-detail-label">Gallons</div>
                    <div class="fillup-detail-value">${fillup.gallons} gal</div>
                </div>
                <div class="fillup-detail-item">
                    <div class="fillup-detail-label">Price/Gal</div>
                    <div class="fillup-detail-value">${formatCurrency(fillup.price_per_gallon)}</div>
                </div>
                <div class="fillup-detail-item">
                    <div class="fillup-detail-label">Total Cost</div>
                    <div class="fillup-detail-value">${formatCurrency(fillup.total_cost)}</div>
                </div>
            </div>

            ${fillup.location ? `<div class="fillup-location">📍 ${fillup.location}</div>` : ''}
            ${fillup.notes ? `<div class="fillup-notes">${fillup.notes}</div>` : ''}

            <div class="fillup-actions">
                <button onclick="deleteFillup(${fillup.id})" class="secondary-btn" style="background: #fee2e2; color: #ef4444; border-color: #ef4444;">Delete</button>
            </div>
        `;

        list.appendChild(fillupItem);
    });

    showElement(list);
}

async function deleteFillup(fillupId) {
    if (!confirm('Are you sure you want to delete this fill-up record?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/fillups/${fillupId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete fill-up');
        }

        showMessage('Fill-up deleted successfully');
        loadFillups();
        loadVehicles();
        loadDashboardStats();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Maintenance functions
function showMaintenanceForm() {
    loadVehiclesForSelect('maintenance-vehicle');
    showElement(document.getElementById('maintenance-form'));
    document.getElementById('add-maintenance-btn').classList.add('hidden');
}

function hideMaintenanceForm() {
    hideElement(document.getElementById('maintenance-form'));
    document.getElementById('add-maintenance-btn').classList.remove('hidden');
    document.getElementById('create-maintenance-form').reset();
}

async function createMaintenance(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const maintenanceData = {
        vehicle_id: parseInt(formData.get('maintenance-vehicle')),
        mileage: parseFloat(formData.get('maintenance-mileage')),
        service_type: formData.get('service-type'),
        description: formData.get('maintenance-description'),
        cost: formData.get('service-cost') ? parseFloat(formData.get('service-cost')) : null,
        provider: formData.get('service-provider') || null,
        next_service_mileage: formData.get('next-service-mileage') ? parseFloat(formData.get('next-service-mileage')) : null,
        notes: formData.get('maintenance-notes') || null
    };

    const dateValue = formData.get('service-date');
    if (dateValue) {
        maintenanceData.date = new Date(dateValue).toISOString();
    }

    const nextDateValue = formData.get('next-service-date');
    if (nextDateValue) {
        maintenanceData.next_service_date = new Date(nextDateValue).toISOString();
    }

    try {
        const response = await fetch(`${API_BASE}/api/maintenance`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(maintenanceData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add maintenance record');
        }

        showMessage('Maintenance record added successfully!');
        hideMaintenanceForm();
        loadMaintenance();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

async function loadMaintenance() {
    const container = document.getElementById('maintenance-container');
    const loading = document.getElementById('maintenance-loading');
    const empty = document.getElementById('maintenance-empty');
    const list = document.getElementById('maintenance-list');

    try {
        showElement(loading);
        hideElement(empty);
        hideElement(list);

        const response = await fetch(`${API_BASE}/api/maintenance`);
        if (!response.ok) {
            throw new Error('Failed to load maintenance records');
        }

        const data = await response.json();
        hideElement(loading);

        if (data.records.length === 0) {
            showElement(empty);
        } else {
            displayMaintenance(data.records);
        }
    } catch (error) {
        hideElement(loading);
        showMessage('Failed to load maintenance records', 'error');
        console.error('Error loading maintenance:', error);
    }
}

function displayMaintenance(records) {
    const list = document.getElementById('maintenance-list');
    list.innerHTML = '';

    records.forEach(record => {
        const maintenanceItem = document.createElement('div');
        maintenanceItem.className = 'maintenance-item';

        const serviceIcon = getServiceTypeIcon(record.service_type);

        maintenanceItem.innerHTML = `
            <div class="maintenance-header">
                <div>
                    <div class="maintenance-service">${serviceIcon} ${record.service_type.replace('_', ' ')}</div>
                    <div class="maintenance-vehicle">${record.vehicle.name}</div>
                </div>
                <div class="maintenance-date">${formatDateTime(record.date)}</div>
            </div>

            <div class="maintenance-description">${record.description}</div>

            <div class="maintenance-details">
                <div class="maintenance-detail-item">
                    <div class="maintenance-detail-label">Mileage</div>
                    <div class="maintenance-detail-value">${formatMileage(record.mileage)} mi</div>
                </div>
                ${record.cost ? `
                    <div class="maintenance-detail-item">
                        <div class="maintenance-detail-label">Cost</div>
                        <div class="maintenance-detail-value">${formatCurrency(record.cost)}</div>
                    </div>
                ` : ''}
                ${record.provider ? `
                    <div class="maintenance-detail-item">
                        <div class="maintenance-detail-label">Provider</div>
                        <div class="maintenance-detail-value">${record.provider}</div>
                    </div>
                ` : ''}
                ${record.next_service_mileage ? `
                    <div class="maintenance-detail-item">
                        <div class="maintenance-detail-label">Next Service</div>
                        <div class="maintenance-detail-value">${formatMileage(record.next_service_mileage)} mi</div>
                    </div>
                ` : ''}
            </div>

            ${record.notes ? `<div class="maintenance-notes">${record.notes}</div>` : ''}

            <div class="maintenance-actions">
                <button onclick="deleteMaintenance(${record.id})" class="secondary-btn" style="background: #fee2e2; color: #ef4444; border-color: #ef4444;">Delete</button>
            </div>
        `;

        list.appendChild(maintenanceItem);
    });

    showElement(list);
}

async function deleteMaintenance(recordId) {
    if (!confirm('Are you sure you want to delete this maintenance record?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/maintenance/${recordId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete maintenance record');
        }

        showMessage('Maintenance record deleted successfully');
        loadMaintenance();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Trip functions
function showTripForm() {
    loadVehiclesForSelect('trip-vehicle');
    showElement(document.getElementById('trip-form'));
    document.getElementById('start-trip-btn').classList.add('hidden');
}

function hideTripForm() {
    hideElement(document.getElementById('trip-form'));
    document.getElementById('start-trip-btn').classList.remove('hidden');
    document.getElementById('create-trip-form').reset();
}

async function createTrip(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const tripData = {
        vehicle_id: parseInt(formData.get('trip-vehicle')),
        start_mileage: parseFloat(formData.get('start-mileage')),
        purpose: formData.get('trip-purpose'),
        start_location: formData.get('start-location') || null,
        notes: formData.get('trip-notes') || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/trips`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(tripData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to start trip');
        }

        const trip = await response.json();
        showMessage('Trip started successfully!');
        hideTripForm();
        startActiveTrip(trip);
        loadTrips();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function startActiveTrip(trip) {
    activeTrip = trip;

    const activeTripDiv = document.getElementById('active-trip');
    const titleEl = document.getElementById('active-trip-title');
    const vehicleEl = document.getElementById('active-vehicle-name');
    const startTimeEl = document.getElementById('active-start-time');
    const startMileageEl = document.getElementById('active-start-mileage');

    titleEl.textContent = `Trip: ${trip.purpose.charAt(0).toUpperCase() + trip.purpose.slice(1)}`;
    vehicleEl.textContent = trip.vehicle?.name || 'Unknown Vehicle';
    startTimeEl.textContent = formatDateTime(trip.start_date);
    startMileageEl.textContent = formatMileage(trip.start_mileage);

    showElement(activeTripDiv);
}

function showCompleteTripModal() {
    showElement(document.getElementById('trip-modal'));
}

function closeTripModal() {
    hideElement(document.getElementById('trip-modal'));
    document.getElementById('complete-trip-form').reset();
}

async function completeTrip(event) {
    event.preventDefault();

    if (!activeTrip) return;

    const formData = new FormData(event.target);
    const endMileage = parseFloat(formData.get('end-mileage'));
    const endLocation = formData.get('end-location') || null;

    try {
        const response = await fetch(`${API_BASE}/api/trips/${activeTrip.id}/complete`, {
            method: 'POST',
            body: new URLSearchParams({
                end_mileage: endMileage,
                end_location: endLocation || ''
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to complete trip');
        }

        showMessage('Trip completed successfully!');
        closeTripModal();
        stopActiveTrip();
        loadTrips();
        loadVehicles();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

function stopActiveTrip() {
    activeTrip = null;
    hideElement(document.getElementById('active-trip'));
}

async function loadTrips() {
    const container = document.getElementById('trips-container');
    const loading = document.getElementById('trips-loading');
    const empty = document.getElementById('trips-empty');
    const list = document.getElementById('trips-list');

    try {
        showElement(loading);
        hideElement(empty);
        hideElement(list);

        const response = await fetch(`${API_BASE}/api/trips`);
        if (!response.ok) {
            throw new Error('Failed to load trips');
        }

        const data = await response.json();
        hideElement(loading);

        if (data.trips.length === 0) {
            showElement(empty);
        } else {
            displayTrips(data.trips);
        }
    } catch (error) {
        hideElement(loading);
        showMessage('Failed to load trips', 'error');
        console.error('Error loading trips:', error);
    }
}

function displayTrips(trips) {
    const list = document.getElementById('trips-list');
    list.innerHTML = '';

    trips.forEach(trip => {
        const tripItem = document.createElement('div');
        tripItem.className = `trip-item ${trip.end_date ? 'completed' : ''}`;

        const purposeIcon = getTripPurposeIcon(trip.purpose);

        tripItem.innerHTML = `
            <div class="trip-header">
                <div>
                    <div class="trip-purpose">${purposeIcon} ${trip.purpose.charAt(0).toUpperCase() + trip.purpose.slice(1)}</div>
                    <div class="trip-vehicle">${trip.vehicle?.name || 'Unknown Vehicle'}</div>
                </div>
                <div class="trip-status">
                    ${trip.end_date ? '✅ Completed' : '🏃 Active'}
                </div>
            </div>

            <div class="trip-details-grid">
                <div class="trip-detail-item">
                    <div class="trip-detail-label">Started</div>
                    <div class="trip-detail-value">${formatDateTime(trip.start_date)}</div>
                </div>
                ${trip.end_date ? `
                    <div class="trip-detail-item">
                        <div class="trip-detail-label">Completed</div>
                        <div class="trip-detail-value">${formatDateTime(trip.end_date)}</div>
                    </div>
                ` : ''}
                <div class="trip-detail-item">
                    <div class="trip-detail-label">Start Mileage</div>
                    <div class="trip-detail-value">${formatMileage(trip.start_mileage)} mi</div>
                </div>
                ${trip.end_mileage ? `
                    <div class="trip-detail-item">
                        <div class="trip-detail-label">End Mileage</div>
                        <div class="trip-detail-value">${formatMileage(trip.end_mileage)} mi</div>
                    </div>
                ` : ''}
                ${trip.distance ? `
                    <div class="trip-detail-item">
                        <div class="trip-detail-label">Distance</div>
                        <div class="trip-detail-value trip-distance">${formatMileage(trip.distance)} mi</div>
                    </div>
                ` : ''}
            </div>

            ${trip.start_location ? `<div class="trip-location">📍 From: ${trip.start_location}</div>` : ''}
            ${trip.end_location ? `<div class="trip-location">🏁 To: ${trip.end_location}</div>` : ''}
            ${trip.notes ? `<div class="trip-notes">${trip.notes}</div>` : ''}

            <div class="trip-actions">
                ${!trip.end_date ? '<button onclick="completeTripFromList(' + trip.id + ')" class="primary-btn">Complete Trip</button>' : ''}
                <button onclick="deleteTrip(${trip.id})" class="secondary-btn" style="background: #fee2e2; color: #ef4444; border-color: #ef4444;">Delete</button>
            </div>
        `;

        list.appendChild(tripItem);
    });

    showElement(list);
}

function completeTripFromList(tripId) {
    // Find trip in current trips and set as active
    // This is a simplified version - in a real app you'd fetch the trip details
    showCompleteTripModal();
}

async function deleteTrip(tripId) {
    if (!confirm('Are you sure you want to delete this trip?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/trips/${tripId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Failed to delete trip');
        }

        showMessage('Trip deleted successfully');
        loadTrips();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// Utility functions
async function loadVehiclesForSelect(selectId) {
    try {
        if (currentVehicles.length === 0) {
            await loadVehicles();
        }

        const select = document.getElementById(selectId);
        const currentValue = select.value;

        select.innerHTML = '<option value="">Select vehicle...</option>';

        currentVehicles.forEach(vehicle => {
            const option = document.createElement('option');
            option.value = vehicle.id;
            option.textContent = vehicle.name;
            select.appendChild(option);
        });

        if (currentValue) {
            select.value = currentValue;
        }
    } catch (error) {
        console.error('Error loading vehicles for select:', error);
    }
}

// Event listeners
document.getElementById('create-vehicle-form').addEventListener('submit', createVehicle);
document.getElementById('create-fillup-form').addEventListener('submit', createFillup);
document.getElementById('create-maintenance-form').addEventListener('submit', createMaintenance);
document.getElementById('create-trip-form').addEventListener('submit', createTrip);
document.getElementById('complete-trip-form').addEventListener('submit', completeTrip);

// Initialize the app
async function init() {
    await Promise.all([
        loadDashboardStats(),
        loadVehicles(),
        loadFillups(),
        loadMaintenance(),
        loadTrips()
    ]);

    // Set default tab
    showTab('vehicles');
}

// Start the app
init();
