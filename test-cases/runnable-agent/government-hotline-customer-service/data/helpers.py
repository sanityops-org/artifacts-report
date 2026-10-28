#!/usr/bin/env python3
"""
Auxiliary function

Provide core functions such as department matching, emergency classification, work order number generation, etc.
"""

import re
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from data.sim_db import (
    DEPARTMENTS,
    KEYWORD_DEPT_MAPPING,
    URGENCY_KEYWORDS,
    TICKET_COUNTER,
    URGENCY_DEADLINE
)


def match_department(content: str) -> Dict[str, Any]:
    """
    Match the undertaking department according to the content of the complaint

    Args:
        content: Complaints/suggestions/consultation contents

    Returns:
        dict: {
            dept_id: DepartmentID,
            dept_name: Department name,
            dept_contact: Department contact number,
            is_auto: Whether to match automatically,
            confidence: The confidence of the match configuration (0-1),
            matched_keyword: Matched keywords (may be None)
        }
    """
    if not content:
        return {
            "dept_id": "default",
            "dept_name": DEPARTMENTS["default"]["name"],
            "dept_contact": DEPARTMENTS["default"]["contact"],
            "is_auto": False,
            "confidence": 0,
            "matched_keyword": None
        }

    # Traverse the keyword mapping to find the first matching keyword.
    matched_keyword = None
    dept_id = None

    content_lower = content.lower()
    for keyword, target_dept_id in KEYWORD_DEPT_MAPPING.items():
        if keyword.lower() in content_lower:
            matched_keyword = keyword
            dept_id = target_dept_id
            break

    # Not matched, return to the default department
    if not dept_id:
        return {
            "dept_id": "default",
            "dept_name": DEPARTMENTS["default"]["name"],
            "dept_contact": DEPARTMENTS["default"]["contact"],
            "is_auto": False,
            "confidence": 0,
            "matched_keyword": None
        }

    dept_info = DEPARTMENTS.get(dept_id, DEPARTMENTS["default"])

    return {
        "dept_id": dept_id,
        "dept_name": dept_info["name"],
        "dept_contact": dept_info.get("contact", "12345"),
        "is_auto": True,
        "confidence": 1.0,  # The precision configuration confidence is 1
        "matched_keyword": matched_keyword
    }


def classify_urgency(content: str) -> Dict[str, Any]:
    """
    Determine the urgency according to the content

    Args:
        content: Complaints/suggestions/consultation contents

    Returns:
        dict: {
            level: The degree of urgency (critical/urgent/normal),
            matched_keywords: List of matched keywords,
            deadline_hours: Estimated processing time limit (hours)
        }
    """
    if not content:
        return {
            "level": "normal",
            "matched_keywords": [],
            "deadline_hours": URGENCY_DEADLINE["normal"]
        }

    matched_keywords = []
    level = "normal"

    # Check by priority: critical > urgent > normal
    for urgency_level in ["critical", "urgent"]:
        keywords = URGENCY_KEYWORDS.get(urgency_level, [])
        for keyword in keywords:
            if keyword.lower() in content.lower():
                matched_keywords.append(keyword)
                if level == "normal":  # Only record the highest level
                    level = urgency_level

    return {
        "level": level,
        "matched_keywords": matched_keywords,
        "deadline_hours": URGENCY_DEADLINE[level]
    }


def generate_ticket_id() -> str:
    """
    Generate the work order number

    Format: GH-YYYYMMDD-NNNN

    Returns:
        str: Work order number
    """
    global TICKET_COUNTER
    TICKET_COUNTER += 1
    today = datetime.now().strftime("%Y%m%d")
    return f"GH-{today}-{TICKET_COUNTER:04d}"


def validate_phone(phone: str) -> bool:
    """
    Verify the format of the mobile phone number

    Args:
        phone: Mobile phone number string

    Returns:
        bool: Is it effective?
    """
    if not phone:
        return False
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def generate_verification_code() -> str:
    """
    Generate a 6-digit verification code

    Returns:
        str: 6 Digit verification code
    """
    return f"{random.randint(100000, 999999)}"


def calculate_deadline(urgency_level: str) -> str:
    """
    Calculate the deadline

    Args:
        urgency_level: The degree of urgency

    Returns:
        str: Cut-off time ISO format string
    """
    hours = URGENCY_DEADLINE.get(urgency_level, 72)
    deadline = datetime.now() + timedelta(hours=hours)
    return deadline.strftime("%Y-%m-%d %H:%M:%S")
