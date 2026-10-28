"""Integration tests for freight logistics assistant."""

import sys
from pathlib import Path
import pytest

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.tracking_engine import get_shipment_status
from apis.route_optimizer import recommend_routes
from apis.pricing_engine import calculate_quotation


class TestIntegration:
    """End-to-end integration tests."""

    @pytest.fixture
    def data_store(self):
        return DataStore(data_dir=project_root / "data")

    def test_shipment_tracking_flow(self, data_store):
        """Test complete shipment tracking flow."""
        result = get_shipment_status("FR202609300001234", data_store)

        assert result.found
        assert result.shipment.status.value == "in_transit"
        assert result.shipment.origin == "Shanghai"
        assert result.shipment.destination == "Beijing"

    def test_route_planning_flow(self, data_store):
        """Test route planning flow."""
        result = recommend_routes(
            origin="Shanghai",
            destination="Beijing",
            data_store=data_store,
        )

        assert len(result.options) > 0
        assert result.recommended is not None
        assert result.options[0].distance_km > 0

    def test_quotation_flow(self, data_store):
        """Test freight quotation flow."""
        quote = calculate_quotation(
            origin="Shanghai",
            destination="Beijing",
            weight_kg=5000,
            data_store=data_store,
        )

        assert quote is not None
        assert quote.total_estimate > 0
        assert quote.transit_days_min > 0

    def test_full_workflow(self, data_store):
        """Test complete workflow from tracking to quotation."""
        # 1. Track a shipment
        tracking = get_shipment_status("FR202609300001234", data_store)
        assert tracking.found

        # 2. Get route for the same origin-destination
        route = recommend_routes(
            origin=tracking.shipment.origin,
            destination=tracking.shipment.destination,
            data_store=data_store,
        )
        assert len(route.options) > 0

        # 3. Get quotation for the route
        quote = calculate_quotation(
            origin=tracking.shipment.origin,
            destination=tracking.shipment.destination,
            weight_kg=tracking.shipment.weight_kg,
            data_store=data_store,
        )
        assert quote is not None