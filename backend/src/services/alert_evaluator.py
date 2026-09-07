"""
Threshold evaluation and alert state machine.

Severity bands mirror the frontend SensorCard:
    NORMAL   comfortably inside [min, max]
    WARNING  inside the range but within `buffer` of either edge
    DANGER   outside [min, max]

Logic, no IO needed for this class
"""

from enum import Enum
from dataclasses import dataclass

RANK = {"normal": 0, "warning": 1, "danger": 2}

class AlertState(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    DANGER = "danger"

METRIC_BOUNDS = {
    "temperature":  ("temp_min", "temp_max"),
    "humidity":     ("humidity_min", "humidity_max"),
    "ph":           ("ph_min", "ph_max")
}

@dataclass
class Transition:
    sensor_type: str
    metric: str
    from_state: AlertState
    to_state: AlertState
    value: float
    threshold_min: float
    threshold_max: float

    @property
    def should_notify(self) -> bool:
        """Only push notification on switching to DANGER"""
        return self.to_state == AlertState.DANGER

class AlertEvaluator:
    def __init__ (
        self,
        warning_buffer_pct: float = 0.10, #same behavior from SensorCard.jsx
        hysteresis_pct: float = 0.02,
        confirm_readings: int = 2,
    ):
        self.warning_buffer_pct = warning_buffer_pct
        self.hysteresis_pct = hysteresis_pct
        self.confirm_readings = confirm_readings

    def _raw(self, value, lo, hi, buf) -> AlertState:
        """Severity ignoring history (same behavior as SensorCard.jsx)"""
        if value < lo or value > hi:
            return AlertState.DANGER
        if value <= lo + buf or value >= hi - buf:
            return AlertState.WARNING
        return AlertState.NORMAL

    def classify(self, value, lo, hi, current: AlertState) -> AlertState:
        band = (hi-lo) or 1.0
        # Set cap of buffer so i cannot swallow whole range on a narrow band
        buf = min(band * self.warning_buffer_pct, band * 0.45)
        pad = self.hysteresis_pct * band

        raw = self._raw(value, lo, hi, buf)

        # Require clearing boundary by "pad" before doing any downgrading
        #   ,or a value will sit on the line and dont switch between state
        if RANK[raw] < RANK[current]:
            if current == AlertState.DANGER and not (lo + pad <= value <= hi - pad):
                return AlertState.DANGER
        if RANK[raw] < RANK[AlertState.WARNING]:
            if not (lo + buf + pad <= value <= hi - buf - pad):
                return  AlertState.WARNING

    
