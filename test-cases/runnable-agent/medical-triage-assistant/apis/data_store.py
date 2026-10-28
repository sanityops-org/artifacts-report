"""Data persistence: JSON reading and writing of built-in analog data.

All data is in the form of "top-level object + single array key", such as
``{"departments": [...]}``；Read and write uniformly go Pydantic's
``model_validate`` / ``model_dump(mode="json")``。
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Type, TypeVar

from pydantic import BaseModel

from models.appointment import Appointment
from models.department import Department
from models.doctor import Doctor
from models.slot import Slot

ModelType = TypeVar("ModelType", bound=BaseModel)


class DataStore:
    """JSON Data storage.

    Attributes:
        data_dir: Data catalog
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure the existence of the data directory"""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _read_payload(self, filename: str) -> Dict[str, Any]:
        """Read JSON top-level object; return an empty object when the file does not exist"""
        path = self.data_dir / filename
        if not path.exists():
            return {}
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"{filename} The structure is illegal: the top layer must be a JSON object")
        return raw

    def _extract_list(self, filename: str, payload: Dict[str, Any], key: str) -> List[Any]:
        """Take out the array key; the missing key returns an empty list, and the type is wrong. ValueError"""
        items = payload.get(key)
        if items is None:
            return []
        if not isinstance(items, list):
            raise ValueError(f"{filename} Structure is illegal: {key} must be an array")
        return items

    def _load_list(
        self, filename: str, model_class: Type[ModelType], key: str
    ) -> List[ModelType]:
        """Read and verify as a model list"""
        items = self._extract_list(filename, self._read_payload(filename), key)
        return [model_class.model_validate(item) for item in items]

    def _load_raw_list(self, filename: str, key: str) -> List[Dict[str, Any]]:
        """Read the original dict list (rule table / mapping table does not follow the model)"""
        return self._extract_list(filename, self._read_payload(filename), key)

    def _save_list(self, filename: str, items: List[BaseModel], key: str) -> None:
        """Write disk: UTF-8, do not escape non-ASCII characters, indent 2; write temporary files first and then replace them atomically (to avoid semi-write damage)"""
        payload = {key: [item.model_dump(mode="json") for item in items]}
        path = self.data_dir / filename
        tmp_path = path.with_name(path.name + ".tmp")
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        os.replace(tmp_path, path)

    # --- Departments and offices ---

    def load_departments(self) -> List[Department]:
        """Read the department table"""
        return self._load_list("departments.json", Department, "departments")

    def save_departments(self, items: List[Department]) -> None:
        """Save the department table"""
        self._save_list("departments.json", items, "departments")

    # --- Doctor ---

    def load_doctors(self) -> List[Doctor]:
        """Read the doctor's list"""
        return self._load_list("doctors.json", Doctor, "doctors")

    def save_doctors(self, items: List[Doctor]) -> None:
        """Save the doctor's list"""
        self._save_list("doctors.json", items, "doctors")

    # --- Number source ---

    def load_slots(self) -> List[Slot]:
        """Read the source table of the number"""
        return self._load_list("slots.json", Slot, "slots")

    def save_slots(self, items: List[Slot]) -> None:
        """Save the source table"""
        self._save_list("slots.json", items, "slots")

    # --- Registration record ---

    def load_appointments(self) -> List[Appointment]:
        """Read the registration record form"""
        return self._load_list("appointments.json", Appointment, "appointments")

    def save_appointments(self, items: List[Appointment]) -> None:
        """Save the registered record form"""
        self._save_list("appointments.json", items, "appointments")

    # --- Rules and mapping (original dict, no modeling)---

    def load_red_flag_rules(self) -> List[Dict[str, Any]]:
        """Read the red flag rule table"""
        return self._load_raw_list("red_flag_rules.json", "rules")

    def load_symptom_map(self) -> List[Dict[str, Any]]:
        """Read symptoms → department mapping table"""
        return self._load_raw_list("symptom_department_map.json", "mappings")


__all__ = ["DataStore"]
