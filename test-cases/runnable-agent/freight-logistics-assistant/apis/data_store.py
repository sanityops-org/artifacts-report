"""Data store for JSON-based mock data."""

import json
from pathlib import Path
from typing import TypeVar, Generic, List, Optional, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class DataStore:
    """Generic JSON data store for mock data."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def _load_list(self, filename: str, model: Type[T]) -> List[T]:
        """Load a JSON file as a list of Pydantic models."""
        file_path = self.data_dir / filename
        if not file_path.exists():
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [model.model_validate(item) for item in data]

    def _save_list(self, filename: str, items: List[BaseModel]) -> None:
        """Save a list of Pydantic models to JSON."""
        file_path = self.data_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                [item.model_dump(mode="json") for item in items],
                f,
                indent=2,
                ensure_ascii=False,
            )

    def load_shipments(self) -> List["Shipment"]:
        """Load all shipments."""
        from models import Shipment
        return self._load_list("shipments.json", Shipment)

    def load_routes(self) -> List["Route"]:
        """Load all routes."""
        from models import Route
        return self._load_list("routes.json", Route)

    def load_carriers(self) -> List["Carrier"]:
        """Load all carriers."""
        from models import Carrier
        return self._load_list("carriers.json", Carrier)

    def load_cargo_types(self) -> List["CargoType"]:
        """Load cargo type definitions."""
        from models import CargoType
        return self._load_list("cargo_types.json", CargoType)

    def load_pricing_rules(self) -> dict:
        """Load pricing rules."""
        file_path = self.data_dir / "pricing_rules.json"
        if not file_path.exists():
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_shipment_by_tracking(self, tracking_number: str) -> Optional["Shipment"]:
        """Get shipment by tracking number."""
        shipments = self.load_shipments()
        for s in shipments:
            if s.tracking_number == tracking_number:
                return s
        return None

    def get_route_by_id(self, route_id: str) -> Optional["Route"]:
        """Get route by ID."""
        routes = self.load_routes()
        for r in routes:
            if r.route_id == route_id:
                return r
        return None

    def get_carrier_by_id(self, carrier_id: str) -> Optional["Carrier"]:
        """Get carrier by ID."""
        carriers = self.load_carriers()
        for c in carriers:
            if c.carrier_id == carrier_id:
                return c
        return None