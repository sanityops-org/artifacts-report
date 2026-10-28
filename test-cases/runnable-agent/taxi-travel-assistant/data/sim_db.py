#!/usr/bin/env python3
"""
Simulated data source

Simulate the data source of the online car-hailing platform, including vehicle library, site library, road network library, order library and price rules.
"""

# Vehicle warehouse
VEHICLES = {
    "V-001": {
        "plate_no": "Capital of a countryA12345",
        "model": "Toyota Corolla",
        "category": "economic",      # economic | comfort | premium | suv
        "status": "idle",            # idle | busy | offline
        "current_location": {"lat": 39.8946, "lng": 116.3220},  # Near Beijing West Station
        "driver_name": "Master Zhang",
        "driver_phone": "138****1234",
        "rating": 4.8,
    },
    "V-002": {
        "plate_no": "Capital of a countryB88888",
        "model": "Volkswagen Passat",
        "category": "comfort",
        "status": "idle",
        "current_location": {"lat": 39.9042, "lng": 116.4074},  # Near Tiananmen
        "driver_name": "Master Li",
        "driver_phone": "139****5678",
        "rating": 4.9,
    },
    "V-003": {
        "plate_no": "Capital of a countryC66666",
        "model": "Mercedes-Benz E-class",
        "category": "premium",
        "status": "idle",
        "current_location": {"lat": 39.9042, "lng": 116.4074},
        "driver_name": "Master Wang",
        "driver_phone": "137****9012",
        "rating": 4.95,
    },
    "V-004": {
        "plate_no": "Capital of a countryD77777",
        "model": "Toyota Highlander",
        "category": "suv",
        "status": "idle",
        "current_location": {"lat": 39.8946, "lng": 116.3220},
        "driver_name": "Master Zhao",
        "driver_phone": "136****3456",
        "rating": 4.85,
    },
    "V-005": {
        "plate_no": "Capital of a countryE55555",
        "model": "Honda Accord",
        "category": "comfort",
        "status": "busy",            # Busy
        "current_location": {"lat": 39.9042, "lng": 116.4074},
        "driver_name": "Master Sun",
        "driver_phone": "135****7890",
        "rating": 4.7,
    },
    "V-006": {
        "plate_no": "Capital of a countryF99999",
        "model": "Volkswagen Maiteng",
        "category": "comfort",
        "status": "idle",
        "current_location": {"lat": 39.8946, "lng": 116.3220},  # Near Beijing West Station
        "driver_name": "Master Zhou",
        "driver_phone": "134****2468",
        "rating": 4.88,
    },
}

# Site/Landmark Library
LOCATIONS = {
    "L-001": {
        "name": "Beijing West Railway Station",
        "type": "station",           # station | airport | landmark | residential
        "coords": {"lat": 39.8946, "lng": 116.3220},
        "hot_level": "high",         # high | medium | low
    },
    "L-002": {
        "name": "Capital AirportT3",
        "type": "airport",
        "coords": {"lat": 40.0485, "lng": 116.6131},
        "hot_level": "high",
    },
    "L-003": {
        "name": "Daxing Airport",
        "type": "airport",
        "coords": {"lat": 39.5098, "lng": 116.4105},
        "hot_level": "high",
    },
    "L-004": {
        "name": "Tiananmen Square",
        "type": "landmark",
        "coords": {"lat": 39.9042, "lng": 116.3975},
        "hot_level": "high",
    },
    "L-005": {
        "name": "International TradeCBD",
        "type": "landmark",
        "coords": {"lat": 39.9087, "lng": 116.4594},
        "hot_level": "high",
    },
    "L-006": {
        "name": "Zhongguancun",
        "type": "landmark",
        "coords": {"lat": 39.9841, "lng": 116.3074},
        "hot_level": "medium",
    },
    "L-007": {
        "name": "Wangjing",
        "type": "residential",
        "coords": {"lat": 39.9862, "lng": 116.4816},
        "hot_level": "medium",
    },
    "L-008": {
        "name": "Sanlitun",
        "type": "landmark",
        "coords": {"lat": 39.9327, "lng": 116.4537},
        "hot_level": "medium",
    },
}

