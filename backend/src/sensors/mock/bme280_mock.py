"""
Mock BME280 sensor for development
Simulates temperature, humidity, and pressure readings
"""
import random
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor


class BME280Mock(BaseSensor):
    """Mock BME280 sensor generating realistic fake data"""
    
    def __init__(self):
        super().__init__(
            sensor_id="bme280",
            name="BME280 Temperature/Humidity/Pressure Sensor (MOCK)"
        )
        # Base values with realistic ranges
        self.base_temp = 22.0  # °C
        self.base_humidity = 60.0  # %
        self.base_pressure = 1013.25  # hPa
        
        # Variation ranges
        self.temp_variation = 2.0
        self.humidity_variation = 5.0
        self.pressure_variation = 3.0
    
    async def read(self) -> Dict[str, Any]:
        """
        Generate mock sensor readings with realistic variations
        
        Returns:
            Dictionary with temperature, humidity, and pressure
        """
        # Add random variation to base values
        temperature = self.base_temp + random.uniform(
            -self.temp_variation, 
            self.temp_variation
        )
        humidity = self.base_humidity + random.uniform(
            -self.humidity_variation,
            self.humidity_variation
        )
        pressure = self.base_pressure + random.uniform(
            -self.pressure_variation,
            self.pressure_variation
        )
        
        # Ensure humidity stays in valid range (0-100%)
        humidity = max(0, min(100, humidity))
        
        # Store reading
        self.last_reading = {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2),
            "unit_temp": "C",
            "unit_humidity": "%",
            "unit_pressure": "hPa"
        }
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading
    
    def set_base_values(self, temp: float = None, humidity: float = None, 
                       pressure: float = None):
        """
        Set base values for testing different conditions
        
        Args:
            temp: Base temperature in °C
            humidity: Base humidity in %
            pressure: Base pressure in hPa
        """
        if temp is not None:
            self.base_temp = temp
        if humidity is not None:
            self.base_humidity = humidity
        if pressure is not None:
            self.base_pressure = pressure
        