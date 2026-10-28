#!/usr/bin/env python3
"""
Simulated data source

Simulate the data of the government hotline system, including departmental library, keyword mapping, emergency grading rules, and work order library.
"""

from typing import Dict, Any, List

# Department library
DEPARTMENTS: Dict[str, Dict[str, Any]] = {
    "eco_env": {
        "name": "Ecology and Environment Bureau",
        "description": "Responsible for environmental pollution prevention and control and ecological protection supervision",
        "contact": "12369"
    },
    "urban_mgmt": {
        "name": "City Administration",
        "description": "Responsible for the supervision of city environmental sanitation, illegal construction and road occupation",
        "contact": "12319"
    },
    "hr_ss": {
        "name": "Human Resources and Social Security Bureau",
        "description": "Responsible for labor security, social security employment and wage arrears",
        "contact": "12333"
    },
    "med_insurance": {
        "name": "Medical Security Bureau",
        "description": "Responsible for medical insurance, medical insurance treatment and medical assistance",
        "contact": "12393"
    },
    "housing": {
        "name": "Housing and Construction Bureau",
        "description": "Responsible for real estate management, property management and housing security",
        "contact": "12345"
    },
    "market_reg": {
        "name": "Market Supervision Bureau",
        "description": "Responsible for food safety, market order and consumer rights protection",
        "contact": "12315"
    },
    "emergency": {
        "name": "Emergency Management Bureau",
        "description": "Responsible for safe production, fire rescue and emergency response",
        "contact": "119"
    },
    "traffic": {
        "name": "Bureau of Transport",
        "description": "Responsible for transportation, bus rental and road management",
        "contact": "12328"
    },
    "education": {
        "name": "Bureau of education",
        "description": "Responsible for education management, enrollment and school supervision",
        "contact": "12345"
    },
    "health": {
        "name": "Health Commission",
        "description": "Responsible for medical and health, public health and health services",
        "contact": "12320"
    },
    "public_security": {
        "name": "Public security bureau",
        "description": "Responsible for public security management, household registration management and traffic safety",
        "contact": "110"
    },
    "default": {
        "name": "Comprehensive Coordination Office",
        "description": "Responsible for cross-departmental coordination and handling of difficult work orders",
        "contact": "12345"
    }
}

# Keywords - Department Mapping Table
KEYWORD_DEPT_MAPPING: Dict[str, str] = {
    # Eco-environment
    "Noise": "eco_env",
    "Noise": "eco_env",
    "Noise disturbs people": "eco_env",
    "Air pollution": "eco_env",
    "Exhaust fumes": "eco_env",
    "Rare delicacy": "eco_env",
    "Water pollution": "eco_env",
    "Dispose of pollutants": "eco_env",
    "Kick up dust": "eco_env",

    # City management
    "Occupy the road and operate": "urban_mgmt",
    "Illegal construction": "urban_mgmt",
    "Illegal construction": "urban_mgmt",
    "Build randomly": "urban_mgmt",
    "Appearance of a city": "urban_mgmt",
    "Sanitation": "urban_mgmt",
    "Rubbish": "urban_mgmt",
    "Refuse classification": "urban_mgmt",
    "Municipal facilities": "urban_mgmt",
    "Manhole cover": "urban_mgmt",
    "Street lamp": "urban_mgmt",

    # People's society
    "Wage arrears": "hr_ss",
    "Unpaid salary": "hr_ss",
    "Not paid the salary": "hr_ss",
    "Delay paying a salary": "hr_ss",
    "Labor arbitration": "hr_ss",
    "Social insurance": "hr_ss",
    "Pension": "hr_ss",
    "Unemployment benefit": "hr_ss",
    "Work injury insurance": "hr_ss",
    "Find a job": "hr_ss",

    # Medical insurance
    "Medical insurance": "med_insurance",
    "Medical insurance card": "med_insurance",
    "Medical insurance reimbursement": "med_insurance",
    "Medical treatment": "med_insurance",

    # Housing construction
    "Real estate certificate": "housing",
    "Property": "housing",
    "Property": "housing",
    "Property management": "housing",
    "Housing": "housing",
    "Public rental housing": "housing",
    "Pull down old houses and relocate the residents": "housing",
    "Dilapidated building": "housing",

    # Market supervision
    "Food safety": "market_reg",
    "Food hygiene": "market_reg",
    "Foodstuffs": "market_reg",
    "Consumer rights protection": "market_reg",
    "Consumer complaints": "market_reg",
    "Counterfeit and inferior": "market_reg",
    "Price fraud": "market_reg",
    "Price": "market_reg",
    "Business licence": "market_reg",

    # Emergency management
    "Inferno": "emergency",
    "Fire": "emergency",
    "Fire fighting": "emergency",
    "Fuel gas": "emergency",
    "Gas leakage": "emergency",
    "Gas": "emergency",
    "Safe production": "emergency",
    "Safety hazards": "emergency",

    # Communications and transport
    "Taxi": "traffic",
    "Public transport": "traffic",
    "Bus": "traffic",
    "Passenger transport": "traffic",
    "Driving school": "traffic",
    "Road": "traffic",
    "Road": "traffic",

    # Education
    "School": "education",
    "Start school": "education",
    "Recruit students": "education",
    "Make up missed lessons": "education",
    "Kindergarten": "education",
    "School district": "education",

    # Hygiene and health
    "Hospital": "health",
    "Clinic": "health",
    "Vaccination": "health",
    "Physical examination": "health",

    # Public security
    "Steal": "public_security",
    "Swindle": "public_security",
    "Law and order": "public_security",
    "Household register": "public_security",
    "Identity card": "public_security",
    "Traffic violations": "public_security",
    "Illegal parking": "public_security",
}

# Keywords of urgency
URGENCY_KEYWORDS: Dict[str, List[str]] = {
    "critical": [
        "Fire", "Explosion", "Group Complaint", "Collective complaint", "Group", "Personal Safety",
        "Gas leak", "gas leak", "significant", "Casualty", "Death",
        "Emergency", "danger", "collapse", "poisoning", "suffocation"
    ],
    "urgent": [
        "Disturbing people", "disturbs people", "violation", "sudden", "serious impact", "accident",
        "Leakage", "blockage", "interruption", "water stop", "power outage", "lost power", "gas stop",
        "Damage", "Pollution", "Blockage", "Safety Hazards"
    ],
    "normal": []  # Default level
}

# Work order storage (memory simulation)
TICKETS: Dict[str, Dict[str, Any]] = {}

# Work order counter
TICKET_COUNTER: int = 0

# Work order status flow
TICKET_STATUS_FLOW = ["pending", "processing", "resolved"]

# Estimated processing time limit (hours)
URGENCY_DEADLINE = {
    "critical": 2,   # 2 hours of emergency
    "urgent": 24,    # Emergency 24 hours
    "normal": 72     # Ordinary 72 hours
}
