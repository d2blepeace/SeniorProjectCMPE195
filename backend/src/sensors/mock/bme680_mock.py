"""
Mock BME680 sensor for development
Simulates temperature, humidity, pressure, and air quality readings
"""
import random
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor


class BME680Mock(BaseSensor):
    """Mock BME680 sensor with air quality simulation"""
    
    def __init__(self):
        super().__init__(
            sensor_id="bme680",
            name="BME680 Environmental Sensor (MOCK)"
        )
        # Base values
        self.base_temp = 22.0  # °C
        self.base_humidity = 60.0  # %
        self.base_pressure = 1013.25  # hPa
        self.base_gas_resistance = 150000  # Ohms (higher = better air quality)
        
        # Variation ranges
        self.temp_variation = 2.0
        self.humidity_variation = 5.0
        self.pressure_variation = 3.0
        self.gas_variation = 30000
    
    async def read(self) -> Dict[str, Any]:
        """
        Generate mock sensor readings including air quality
        
        Returns:
            Dictionary with temperature, humidity, pressure, and air quality
        """
        # Add random variation
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
        gas_resistance = self.base_gas_resistance + random.uniform(
            -self.gas_variation,
            self.gas_variation
        )
        
        # Ensure valid ranges
        humidity = max(0, min(100, humidity))
        gas_resistance = max(10000, gas_resistance)
        
        # Calculate air quality index based on gas resistance
        # Higher resistance = better air quality
        if gas_resistance > 150000:
            air_quality = "Good"
            aqi_score = 1
        elif gas_resistance > 100000:
            air_quality = "Moderate"
            aqi_score = 2
        elif gas_resistance > 50000:
            air_quality = "Poor"
            aqi_score = 3
        else:
            air_quality = "Unhealthy"
            aqi_score = 4
        
        # Store reading
        self.last_reading = {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2),
            "gas_resistance": int(gas_resistance),
            "air_quality": air_quality,
            "aqi_score": aqi_score,
            "unit_temp": "C",
            "unit_humidity": "%",
            "unit_pressure": "hPa",
            "unit_gas": "Ohms"
        }
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading
    
    def simulate_poor_air_quality(self):
        """Simulate poor air quality for testing alerts"""
        self.base_gas_resistance = 40000
    
    def simulate_good_air_quality(self):
        """Simulate good air quality"""
        self.base_gas_resistance = 180000