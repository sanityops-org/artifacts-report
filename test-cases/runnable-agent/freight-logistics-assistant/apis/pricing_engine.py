"""Freight pricing and quotation engine."""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from models import (
    Carrier,
    Quotation,
    QuotationComparison,
    AccessorialCharge,
    ServiceLevel,
    CargoCategory,
    QuotationStatus,
)
from apis.data_store import DataStore
from apis.route_optimizer import recommend_routes


class TransitTimeResult(BaseModel):
    """Transit time estimate."""
    origin: str
    destination: str
    min_days: int
    max_days: int
    average_days: float
    carrier: Optional[str] = None
    service_level: Optional[ServiceLevel] = None
    factors: List[str] = []


def calculate_quotation(
    origin: str,
    destination: str,
    weight_kg: float,
    data_store: DataStore,
    volume_cbm: Optional[float] = None,
    cargo_type: Optional[CargoCategory] = None,
    service_level: ServiceLevel = ServiceLevel.STANDARD,
    carrier_id: Optional[str] = None,
) -> Optional[Quotation]:
    """Calculate freight quotation estimate."""
    # Get route distance
    recommendation = recommend_routes(origin, destination, data_store)
    if not recommendation.options:
        return None

    route_option = recommendation.options[0]
    distance_km = route_option.distance_km

    # Get carrier
    carrier = None
    if carrier_id:
        carrier = data_store.get_carrier_by_id(carrier_id)
    if not carrier:
        carriers = data_store.load_carriers()
        carrier = carriers[0] if carriers else None
    if not carrier:
        return None

    # Calculate base rate
    base_rate = distance_km * carrier.base_rate_per_km

    # Apply weight/volume chargeable
    if volume_cbm:
        # Use volumetric weight if higher (1 CBM = 167 kg)
        volumetric_weight = volume_cbm * 167
        if volumetric_weight > weight_kg:
            weight_chargeable = volumetric_weight
        else:
            weight_chargeable = weight_kg
    else:
        weight_chargeable = weight_kg

    # Weight surcharge for heavy loads
    weight_surcharge = 0
    if weight_chargeable > 20000:  # Over 20 tons
        weight_surcharge = (weight_chargeable - 20000) * 0.02

    # Fuel surcharge
    fuel_surcharge = base_rate * carrier.fuel_surcharge_pct

    # Service level multiplier
    service_multiplier = {
        ServiceLevel.ECONOMY: 0.85,
        ServiceLevel.STANDARD: 1.0,
        ServiceLevel.EXPRESS: 1.5,
    }.get(service_level, 1.0)

    base_rate *= service_multiplier

    # Cargo type surcharge
    cargo_surcharge = 0
    if cargo_type == CargoCategory.REFRIGERATED:
        cargo_surcharge = base_rate * 0.25
    elif cargo_type == CargoCategory.HAZARDOUS:
        cargo_surcharge = base_rate * 0.35
    elif cargo_type == CargoCategory.OVERSIZED:
        cargo_surcharge = base_rate * 0.40
    elif cargo_type == CargoCategory.HIGH_VALUE:
        cargo_surcharge = base_rate * 0.15

    # Total
    total = max(
        carrier.min_charge,
        base_rate + fuel_surcharge + weight_surcharge + cargo_surcharge,
    )

    # Transit time estimation
    transit_days = int(distance_km / 500) + 1  # Rough estimate: 500 km per day
    if service_level == ServiceLevel.EXPRESS:
        transit_days = max(1, transit_days - 1)
    elif service_level == ServiceLevel.ECONOMY:
        transit_days += 2

    # Generate quote ID
    quote_id = f"QT{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return Quotation(
        quote_id=quote_id,
        carrier_id=carrier.carrier_id,
        carrier_name=carrier.name,
        route_id=route_option.route_id,
        origin=origin,
        destination=destination,
        distance_km=distance_km,
        weight_kg=weight_kg,
        volume_cbm=volume_cbm,
        service_level=service_level,
        base_rate=round(base_rate, 2),
        fuel_surcharge=round(fuel_surcharge, 2),
        accessorial_charges=[
            AccessorialCharge(name="Weight surcharge", amount=round(weight_surcharge, 2)),
            AccessorialCharge(name="Cargo type surcharge", amount=round(cargo_surcharge, 2)),
        ] if weight_surcharge > 0 or cargo_surcharge > 0 else [],
        total_estimate=round(total, 2),
        transit_days_min=max(1, transit_days - 1),
        transit_days_max=transit_days + 1,
        valid_until=datetime.now() + timedelta(days=7),
        status=QuotationStatus.VALID,
    )


def compare_carriers(
    origin: str,
    destination: str,
    weight_kg: float,
    data_store: DataStore,
    volume_cbm: Optional[float] = None,
    cargo_type: Optional[CargoCategory] = None,
    service_level: ServiceLevel = ServiceLevel.STANDARD,
    carrier_ids: Optional[List[str]] = None,
) -> QuotationComparison:
    """Compare quotations from multiple carriers."""
    carriers = data_store.load_carriers()

    if carrier_ids:
        carriers = [c for c in carriers if c.carrier_id in carrier_ids]

    quotes = []
    for carrier in carriers[:5]:  # Max 5 carriers
        quote = calculate_quotation(
            origin=origin,
            destination=destination,
            weight_kg=weight_kg,
            volume_cbm=volume_cbm,
            cargo_type=cargo_type,
            service_level=service_level,
            carrier_id=carrier.carrier_id,
            data_store=data_store,
        )
        if quote:
            quotes.append(quote)

    # Sort by price
    quotes.sort(key=lambda q: q.total_estimate)

    best_price = quotes[0].quote_id if quotes else None
    fastest = min(quotes, key=lambda q: q.transit_days_max).quote_id if quotes else None

    return QuotationComparison(
        origin=origin,
        destination=destination,
        weight_kg=weight_kg,
        quotes=quotes,
        best_price=best_price,
        fastest=fastest,
    )


def get_transit_time(
    origin: str,
    destination: str,
    data_store: DataStore,
    carrier_id: Optional[str] = None,
    service_level: Optional[ServiceLevel] = None,
) -> TransitTimeResult:
    """Get estimated transit time between locations."""
    recommendation = recommend_routes(origin, destination, data_store)
    if not recommendation.options:
        return TransitTimeResult(
            origin=origin,
            destination=destination,
            min_days=0,
            max_days=0,
            average_days=0,
            factors=["Route not found"],
        )

    distance_km = recommendation.options[0].distance_km

    # Base transit time calculation
    base_days = int(distance_km / 500) + 1

    # Apply service level adjustment
    if service_level == ServiceLevel.EXPRESS:
        base_days = max(1, base_days - 1)
    elif service_level == ServiceLevel.ECONOMY:
        base_days += 2

    factors = []
    if distance_km > 2000:
        factors.append("Long distance route")
    if service_level == ServiceLevel.EXPRESS:
        factors.append("Express service")
    elif service_level == ServiceLevel.ECONOMY:
        factors.append("Economy service")

    return TransitTimeResult(
        origin=origin,
        destination=destination,
        min_days=max(1, base_days - 1),
        max_days=base_days + 2,
        average_days=base_days,
        carrier=carrier_id,
        service_level=service_level,
        factors=factors,
    )