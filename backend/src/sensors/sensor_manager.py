"""
Sensor Manager
Coordinates reading from all sensors
"""

from typing import Dict, List, Any
import asyncio
from .base_sensor import BaseSensor


class SensorManager:
    """Manages all sensors and coordinates readings"""

    def __init__(self, sensors: Dict[str, BaseSensor]):
        """
        Initialize sensor manager

        Args:
            sensors: Dictionary of sensor_id -> BaseSensor instance
        """
        self.sensors = sensors

    async def read_all(self) -> Dict[str, Any]:
        """
        Read all sensors concurrently

        Returns:
            Dictionary with readings from all sensors
        """
        readings = {}

        # Read all sensors concurrently using asyncio.gather
        tasks = [
            self._read_sensor_safe(sensor_id, sensor)
            for sensor_id, sensor in self.sensors.items()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        for sensor_id, result in zip(self.sensors.keys(), results):
            if isinstance(result, Exception):
                readings[sensor_id] = {"error": str(result), "status": "error"}
            else:
                readings[sensor_id] = result

        return readings

    async def _read_sensor_safe(
        self, sensor_id: str, sensor: BaseSensor
    ) -> Dict[str, Any]:
        """
        Read sensor with error handling

        Args:
            sensor_id: Sensor identifier
            sensor: Sensor instance

        Returns:
            Sensor reading or error dict
        """
        try:
            reading = await sensor.read()
            return {**reading, "sensor_id": sensor_id, "status": "ok"}
        except Exception as e:
            return {"error": str(e), "status": "error", "sensor_id": sensor_id}

    async def read_sensor(self, sensor_id: str) -> Dict[str, Any]:
        """
        Read a specific sensor

        Args:
            sensor_id: ID of sensor to read

        Returns:
            Sensor reading

        Raises:
            KeyError: If sensor_id not found
        """
        if sensor_id not in self.sensors:
            raise KeyError(f"Sensor '{sensor_id}' not found")

        return await self._read_sensor_safe(sensor_id, self.sensors[sensor_id])

    def get_all_status(self) -> List[Dict[str, Any]]:
        """
        Get status of all sensors

        Returns:
            List of sensor status dictionaries
        """
        return [sensor.get_status() for sensor in self.sensors.values()]

    def get_sensor_status(self, sensor_id: str) -> Dict[str, Any]:
        """
        Get status of specific sensor

        Args:
            sensor_id: ID of sensor

        Returns:
            Sensor status dictionary

        Raises:
            KeyError: If sensor_id not found
        """
        if sensor_id not in self.sensors:
            raise KeyError(f"Sensor '{sensor_id}' not found")

        return self.sensors[sensor_id].get_status()

    def get_sensor_ids(self) -> List[str]:
        """Get list of all sensor IDs"""
        return list(self.sensors.keys())

    async def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all sensors

        Returns:
            Dictionary of sensor_id -> initialization success
        """
        results = {}
        for sensor_id, sensor in self.sensors.items():
            try:
                results[sensor_id] = await sensor.initialize()
            except Exception as e:
                print(f"Error initializing {sensor_id}: {e}")
                results[sensor_id] = False

        return results
