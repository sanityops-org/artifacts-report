"""
Data persistence layer

Provide the data persistence capability of the energy management system, and store various data models based on JSON files.
All data models are Pydantic models, which support serialization and deserialization.
"""

import json
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from models.facility import Facility
from models.enums import FacilityType


ModelType = TypeVar("ModelType", bound=BaseModel)


class DataStore:
    """
    Data persistence layer

    Lightweight data storage based on JSON files, responsible for loading and saving various data of the energy management system:
    - Facilities (facilities.json)
    - Equipment (equipment.json)
    - Consumption record (consumption_patterns.json)
    - Efficiency measures (efficiency_measures.json)
    - Renewable energy options (renewable_options.json)

    Attributes:
        data_dir: Data file storage directory, the default is "data"
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize DataStore

        Args:
            data_dir: The data file storage directory defaults to "data" (related to the current working directory).
                      When the directory does not exist, it will be automatically created when it is saved for the first time.
        """
        self.data_dir = data_dir

    def _ensure_data_dir(self) -> Path:
        """Make sure that the data directory exists and return the directory path."""
        data_path = Path(self.data_dir)
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path

    def _load_list(
        self, filename: str, model_class: Type[ModelType], key: str
    ) -> list[ModelType]:
        """
        General list data loading method

        Read the data from the JSON file and deserialize it into a list of model objects.

        Args:
            filename: Data file name (relationd to the data directory)
            model_class: PydanticModel class, used for deserialization
            key: JSONThe key name containing the list data in the file

        Returns:
            List of model objects. Return an empty list when the file does not exist or the data is empty.

        Raises:
            ValueError: Throw out when the data format is illegal or the verification fails
        """
        file_path = Path(self.data_dir) / filename

        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Failed to read the data file: {file_path} ({e})") from e

        if not raw:
            return []

        items_raw = raw.get(key)
        if items_raw is None:
            return []

        if not isinstance(items_raw, list):
            raise ValueError(
                f"The value of the key '{key}' in the data file {file_path} must be a list."
            )

        items: list[ModelType] = []
        for index, item_data in enumerate(items_raw):
            try:
                items.append(model_class.model_validate(item_data))
            except ValidationError as e:
                raise ValueError(
                    f"The data verification of the {index} in the data file {file_path} failed: {e}"
                ) from e

        return items

    def _load_raw(self, filename: str) -> list:
        """
        Load the original JSON list data (no model verification required)

        Args:
            filename: Data file name

        Returns:
            List of raw data
        """
        file_path = Path(self.data_dir) / filename

        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"Failed to read the data file: {file_path} ({e})") from e

        # Support packaging format {"key": [...]} Or direct list format [...]
        if isinstance(raw, list):
            return raw

        # Try to find the first list value
        for key, value in raw.items():
            if isinstance(value, list):
                return value

        return []

    def _save_list(
        self,
        filename: str,
        items: list[ModelType],
        key: str,
    ) -> None:
        """
        General list data saving method

        Serialize the list of model objects and write it to the JSON file.

        Args:
            filename: Data file name (relationd to the data directory)
            items: List of model objects to be saved
            key: The key name used when writing JSON files

        Raises:
            ValueError: Throw out when the object serialization fails
        """
        data_path = self._ensure_data_dir()
        file_path = data_path / filename

        try:
            items_raw = [item.model_dump(mode="json") for item in items]
        except AttributeError as e:
            raise ValueError(f"Failed to save data, object serialization error: {e}") from e

        payload = {key: items_raw}

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise ValueError(f"Failed to write the data file: {file_path} ({e})") from e

    # ------------------------------------------------------------------
    # Facility data
    # ------------------------------------------------------------------
    def load_facilities(self) -> list:
        """Load the list of facility data"""
        return self._load_raw("facilities.json")

    def save_facilities(self, facilities: list) -> None:
        """Save the list of facility data"""
        self._save_list("facilities.json", facilities, "facilities")

    # ------------------------------------------------------------------
    # Device data
    # ------------------------------------------------------------------
    def load_equipment(self) -> list:
        """Load the device data list"""
        return self._load_raw("equipment.json")

    def save_equipment(self, equipment: list) -> None:
        """Save the list of device data"""
        self._save_list("equipment.json", equipment, "equipment")

    # ------------------------------------------------------------------
    # Consumption record data
    # ------------------------------------------------------------------
    def load_consumption_patterns(self) -> list:
        """Load the consumption record data list"""
        return self._load_raw("consumption_patterns.json")

    def save_consumption_patterns(self, patterns: list) -> None:
        """Save the list of consumption record data"""
        self._save_list("consumption_patterns.json", patterns, "consumption_patterns")

    # ------------------------------------------------------------------
    # Data on efficiency measures
    # ------------------------------------------------------------------
    def load_efficiency_measures(self) -> list:
        """Load the data list of efficiency measures"""
        return self._load_raw("efficiency_measures.json")

    def save_efficiency_measures(self, measures: list) -> None:
        """Save the data list of efficiency measures"""
        self._save_list("efficiency_measures.json", measures, "efficiency_measures")

    # ------------------------------------------------------------------
    # Renewable energy option data
    # ------------------------------------------------------------------
    def load_renewable_options(self) -> list:
        """Load the data list of renewable energy options"""
        return self._load_raw("renewable_options.json")

    def save_renewable_options(self, options: list) -> None:
        """Save the data list of renewable energy options"""
        self._save_list("renewable_options.json", options, "renewable_options")


__all__ = ["DataStore"]
