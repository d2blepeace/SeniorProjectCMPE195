"""
Real BME280 sensor implementation for Raspberry Pi
Reads temperature, humidity, and pressure via I2C
"""
import asyncio
import board
import adafruit_bme280.advanced as adafruit_bme280
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor


class BME280Real(BaseSensor):
    """Real BME280 sensor via I2C on Raspberry Pi"""
    
    def __init__(self, i2c_address=0x76):
        """
        Initialize BME280 sensor
        
        Args:
            i2c_address: I2C address (default: 0x76, alternative: 0x77)
        """
        super().__init__("bme280", "BME280 Sensor")
        
        try:
            # Initialize I2C
            i2c = board.I2C()
            self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=i2c_address)
            
            # Configure sensor for highest accuracy
            self.sensor.sea_level_pressure = 1013.25
            self.sensor.mode = adafruit_bme280.MODE_NORMAL
            self.sensor.standby_period = adafruit_bme280.STANDBY_TC_500
            self.sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
            
            self.sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
            self.sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X2
            self.sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X8
            
            self.is_initialized = True
            print(f"BME280 initialized at address 0x{i2c_address:02x}")
            
        except Exception as e:
            print(f"Failed to initialize BME280: {e}")
            self.sensor = None
            self.is_initialized = False
    
    def _blocking_i2c_read(self) -> Dict[str, Any]:
        """
        Synchronous I2C read (runs in thread pool)
        
        Returns:
            Dictionary with temperature, humidity, pressure
        """
        if not self.sensor:
            raise RuntimeError("BME280 sensor not initialized")
        
        # Read from I2C (blocking operation)
        temperature = self.sensor.temperature
        humidity = self.sensor.humidity
        pressure = self.sensor.pressure
        
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "pressure": round(pressure, 2)
        }
    
    async def read(self) -> Dict[str, Any]:
        """
        Async wrapper for I2C read
        
        Uses run_in_executor to prevent blocking the event loop
        
        Returns:
            Sensor reading dictionary
        """
        if not self.is_initialized:
            raise RuntimeError("BME280 sensor not initialized")
        
        # Get event loop
        loop = asyncio.get_event_loop()
        
        # Run blocking I2C read in thread pool
        data = await loop.run_in_executor(None, self._blocking_i2c_read)
        
        # Store reading
        self.last_reading = {
            **data,
            "unit_temp": "C",
            "unit_humidity": "%",
            "unit_pressure": "hPa"
        }
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading


# Test function 
if __name__ == "__main__":
    async def test():
        sensor = BME280Real()
        reading = await sensor.read()
        print(f"Reading: {reading}")
    
    asyncio.run(test())
