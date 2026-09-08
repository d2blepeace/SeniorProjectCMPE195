"""
Sensor Factory
Create sensor instances, choose real sensor over mock sensors if it is available
"""

from typing import Dict
from .base_sensor import BaseSensor
from .sensor_manager import SensorManager
from importlib import import_module
from ..utils.logger import logger

# Sensors
SENSOR_SPECS = {
    "bme280": { 
        "real_module": ".hardware.bme280", "real_class": "BME280Real",
        "mock_module": ".mock.bme280_mock", "mock_class": "BME280Mock",},

    "bme680": {
        "real_module": ".hardware.bme680", "real_class": "BME680Real",
        "mock_module": ".mock.bme680_mock", "mock_class": "BME680Mock",
    },

    "ph": {
        "real_module": ".hardware.ph", "real_class": "PHReal",
        "mock_module": ".mock.ph_mock", "mock_class": "PHMock",
    },
}
class SensorFactory:
    """Factory for creating sensor instances"""

    @staticmethod
    def _instantiate(module_path: str, class_name: str) -> BaseSensor:
        """Import a sensor module relative to this package and construct it."""
        module = import_module(module_path, package=__package__)
        return getattr(module, class_name)()
    
    @staticmethod
    def _create_one(sensor_id: str, spec: dict, use_mock: bool) -> BaseSensor:
        """
        Create a single sensor, falling back to mock if the real one
        can't be imported, constructed, or initialized.
        """
        if not use_mock:
            try:
                sensor = SensorFactory._instantiate(
                    spec["real_module"], spec["real_class"]
                )
                # PHReal (and others) may construct successfully but report
                # failed init when the device or its library is missing.
                # Treat that as unavailable rather than silently reporting REAL.
                if not getattr(sensor, "is_initialized", True):
                    raise RuntimeError("sensor reported failed initialization")

                sensor.is_mock = False
                logger.success(f" Real sensor ready: {sensor_id}")
                return sensor

            except Exception as e:
                # Exception, not ImportError: also catches a missing device
                # on the I2C bus, which surfaces at construction time.
                logger.warning(f"  {sensor_id}: real sensor unavailable ({e}) — using MOCK")

        sensor = SensorFactory._instantiate(spec["mock_module"], spec["mock_class"])
        sensor.is_mock = True
        return sensor
    
    @staticmethod
    def create_sensors(use_mock: bool = True) -> Dict[str, BaseSensor]:
        """
        Create sensor instances

        Args:
            use_mock: If True, create mock sensors; if False, create real hardware sensors

        Returns:
            Dictionary of sensor_id -> BaseSensor instance
        """
        sensors = {
            sensor_id: SensorFactory._create_one(sensor_id, spec, use_mock)
            for sensor_id, spec in SENSOR_SPECS.items()
        }

        # Summary line — this is what you check at startup and during a demo.
        real = [sid for sid, s in sensors.items() if not s.is_mock]
        mock = [sid for sid, s in sensors.items() if s.is_mock]
        logger.info(f"Sensor modes - REAL: {real or 'none'} | MOCK: {mock or 'none'}")

        return sensors

    @staticmethod
    def get_sensor_manager(use_mock: bool = True) -> SensorManager:
        """Create a SensorManager with appropriate sensors"""
        return SensorManager(SensorFactory.create_sensors(use_mock))

    @staticmethod
    def create_hybrid_sensors(
        mock_sensors: list = None, real_sensors: list = None
    ) -> Dict[str, BaseSensor]:
        """
        Force specific sensors to mock or real. Mainly useful for tests.

        Anything not named in either list is omitted.

        Example:
            SensorFactory.create_hybrid_sensors(
                mock_sensors=["ph"], real_sensors=["bme280", "bme680"]
            )
        """
        mock_sensors = mock_sensors or []
        real_sensors = real_sensors or []

        return {
            sid: SensorFactory._create_one(
                sid, SENSOR_SPECS[sid], use_mock=(sid in mock_sensors)
            )
            for sid in [*mock_sensors, *real_sensors]
            if sid in SENSOR_SPECS
        }
