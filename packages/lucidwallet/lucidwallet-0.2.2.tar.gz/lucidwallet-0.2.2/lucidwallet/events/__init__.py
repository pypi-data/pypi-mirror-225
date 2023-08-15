from dataclasses import dataclass, field
from enum import Enum


@dataclass
class Event:
    class EventType(Enum):
        NewRows = "NewRows"
        ClearTable = "ClearTable"
        ScanningStart = "ScanningStart"
        ScanningEnd = "ScanningEnd"
        Scroll = "Scroll"

    type: EventType
    rows: list[tuple] = field(default_factory=list)
    scroll_height: float = 0.0
