#!/usr/bin/env python3
"""_labels: Enumeration to the shared mapping of display labels (non-tool module, scanner skips `_` prefix file)."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.enums import DoctorTitle

DOCTOR_TITLE_LABELS = {
    DoctorTitle.CHIEF: "Chief Physician",
    DoctorTitle.ASSOCIATE_CHIEF: "Deputy Chief Physician",
    DoctorTitle.ATTENDING: "Attending Physician",
}