# Road network matrix (simplified: distance between stations/estimated time)
ROUTE_MATRIX = {
    ("L-001", "L-002"): {"distance_km": 35.2, "duration_min": 45, "toll": 15},
    ("L-001", "L-003"): {"distance_km": 55.0, "duration_min": 50, "toll": 20},
    ("L-001", "L-004"): {"distance_km": 8.5, "duration_min": 20, "toll": 0},
    ("L-001", "L-005"): {"distance_km": 15.0, "duration_min": 30, "toll": 0},
    ("L-001", "L-006"): {"distance_km": 18.0, "duration_min": 35, "toll": 0},
    ("L-001", "L-007"): {"distance_km": 22.0, "duration_min": 40, "toll": 0},
    ("L-001", "L-008"): {"distance_km": 14.0, "duration_min": 28, "toll": 0},
    ("L-002", "L-003"): {"distance_km": 75.0, "duration_min": 70, "toll": 30},
    ("L-002", "L-004"): {"distance_km": 28.0, "duration_min": 35, "toll": 10},
    ("L-002", "L-005"): {"distance_km": 25.0, "duration_min": 30, "toll": 10},
    ("L-002", "L-006"): {"distance_km": 30.0, "duration_min": 40, "toll": 10},
    ("L-002", "L-007"): {"distance_km": 20.0, "duration_min": 28, "toll": 10},
    ("L-002", "L-008"): {"distance_km": 22.0, "duration_min": 30, "toll": 10},
    ("L-003", "L-004"): {"distance_km": 50.0, "duration_min": 45, "toll": 15},
    ("L-003", "L-005"): {"distance_km": 45.0, "duration_min": 40, "toll": 15},
    ("L-004", "L-005"): {"distance_km": 5.0, "duration_min": 12, "toll": 0},
    ("L-004", "L-006"): {"distance_km": 12.0, "duration_min": 25, "toll": 0},
    ("L-004", "L-007"): {"distance_km": 14.0, "duration_min": 28, "toll": 0},
    ("L-004", "L-008"): {"distance_km": 6.0, "duration_min": 15, "toll": 0},
    ("L-005", "L-006"): {"distance_km": 15.0, "duration_min": 30, "toll": 0},
    ("L-005", "L-007"): {"distance_km": 10.0, "duration_min": 20, "toll": 0},
    ("L-005", "L-008"): {"distance_km": 4.0, "duration_min": 10, "toll": 0},
    ("L-006", "L-007"): {"distance_km": 8.0, "duration_min": 18, "toll": 0},
    ("L-006", "L-008"): {"distance_km": 16.0, "duration_min": 30, "toll": 0},
    ("L-007", "L-008"): {"distance_km": 10.0, "duration_min": 22, "toll": 0},
}

# Order library
ORDERS = {}

# Price rules (unit: yuan)
FARE_RULES = {
    "economic": {
        "base_fare": 13,
        "per_km": 2.3,
        "per_min": 0.5,
        "night_surcharge": 1.2,      # Price increase at night (23:00-05:00)
        "long_distance_threshold": 15,  # Long-distance threshold（km）
        "long_distance_surcharge": 1.5, # Long-distance price increase multiplier
    },
    "comfort": {
        "base_fare": 15,
        "per_km": 2.8,
        "per_min": 0.6,
        "night_surcharge": 1.3,
        "long_distance_threshold": 15,
        "long_distance_surcharge": 1.5,
    },
    "premium": {
        "base_fare": 18,
        "per_km": 3.5,
        "per_min": 0.8,
        "night_surcharge": 1.5,
        "long_distance_threshold": 20,
        "long_distance_surcharge": 1.3,
    },
    "suv": {
        "base_fare": 20,
        "per_km": 4.0,
        "per_min": 1.0,
        "night_surcharge": 1.5,
        "long_distance_threshold": 20,
        "long_distance_surcharge": 1.3,
    },
}

# The next order number
_next_order_id = 1

def generate_order_id():
    """Generate the order number"""
    global _next_order_id
    order_id = f"O-{_next_order_id:06d}"
    _next_order_id += 1
    return order_id
