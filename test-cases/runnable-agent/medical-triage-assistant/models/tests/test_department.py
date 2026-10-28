"""Department model test."""

import pytest
from pydantic import ValidationError

from models.department import Department
from models.enums import DepartmentCategory


def _department(**overrides) -> dict:
    data = {
        "department_id": "dept_neurology",
        "name": "Neurology",
        "category": "internal",
        "description": "Diagnosis and treatment of headache, dizziness, cerebrovascular disease and other neurological diseases.",
        "location": "Area C, 4th Floor, Outpatient Building",
        "preparation": ["Carry past medical records"],
    }
    data.update(overrides)
    return data


def test_valid_department():
    """The legal department can be constructed"""
    dept = Department.model_validate(_department())

    assert dept.department_id == "dept_neurology"
    assert dept.name == "Neurology"
    assert dept.category == DepartmentCategory.INTERNAL
    assert dept.preparation == ["Carry past medical records"]


def test_preparation_defaults_to_empty_list():
    """preparation Can be omitted, the default is an empty list"""
    data = _department()
    data.pop("preparation")

    assert Department.model_validate(data).preparation == []


def test_department_id_is_normalized():
    """department_id Unify the blank and convert it to lowercase."""
    dept = Department.model_validate(_department(department_id=" Dept_Neurology "))

    assert dept.department_id == "dept_neurology"


@pytest.mark.parametrize("bad_id", ["neuro", "dept_", "dept-Nerve", "DEPTBAD"])
def test_invalid_department_id_rejected(bad_id):
    """Illegal department_id was rejected"""
    with pytest.raises(ValidationError):
        Department.model_validate(_department(department_id=bad_id))


def test_invalid_category_rejected():
    """Illegal categories are rejected."""
    with pytest.raises(ValidationError):
        Department.model_validate(_department(category="unknown"))


def test_dump_is_json_serializable():
    """model_dump(mode="json") The output can be directly dropped."""
    dumped = Department.model_validate(_department()).model_dump(mode="json")

    assert dumped["category"] == "internal"
    assert isinstance(dumped["preparation"], list)
