"""Route planning and optimization engine."""

from typing import List, Optional
from pydantic import BaseModel

from models import Route, RouteOption, RouteRestriction, CargoCategory
from apis.data_store import DataStore


class RouteRecommendation(BaseModel):
    """Route recommendation result."""
    origin: str
    destination: str
    options: List[RouteOption]
    recommended: Optional[str] = None  # route_id of best option
    note: Optional[str] = None


class RestrictionCheck(BaseModel):
    """Route restriction check result."""
    cargo_category: CargoCategory
    route_id: Optional[str]
    origin: Optional[str]
    destination: Optional[str]
    allowed: bool
    requirements: List[str]
    alternative_routes: List[str]
    notes: Optional[str] = None


def recommend_routes(
    origin: str,
    destination: str,
    data_store: DataStore,
    cargo_type: Optional[CargoCategory] = None,
    priority: str = "balanced",
) -> RouteRecommendation:
    """Recommend optimal routes between origin and destination."""
    routes = data_store.load_routes()
    options = []

    for route in routes:
        # Match origin and destination (case-insensitive partial match)
        if origin.lower() not in route.origin.lower():
            continue
        if destination.lower() not in route.destination.lower():
            continue

        # Check cargo restrictions
        if cargo_type:
            restricted = False
            for r in route.restrictions:
                if r.cargo_category == cargo_type and not r.allowed:
                    restricted = True
                    break
            if restricted:
                continue

        # Calculate estimated cost based on distance
        carriers = data_store.load_carriers()
        avg_rate = sum(c.base_rate_per_km for c in carriers) / len(carriers) if carriers else 2.5
        estimated_cost = route.distance_km * avg_rate

        option = RouteOption(
            route_id=route.route_id,
            name=route.name,
            origin=route.origin,
            destination=route.destination,
            distance_km=route.distance_km,
            estimated_hours=route.estimated_hours,
            estimated_cost=estimated_cost,
            waypoints_count=len(route.waypoints),
            restrictions=[r.cargo_category.value for r in route.restrictions if not r.allowed],
        )
        options.append(option)

    # Sort by priority
    if priority == "cost":
        options.sort(key=lambda x: x.estimated_cost)
    elif priority == "time":
        options.sort(key=lambda x: x.estimated_hours)
    else:  # balanced
        options.sort(key=lambda x: x.estimated_cost + x.estimated_hours * 10)

    recommended = options[0].route_id if options else None

    return RouteRecommendation(
        origin=origin,
        destination=destination,
        options=options[:5],  # Return top 5
        recommended=recommended,
        note=f"Found {len(options)} route(s)" if options else "No routes found for this origin-destination pair",
    )


def get_route_details(route_id: str, data_store: DataStore) -> Optional[Route]:
    """Get detailed route information."""
    return data_store.get_route_by_id(route_id)


def check_route_restrictions(
    cargo_type: CargoCategory,
    data_store: DataStore,
    route_id: Optional[str] = None,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
) -> RestrictionCheck:
    """Check if cargo type is allowed on route."""
    route = None
    if route_id:
        route = data_store.get_route_by_id(route_id)
    elif origin and destination:
        recommendation = recommend_routes(origin, destination, data_store, cargo_type)
        if recommendation.options:
            route = data_store.get_route_by_id(recommendation.options[0].route_id)

    if not route:
        return RestrictionCheck(
            cargo_category=cargo_type,
            route_id=route_id,
            origin=origin,
            destination=destination,
            allowed=True,
            requirements=[],
            alternative_routes=[],
            notes="Route not found - assuming allowed",
        )

    for restriction in route.restrictions:
        if restriction.cargo_category == cargo_type:
            return RestrictionCheck(
                cargo_category=cargo_type,
                route_id=route.route_id,
                origin=route.origin,
                destination=route.destination,
                allowed=restriction.allowed,
                requirements=restriction.requirements,
                alternative_routes=[],  # Would need to query other routes
                notes=restriction.notes,
            )

    # No restriction found means allowed
    return RestrictionCheck(
        cargo_category=cargo_type,
        route_id=route.route_id,
        origin=route.origin,
        destination=route.destination,
        allowed=True,
        requirements=[],
        alternative_routes=[],
    )