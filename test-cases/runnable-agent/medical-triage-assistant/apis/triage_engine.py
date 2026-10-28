"""Triage engine: Red flag symptom screening and candidate departments converge.

Pure rule implementation, zero external dependence; rule tables and mapping tables are injected by the caller, which is convenient for testing and replacement.
"""

import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from models.department import Department
from models.enums import RedFlagAction, RedFlagLevel

FALLBACK_DEPARTMENT_ID = "dept_general_internal"
PEDIATRICS_DEPARTMENT_ID = "dept_pediatrics"
PEDIATRICS_AGE_LIMIT = 14


def normalize(text: Optional[str]) -> str:
    """Normalize text for case-insensitive English keyword matching."""
    if not text:
        return ""
    chars: List[str] = []
    for char in text:
        code = ord(char)
        if code == 0x3000:
            char = " "
        elif 0xFF01 <= code <= 0xFF5E:
            char = chr(code - 0xFEE0)
        chars.append(char)
    normalized = re.sub(r"\s+", " ", "".join(chars)).strip()
    normalized = re.sub(r"\s+([,.!?;:])", r"\1", normalized)
    return normalized.lower()


class RedFlagResult(BaseModel):
    """Red flag screening results.

    Attributes:
        hit: Whether to hit the danger signal
        rule_id: The rule number of the hit
        name: Hit rule name
        level: Severity
        action: Disposal action
        advice: Guide copy for patients
        matched_keywords: The key words that hit
    """

    hit: bool = Field(..., description="Whether to hit the danger signal")
    rule_id: Optional[str] = Field(None, description="The rule number of the hit")
    name: Optional[str] = Field(None, description="Hit rule name")
    level: Optional[RedFlagLevel] = Field(None, description="Severity")
    action: Optional[RedFlagAction] = Field(None, description="Disposal action")
    advice: Optional[str] = Field(None, description="Guide copy for patients")
    matched_keywords: List[str] = Field(
        default_factory=list, description="The key words that hit"
    )


def check_red_flags(
    text: str,
    rules: List[Dict[str, Any]],
    symptoms: Optional[List[str]] = None,
) -> RedFlagResult:
    """Red flag symptom screening (compulsory gate).

    Make a keyword substring match between the patient's description text and the extracted symptom words. When you hit more than one
    emergency Priority, take the order of the rule table at the same level - to ensure that the results are determined and reproduced.

    Args:
        text: The original description of the patient
        rules: Red Flag Rules Table
        symptoms: Optional normalization symptom words

    Returns:
        RedFlagResult；When it is not hit, hit is False, action is None
    """
    haystack = normalize(text)
    for symptom in symptoms or []:
        haystack += normalize(str(symptom))

    if not haystack:
        return RedFlagResult(hit=False)

    hits: List[tuple] = []
    for index, rule in enumerate(rules):
        matched = [
            keyword
            for keyword in rule.get("keywords", []) or []
            if normalize(keyword) and normalize(keyword) in haystack
        ]
        if matched:
            hits.append((index, RedFlagLevel(rule["level"]), rule, matched))

    if not hits:
        return RedFlagResult(hit=False)

    hits.sort(
        key=lambda item: (0 if item[1] == RedFlagLevel.EMERGENCY else 1, item[0])
    )
    _, level, rule, matched = hits[0]

    return RedFlagResult(
        hit=True,
        rule_id=rule["rule_id"],
        name=rule["name"],
        level=level,
        action=RedFlagAction(rule["action"]),
        advice=rule["advice"],
        matched_keywords=matched,
    )


class Candidate(BaseModel):
    """Candidate department.

    Attributes:
        department_id: Department identification
        name: English display name of the department
        score: Rules cumulative score
        matched_symptoms: The standard symptom words of the hit
    """

    department_id: str = Field(..., description="Department identification")
    name: str = Field(..., description="English display name of the department")
    score: int = Field(..., description="Rules cumulative score")
    matched_symptoms: List[str] = Field(
        default_factory=list, description="The standard symptom words of the hit"
    )


