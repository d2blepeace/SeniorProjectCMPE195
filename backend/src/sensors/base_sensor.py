"""
Base sensor abstract class
All sensors (mock and real) inherit from this
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseSensor(ABC):
    """Abstract base class for all sensors"""

    def __init__(self, sensor_id: str, name: str):
        """
        Initialize sensor

        Args:
            sensor_id: Unique identifier for sensor
            name: Human-readable sensor name
        """
        self.sensor_id = sensor_id
        self.name = name
        self.last_reading: Optional[Dict[str, Any]] = None
        self.last_reading_time: Optional[str] = None
        self.is_initialized = True

    @abstractmethod
    async def read(self) -> Dict[str, Any]:
        """
        Read sensor data
        Must be implemented by subclasses

        Returns:
            Dictionary containing sensor readings
        """
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get sensor health status

        Returns:
            Dictionary with sensor status information
        """
        return {
            "sensor_id": self.sensor_id,
            "name": self.name,
            "last_reading": self.last_reading,
            "last_reading_time": self.last_reading_time,
            "is_initialized": self.is_initialized,
            "is_healthy": self.last_reading is not None,
        }

    async def initialize(self) -> bool:
        """
        Initialize sensor hardware (override if needed)

        Returns:
            True if initialization successful
        """
        self.is_initialized = True
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.sensor_id}, name={self.name})>"
