"""Tools package for freight logistics assistant.

All tools in this package follow the convention:
- File name is the tool name
- Module-level docstring is the tool description
- Module-level 'parameters' is the JSON Schema for parameters
- execute(params: dict) -> dict is the entry point
"""

from tools.shipment_get_status import execute as shipment_get_status
from tools.shipment_get_history import execute as shipment_get_history
from tools.shipment_list_by_route import execute as shipment_list_by_route
from tools.route_recommend_options import execute as route_recommend_options
from tools.route_get_details import execute as route_get_details
from tools.route_check_restrictions import execute as route_check_restrictions
from tools.freight_calculate_estimate import execute as freight_calculate_estimate
from tools.freight_compare_carriers import execute as freight_compare_carriers
from tools.freight_get_transit_time import execute as freight_get_transit_time

__all__ = [
    "shipment_get_status",
    "shipment_get_history",
    "shipment_list_by_route",
    "route_recommend_options",
    "route_get_details",
    "route_check_restrictions",
    "freight_calculate_estimate",
    "freight_compare_carriers",
    "freight_get_transit_time",
]