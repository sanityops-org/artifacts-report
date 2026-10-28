#!/usr/bin/env python3
"""
Auxiliary function

Provide auxiliary functions such as route calculation, cost calculation, vehicle matching, etc.
"""

import math
from typing import Dict, Any, List, Optional

from . import sim_db


def calc_route(origin: str, destination: str) -> Optional[Dict[str, Any]]:
    """
    Calculate the route information

    Args:
        origin: Starting point ID
        destination: End point ID

    Returns:
        dict: distance_km, duration_min, toll, waypoints
        None: Unable to find the route
    """
    # Check whether the position exists.
    if origin not in sim_db.LOCATIONS:
        return None
    if destination not in sim_db.LOCATIONS:
        return None

    # Directly query the road network matrix
    key = (origin, destination)
    reverse_key = (destination, origin)

    route_info = sim_db.ROUTE_MATRIX.get(key) or sim_db.ROUTE_MATRIX.get(reverse_key)

    if route_info:
        return {
            "distance_km": route_info["distance_km"],
            "duration_min": route_info["duration_min"],
            "toll": route_info["toll"],
            "waypoints": [sim_db.LOCATIONS[origin]["name"], sim_db.LOCATIONS[destination]["name"]],
        }

    # If there is no direct route, estimate the straight line distance.
    origin_coords = sim_db.LOCATIONS[origin]["coords"]
    dest_coords = sim_db.LOCATIONS[destination]["coords"]

    distance = haversine_distance(
        origin_coords["lat"], origin_coords["lng"],
        dest_coords["lat"], dest_coords["lng"]
    )

    # Estimated: The distance of urban roads is about 1.4 times the distance in a straight line.
    estimated_distance = distance * 1.4
    # Estimate: the average speed of the city 25 km/h
    estimated_duration = estimated_distance / 25 * 60

    return {
        "distance_km": round(estimated_distance, 1),
        "duration_min": round(estimated_duration),
        "toll": 0,
        "waypoints": [sim_db.LOCATIONS[origin]["name"], sim_db.LOCATIONS[destination]["name"]],
    }


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate the spherical distance between two points（km）
    """
    R = 6371  # Earth radius（km）

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calc_fare(
    distance_km: float,
    duration_min: float,
    category: str,
    time_of_day: str = "day"
) -> Dict[str, Any]:
    """
    Calculate the details of the cost

    Args:
        distance_km: Distance (kilometers)
        duration_min: Duration (minutes)
        category: Car model category (economic | comfort | premium | suv)
        time_of_day: Time period (day | night)

    Returns:
        dict: base_fare, distance_fare, time_fare, surcharge, total
    """
    if category not in sim_db.FARE_RULES:
        return {"error": f"Unknown car model: {category}"}

    rules = sim_db.FARE_RULES[category]

    base_fare = rules["base_fare"]
    distance_fare = distance_km * rules["per_km"]
    time_fare = duration_min * rules["per_min"]

    # Price increase at night
    night_surcharge = 0
    if time_of_day == "night":
        night_surcharge = (base_fare + distance_fare + time_fare) * (rules["night_surcharge"] - 1)

    # Long-distance price increase (exceeding the threshold part)
    long_distance_surcharge = 0
    if distance_km > rules["long_distance_threshold"]:
        extra_km = distance_km - rules["long_distance_threshold"]
        long_distance_surcharge = extra_km * rules["per_km"] * (rules["long_distance_surcharge"] - 1)

    total = base_fare + distance_fare + time_fare + night_surcharge + long_distance_surcharge

    return {
        "base_fare": round(base_fare, 2),
        "distance_fare": round(distance_fare, 2),
        "time_fare": round(time_fare, 2),
        "night_surcharge": round(night_surcharge, 2),
        "long_distance_surcharge": round(long_distance_surcharge, 2),
        "total": round(total, 2),
    }


def find_nearby_vehicles(
    location: str,
    category: Optional[str] = None,
    radius_km: float = 5.0
) -> List[Dict[str, Any]]:
    """
    Find available vehicles nearby

    Args:
        location: Place ID
        category: Model category filtering (optional)
        radius_km: Search radius (kilometers)

    Returns:
        list: List of available vehicles, each item includes vehicle_id, distance_km, eta_min
    """
    if location not in sim_db.LOCATIONS:
        return []

    loc_coords = sim_db.LOCATIONS[location]["coords"]
    nearby = []

    for vehicle_id, vehicle in sim_db.VEHICLES.items():
        # Filter status
        if vehicle["status"] != "idle":
            continue

        # Filter the car model
        if category and vehicle["category"] != category:
            continue

        # Calculate the distance
        vehicle_coords = vehicle["current_location"]
        distance = haversine_distance(
            loc_coords["lat"], loc_coords["lng"],
            vehicle_coords["lat"], vehicle_coords["lng"]
        )

        if distance <= radius_km:
            # Estimated arrival time: average urban speed 25 km/h
            eta_min = distance / 25 * 60
            nearby.append({
                "vehicle_id": vehicle_id,
                "plate_no": vehicle["plate_no"],
                "model": vehicle["model"],
                "category": vehicle["category"],
                "driver_name": vehicle["driver_name"],
                "rating": vehicle["rating"],
                "distance_km": round(distance, 2),
                "eta_min": round(eta_min),
            })

    # Sort by distance
    nearby.sort(key=lambda x: x["distance_km"])
    return nearby


def estimate_arrival(vehicle_id: str, pickup_location: str) -> Optional[int]:
    """
    Estimate the arrival time of the vehicle

    Args:
        vehicle_id: Vehicle ID
        pickup_location: The location of the bus point ID

    Returns:
        int: Estimated arrival time (minutes), None means that it cannot be estimated
    """
    if vehicle_id not in sim_db.VEHICLES:
        return None
    if pickup_location not in sim_db.LOCATIONS:
        return None

    vehicle = sim_db.VEHICLES[vehicle_id]
    loc_coords = sim_db.LOCATIONS[pickup_location]["coords"]

    distance = haversine_distance(
        vehicle["current_location"]["lat"], vehicle["current_location"]["lng"],
        loc_coords["lat"], loc_coords["lng"]
    )

    # The average speed of the city 25 km/h
    eta_min = distance / 25 * 60
    return round(eta_min)
