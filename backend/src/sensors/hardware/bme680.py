"""
Real BME680 sensor implementation for Raspberry Pi
Reads temperature, humidity, pressure, and air quality via I2C
"""
import asyncio
import board
import adafruit_bme680
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor


class BME680Real(BaseSensor):
    """Real BME680 sensor via I2C on Raspberry Pi"""
    
    def __init__(self, i2c_address=0x77):
        """
        Initialize BME680 sensor
        
        Args:
            i2c_address: I2C address (default: 0x77, alternative: 0x76)
        """
        super().__init__("bme680", "BME680 Sensor")
        
        try:
            # Initialize I2C
            i2c = board.I2C()
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=i2c_address)
            
            # Configure sensor
            self.sensor.sea_level_pressure = 1013.25
            
            self.is_initialized = True
            print(f"BME680 initialized at address 0x{i2c_address:02x}")
            
        except Exception as e:
            print(f"Failed to initialize BME680: {e}")
            self.sensor = None
            self.is_initialized = False
    
    def _blocking_i2c_read(self) -> Dict[str, Any]:
        """
        Synchronous I2C read (runs in thread pool)
        
        Returns:
            Dictionary with temperature, humidity, pressure, gas resistance
        """
        if not self.sensor:
            raise RuntimeError("BME680 sensor not initialized")
        
        # Read from I2C (blocking operation)
        temperature = self.sensor.temperature
        humidity = self.sensor.humidity
        pressure = self.sensor.pressure
        gas_resistance = self.sensor.gas
        
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
        
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2),
            "gas_resistance": int(gas_resistance),
            "air_quality": air_quality,
            "aqi_score": aqi_score
        }
    
    async def read(self) -> Dict[str, Any]:
        """
        Async wrapper for I2C read
        
        Returns:
            Sensor reading dictionary
        """
        if not self.is_initialized:
            raise RuntimeError("BME680 sensor not initialized")
        
        # Get event loop
        loop = asyncio.get_event_loop()
        
        # Run blocking I2C read in thread pool
        data = await loop.run_in_executor(None, self._blocking_i2c_read)
        
        # Store reading
        self.last_reading = {
            **data,
            "unit_temp": "C",
            "unit_humidity": "%",
            "unit_pressure": "hPa",
            "unit_gas": "Ohms"
        }
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading


# Test function
if __name__ == "__main__":
    async def test():
        sensor = BME680Real()
        reading = await sensor.read()
        print(f"Reading: {reading}")
    
    asyncio.run(test())
