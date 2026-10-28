"""
Data persistence layer

Provide the data persistence capability of the container terminal scheduling system, and store various data models based on JSON files.
All data models are Pydantic models, which support serialization and deserialization.
"""

import json
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from models import (
    Vessel,
    Berth,
    YardBlock,
    Container,
    Equipment,
    Task,
    GateChannel,
    Appointment,
    ExecutionRecord,
)


ModelType = TypeVar("ModelType", bound=BaseModel)


class DataStore:
    """
    Data persistence layer

    Lightweight data storage based on JSON files, responsible for loading and saving all kinds of data in the dock scheduling system:
    - Shipping (vessels.json)
    - Berth (berths.json)
    - Heap block (yard_blocks.json)
    - Container (containers.json)
    - Equipment (equipment.json)
    - Task (tasks.json)
    - Gate passage (gate_channels.json)
    - Make an appointment (appointments.json)
    - Execution record (execution_records.json)

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
    # Ship data
    # ------------------------------------------------------------------
    def load_vessels(self) -> list[Vessel]:
        """Load the list of ship data"""
        return self._load_list("vessels.json", Vessel, "vessels")

    def save_vessels(self, vessels: list[Vessel]) -> None:
        """Save the list of ship data"""
        self._save_list("vessels.json", vessels, "vessels")

    # ------------------------------------------------------------------
    # Parking data
    # ------------------------------------------------------------------
    def load_berths(self) -> list[Berth]:
        """Load the list of berth data"""
        return self._load_list("berths.json", Berth, "berths")

    def save_berths(self, berths: list[Berth]) -> None:
        """Save the list of berth data"""
        self._save_list("berths.json", berths, "berths")

    # ------------------------------------------------------------------
    # Block data of the warehouse
    # ------------------------------------------------------------------
    def load_yard_blocks(self) -> list[YardBlock]:
        """Load the stack block data list"""
        return self._load_list("yard_blocks.json", YardBlock, "yard_blocks")

    def save_yard_blocks(self, blocks: list[YardBlock]) -> None:
        """Save the data list of the warehouse block"""
        self._save_list("yard_blocks.json", blocks, "yard_blocks")

    # ------------------------------------------------------------------
    # Container data
    # ------------------------------------------------------------------
    def load_containers(self) -> list[Container]:
        """Load the container data list"""
        return self._load_list("containers.json", Container, "containers")

    def save_containers(self, containers: list[Container]) -> None:
        """Save the container data list"""
        self._save_list("containers.json", containers, "containers")

    # ------------------------------------------------------------------
    # Device data
    # ------------------------------------------------------------------
    def load_equipment(self) -> list[Equipment]:
        """Load the device data list"""
        return self._load_list("equipment.json", Equipment, "equipment")

    def save_equipment(self, equipment: list[Equipment]) -> None:
        """Save the list of device data"""
        self._save_list("equipment.json", equipment, "equipment")

    # ------------------------------------------------------------------
    # Task data
    # ------------------------------------------------------------------
    def load_tasks(self) -> list[Task]:
        """Load the task data list"""
        return self._load_list("tasks.json", Task, "tasks")

    def save_tasks(self, tasks: list[Task]) -> None:
        """Save the list of task data"""
        self._save_list("tasks.json", tasks, "tasks")

    # ------------------------------------------------------------------
    # Gate channel data
    # ------------------------------------------------------------------
    def load_gate_channels(self) -> list[GateChannel]:
        """Load the gate channel data list"""
        return self._load_list("gate_channels.json", GateChannel, "gate_channels")

    def save_gate_channels(self, channels: list[GateChannel]) -> None:
        """Save the list of gate channel data"""
        self._save_list("gate_channels.json", channels, "gate_channels")

    # ------------------------------------------------------------------
    # Appointment data
    # ------------------------------------------------------------------
    def load_appointments(self) -> list[Appointment]:
        """Load the list of appointment data"""
        return self._load_list("appointments.json", Appointment, "appointments")

    def save_appointments(self, appointments: list[Appointment]) -> None:
        """Save the reservation data list"""
        self._save_list("appointments.json", appointments, "appointments")

    # ------------------------------------------------------------------
    # Execution record data
    # ------------------------------------------------------------------
    def load_execution_records(self) -> list[ExecutionRecord]:
        """Load the list of execution record data"""
        return self._load_list(
            "execution_records.json", ExecutionRecord, "execution_records"
        )

    def save_execution_records(self, records: list[ExecutionRecord]) -> None:
        """Save the list of execution record data"""
        self._save_list(
            "execution_records.json", records, "execution_records"
        )


__all__ = ["DataStore"]