class ShortlistResult(BaseModel):
    """Convergence results of candidate departments.

    Attributes:
        candidates: Candidate departments (up to max_candidates, descending order by score)
        fallback_department: When there is no hit, the bottom department; when there is a candidate, it is None
        age_rule_applied: Does it trigger the pediatric age rule?
        note: Behavioral tips for the model
    """

    candidates: List[Candidate] = Field(
        default_factory=list, description="Candidate department"
    )
    fallback_department: Optional[str] = Field(
        None, description="The logo of the bottom department when there is no hit"
    )
    age_rule_applied: bool = Field(False, description="Does it trigger the pediatric age rule?")
    note: str = Field("", description="Behavioral tips for the model")


def _match_mapping(symptom: str, mapping: Dict[str, Any]) -> bool:
    """Whether the patient's symptom word hits the mapping (the mapping word appears as a substring in the patient's symptom word)"""
    for keyword in [mapping.get("symptom", "")] + list(mapping.get("aliases", []) or []):
        needle = normalize(keyword)
        if needle and needle in symptom:
            return True
    return False


def shortlist_departments(
    symptoms: List[str],
    mappings: List[Dict[str, Any]],
    departments: List[Department],
    age: Optional[int] = None,
    max_candidates: int = 3,
) -> ShortlistResult:
    """Converge the symptoms into limited candidate departments (up to 3).

    Scoring rule: the weight of the hit mapping item is accumulated to each section in the department;
    Sort by score in descending order, and score in ascending order by department_id. Compulsory convergence to pediatrics when under the age of 14.

    Args:
        symptoms: List of normalized symptom words
        mappings: Symptoms → Department Mapping Table
        departments: Department table
        age: The age of the patient, unknown time transmission None
        max_candidates: Maximum number of candidates

    Returns:
        ShortlistResult
    """
    dept_names = {dept.department_id: dept.name for dept in departments}

    scores: Dict[str, int] = {}
    matched: Dict[str, List[str]] = {}

    for raw in symptoms or []:
        symptom = normalize(str(raw))
        if not symptom:
            continue
        for mapping in mappings:
            if not _match_mapping(symptom, mapping):
                continue
            weight = int(mapping.get("weight", 0))
            symptom_name = mapping.get("symptom", "")
            for dept_id in mapping.get("departments", []) or []:
                if dept_id not in dept_names:
                    continue
                scores[dept_id] = scores.get(dept_id, 0) + weight
                bucket = matched.setdefault(dept_id, [])
                if symptom_name not in bucket:
                    bucket.append(symptom_name)

    if age is not None and age < PEDIATRICS_AGE_LIMIT and PEDIATRICS_DEPARTMENT_ID in dept_names:
        pediatrics = Candidate(
            department_id=PEDIATRICS_DEPARTMENT_ID,
            name=dept_names[PEDIATRICS_DEPARTMENT_ID],
            score=scores.get(PEDIATRICS_DEPARTMENT_ID, 0),
            matched_symptoms=matched.get(PEDIATRICS_DEPARTMENT_ID, []),
        )
        return ShortlistResult(
            candidates=[pediatrics],
            fallback_department=None,
            age_rule_applied=True,
            note="Underage patients (under 14 years old) are first diagnosed by pediatrics, and candidates have been converged to pediatrics.",
        )

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    candidates = [
        Candidate(
            department_id=dept_id,
            name=dept_names[dept_id],
            score=score,
            matched_symptoms=matched.get(dept_id, []),
        )
        for dept_id, score in ranked[:max_candidates]
    ]

    if not candidates:
        fallback = FALLBACK_DEPARTMENT_ID if FALLBACK_DEPARTMENT_ID in dept_names else None
        return ShortlistResult(
            candidates=[],
            fallback_department=fallback,
            age_rule_applied=False,
            note="At present, the information provided is not enough to judge the department. It is recommended to go to the internal medicine department first, and the doctor will make further judgment.",
        )

    return ShortlistResult(
        candidates=candidates,
        fallback_department=None,
        age_rule_applied=False,
        note="Please select 1 department from the candidates to recommend to the patient and explain the basis for judgment.",
    )
