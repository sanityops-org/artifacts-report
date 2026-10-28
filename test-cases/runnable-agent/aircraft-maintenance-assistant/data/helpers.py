#!/usr/bin/env python3
"""
Auxiliary function

Provide life calculation, time control rules, conformity determination and other auxiliary functions.
"""

from typing import Dict, Any, Optional


def calc_remaining_life(
    component: Dict[str, Any],
    hours_since_install: int,
    cycles_since_install: int
) -> Dict[str, Any]:
    """
    Calculate the remaining life of the life piece

    Args:
        component: Component definition (need to include category, total_life_hours, total_life_cycles）
        hours_since_install: Operating hours after installation
        cycles_since_install: The number of cycles after installation

    Returns:
        dict: remaining_hours, remaining_cycles, alert_level
    """
    total_hours = component.get("total_life_hours", 0)
    total_cycles = component.get("total_life_cycles", 0)

    remaining_hours = max(0, total_hours - hours_since_install)
    remaining_cycles = max(0, total_cycles - cycles_since_install)

    # Calculate the residual ratio (take the smaller values in the hour and cycle)
    if total_hours > 0 and total_cycles > 0:
        ratio_hours = remaining_hours / total_hours
        ratio_cycles = remaining_cycles / total_cycles
        ratio = min(ratio_hours, ratio_cycles)
    elif total_hours > 0:
        ratio = remaining_hours / total_hours
    elif total_cycles > 0:
        ratio = remaining_cycles / total_cycles
    else:
        ratio = 1.0

    # Determine the level of early warning
    if remaining_hours <= 0 or remaining_cycles <= 0:
        alert_level = "exceeded"
    elif ratio < 0.1:  # < 10%
        alert_level = "critical"
    elif ratio < 0.2:  # < 20%
        alert_level = "warning"
    else:
        alert_level = "ok"

    return {
        "remaining_hours": remaining_hours,
        "remaining_cycles": remaining_cycles,
        "alert_level": alert_level,
        "remaining_ratio": round(ratio, 3),
    }


def check_time_control_limit(
    tci: Dict[str, Any],
    current_value: float
) -> Dict[str, Any]:
    """
    Control restriction status when checking

    Args:
        tci: Time control definition (need to include limit_type, limit_value, alert_threshold）
        current_value: Current cumulative value

    Returns:
        dict: status, remaining, ratio
    """
    limit_value = tci.get("limit_value", 0)
    alert_threshold = tci.get("alert_threshold", 0.8)

    remaining = limit_value - current_value
    ratio = current_value / limit_value if limit_value > 0 else 0

    if current_value >= limit_value:
        status = "exceeded"
    elif ratio >= alert_threshold:
        status = "warning"
    else:
        status = "ok"

    return {
        "status": status,
        "remaining": max(0, remaining),
        "current_value": current_value,
        "limit_value": limit_value,
        "ratio": round(ratio, 3),
    }


def evaluate_ad_compliance(
    ad: Dict[str, Any],
    compliance_record: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluate AD airworthiness compliance

    Args:
        ad: AD Definition
        compliance_record: The AD execution record of the aircraft (may be None）

    Returns:
        dict: status, action_required, deadline Equal
    """
    ad_status = ad.get("status", "open")

    # It has been replaced
    if ad_status == "superseded":
        return {
            "status": "superseded",
            "action_required": False,
            "superseded_by": ad.get("superseded_by"),
            "message": f"This AD has been replaced by {ad.get('superseded_by')}",
        }

    # Executed
    if compliance_record and compliance_record.get("status") == "complied":
        return {
            "status": "complied",
            "action_required": False,
            "complied_date": compliance_record.get("date"),
            "message": "AD Executed",
        }

    # Not executed
    return {
        "status": "open",
        "action_required": True,
        "effective_date": ad.get("effective_date"),
        "deadline_days": ad.get("deadline_days"),
        "compliance": ad.get("compliance"),
        "message": "AD It has not been implemented, and measures need to be taken.",
    }


def assess_defect_impact(defect: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate the impact of defects on airworthiness

    Args:
        defect: Definition of defect

    Returns:
        dict: airworthy, requires_action, mel_controlled Equal
    """
    severity = defect.get("severity", "low")
    mel_reference = defect.get("mel_reference")
    mel_deadline = defect.get("mel_deadline")

    # Critical Level affects airworthiness
    if severity == "critical":
        return {
            "airworthy": False,
            "requires_action": True,
            "mel_controlled": False,
            "impact": "grounding",
            "message": "Serious defects need to be dealt with immediately.",
        }

    # MEL Defects in control
    if mel_reference:
        return {
            "airworthy": True,
            "requires_action": False,  # It is not mandatory at this stage.
            "mel_controlled": True,
            "mel_reference": mel_reference,
            "mel_deadline": mel_deadline,
            "impact": "mel",
            "message": f"The defect has been included in MEL control. ({mel_reference})",
        }

    # Minor defects
    return {
        "airworthy": True,
        "requires_action": False,
        "mel_controlled": False,
        "impact": "monitor",
        "message": "Minor defects can continue to be monitored.",
    }
