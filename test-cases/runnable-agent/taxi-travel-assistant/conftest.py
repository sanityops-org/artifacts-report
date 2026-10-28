#!/usr/bin/env python3
"""
pytest Global configuration

Reset the state of simulation data (sim_db) to avoid state pollution across test modules.
For example, after order_booking test and placing an order, the vehicle will be set to busy. If it is not reset,
Subsequent vehicle_query tests will not be able to query available vehicles.
"""

import sys
from pathlib import Path

# Add the agent root directory to sys.path to ensure that the import data module can be
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest


@pytest.fixture(autouse=True)
def reset_sim_db():
    """Reset the vehicle and order status before the start of each test."""
    from data import sim_db

    # Restore all vehicles to idle (ordering/cancellation will change the status)
    for vehicle in sim_db.VEHICLES.values():
        vehicle["status"] = "idle"

    # Empty the order library to avoid the order number and vehicle status cross-test residue.
    sim_db.ORDERS.clear()

    yield
