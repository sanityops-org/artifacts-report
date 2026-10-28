#!/usr/bin/env python3
"""
Simulated data source

Simulate MRO system data sources, including component library, time control library, AD/SB library, and aircraft history library.
"""

# Parts library
COMPONENTS = {
    "PN-12345": {
        "name": "The main landing gear is the action cylinder",
        "category": "life_limited",  # life_limited | time_controlled | on_condition
        "total_life_hours": 12000,
        "total_life_cycles": 8000,
        "sb_list": ["SB-2025-001"],
    },
    "PN-67890": {
        "name": "APU Start the generator",
        "category": "time_controlled",
        "tci_reference": "TCI-001",
        "sb_list": [],
    },
    "PN-11111": {
        "name": "Left-handed fuel pump",
        "category": "life_limited",
        "total_life_hours": 15000,
        "total_life_cycles": 10000,
        "sb_list": [],
    },
}

# Time control library
TIME_CONTROLLED_ITEMS = {
    "TCI-001": {
        "name": "APU Start the generator",
        "limit_type": "hours",  # hours | cycles | calendar
        "limit_value": 3000,
        "alert_threshold": 0.8,
        "install_date": "2024-01-15",
    },
    "TCI-002": {
        "name": "Brake assembly",
        "limit_type": "cycles",
        "limit_value": 2000,
        "alert_threshold": 0.85,
        "install_date": "2025-03-01",
    },
}

# Airworthiness command bank (AD)
AIRWORTHINESS_DIRECTIVES = {
    "AD-2024-01-001": {
        "title": "Check the rack-up and release of the landing gear",
        "effective_date": "2024-03-01",
        "compliance": "mandatory",  # mandatory | recommended
        "affected_parts": ["PN-12345"],
        "status": "open",  # open | complied | superseded
        "superseded_by": None,
        "deadline_days": 90,
    },
    "AD-2024-02-001": {
        "title": "Fuel pump sealing inspection",
        "effective_date": "2024-06-01",
        "compliance": "mandatory",
        "affected_parts": ["PN-11111"],
        "status": "open",
        "superseded_by": None,
        "deadline_days": 60,
    },
    "AD-2023-05-001": {
        "title": "Old version of landing gear inspection (replaced)",
        "effective_date": "2023-05-01",
        "compliance": "mandatory",
        "affected_parts": ["PN-12345"],
        "status": "superseded",
        "superseded_by": "AD-2024-01-001",
        "deadline_days": None,
    },
}

# Service announcement library (SB)
# Note: Reserved as a future extension point, there is no SB query logic for the time being.
SERVICE_BULLETINS = {
    "SB-2025-001": {
        "title": "APU Improved starting motor installation",
        "issued_date": "2025-01-10",
        "compliance": "recommended",
        "affected_parts": ["PN-12345"],
        "estimated_hours": 8,
    },
    "SB-2025-002": {
        "title": "Fuel pipeline improvement",
        "issued_date": "2025-03-15",
        "compliance": "recommended",
        "affected_parts": ["PN-11111"],
        "estimated_hours": 4,
    },
}

# Aircraft resume library
AIRCRAFT_RECORDS = {
    "B-1234": {
        "model": "A320",
        "total_hours": 15234,
        "total_cycles": 8901,
        "components": {
            "PN-12345": {
                "install_date": "2023-06-01",
                "hours_since_install": 2150,
                "cycles_since_install": 1203,
                "last_check_date": "2026-08-15",
            },
            "PN-67890": {
                "install_date": "2024-01-15",
                "hours_since_install": 2800,
                "cycles_since_install": 1500,
                "last_check_date": "2026-08-20",
            },
            "PN-11111": {
                "install_date": "2022-01-01",
                "hours_since_install": 14234,
                "cycles_since_install": 7901,
                "last_check_date": "2026-07-10",
            },
        },
        "open_defects": [
            {
                "id": "DEF-001",
                "description": "Leakage of lubricating oil on the right",
                "severity": "medium",
                "mel_reference": "MEL-79-01",
                "mel_deadline": "2026-09-10",
            },
            {
                "id": "DEF-002",
                "description": "Cabin reading light failure",
                "severity": "low",
                "mel_reference": None,
                "mel_deadline": None,
            },
        ],
        "ad_compliance": {
            "AD-2024-01-001": {"status": "complied", "date": "2024-04-15"},
        },
    },
    "B-5678": {
        "model": "A320",
        "total_hours": 8500,
        "total_cycles": 5200,
        "components": {
            "PN-12345": {
                "install_date": "2025-01-01",
                "hours_since_install": 500,
                "cycles_since_install": 300,
                "last_check_date": "2026-08-01",
            },
        },
        "open_defects": [],
        "ad_compliance": {
            "AD-2024-01-001": {"status": "complied", "date": "2025-06-15"},
            "AD-2024-02-001": {"status": "complied", "date": "2025-07-01"},
        },
    },
}
