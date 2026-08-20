"""
Sensor Factory
Creates mock or real sensors based on configuration
"""

from typing import Dict
from .base_sensor import BaseSensor
from .sensor_manager import SensorManager


class SensorFactory:
    """Factory for creating sensor instances"""

    @staticmethod
    def create_sensors(use_mock: bool = True) -> Dict[str, BaseSensor]:
        """
        Create sensor instances

        Args:
            use_mock: If True, create mock sensors; if False, create real hardware sensors

        Returns:
            Dictionary of sensor_id -> BaseSensor instance
        """
        if use_mock:
            # Import mock sensors
            from .mock.bme280_mock import BME280Mock
            from .mock.bme680_mock import BME680Mock
            from .mock.ph_mock import PHMock

            print("🔧 Using MOCK sensors (development mode)")

            return {"bme280": BME280Mock(), "bme680": BME680Mock(), "ph": PHMock()}
        else:
            # Import real hardware sensors
            try:
                from .hardware.bme280 import BME280Real
                from .hardware.bme680 import BME680Real
                from .hardware.ph import PHReal

                print("⚡ Using REAL hardware sensors (production mode)")

                return {"bme280": BME280Real(), "bme680": BME680Real(), "ph": PHReal()}
            except ImportError as e:
                print(f"❌ Error importing hardware sensors: {e}")
                print("⚠️  Falling back to mock sensors")
                # Fallback to mock sensors if hardware not available
                from .mock.bme280_mock import BME280Mock
                from .mock.bme680_mock import BME680Mock
                from .mock.ph_mock import PHMock

                return {"bme280": BME280Mock(), "bme680": BME680Mock(), "ph": PHMock()}

    @staticmethod
    def get_sensor_manager(use_mock: bool = True) -> SensorManager:
        """
        Create a SensorManager with appropriate sensors

        Args:
            use_mock: If True, use mock sensors; if False, use real sensors

        Returns:
            SensorManager instance
        """
        sensors = SensorFactory.create_sensors(use_mock)
        return SensorManager(sensors)

    @staticmethod
    def create_hybrid_sensors(
        mock_sensors: list = None, real_sensors: list = None
    ) -> Dict[str, BaseSensor]:
        """
        Create a mix of mock and real sensors (useful for testing)

        Args:
            mock_sensors: List of sensor IDs to use mock versions
            real_sensors: List of sensor IDs to use real versions

        Returns:
            Dictionary of mixed sensors

        Example:
            # Test with real pH sensor but mock environmental sensors
            sensors = SensorFactory.create_hybrid_sensors(
                mock_sensors=['bme280', 'bme680'],
                real_sensors=['ph']
            )
        """
        sensors = {}

        mock_sensors = mock_sensors or []
        real_sensors = real_sensors or []

        # Import mock sensors
        from .mock.bme280_mock import BME280Mock
        from .mock.bme680_mock import BME680Mock
        from .mock.ph_mock import PHMock

        mock_map = {"bme280": BME280Mock, "bme680": BME680Mock, "ph": PHMock}

        # Try to import real sensors
        try:
            from .hardware.bme280_real import BME280Real
            from .hardware.bme680_real import BME680Real
            from .hardware.ph_real import PHReal

            real_map = {"bme280": BME280Real, "bme680": BME680Real, "ph": PHReal}
        except ImportError:
            print("Hardware sensors not available, using all mocks")
            real_map = {}

        # Create mock sensors
        for sensor_id in mock_sensors:
            if sensor_id in mock_map:
                sensors[sensor_id] = mock_map[sensor_id]()
                print(f"🔧 Created MOCK sensor: {sensor_id}")

        # Create real sensors
        for sensor_id in real_sensors:
            if sensor_id in real_map:
                sensors[sensor_id] = real_map[sensor_id]()
                print(f"Created REAL sensor: {sensor_id}")
            elif sensor_id in mock_map:
                # Fallback to mock if real not available
                sensors[sensor_id] = mock_map[sensor_id]()
                print(f"{sensor_id} real sensor not available, using mock")

        return sensors
