"""
Real pH sensor implementation for Raspberry Pi
Atlas Scientific pH sensor via I2C
"""
import asyncio
import time
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor

try:
    import smbus2
    SMBUS_AVAILABLE = True
except ImportError:
    SMBUS_AVAILABLE = False
    print("smbus2 not available - install with: pip install smbus2")


class PHReal(BaseSensor):
    """Real Atlas Scientific pH sensor via I2C"""
    
    def __init__(self, i2c_address=0x63):
        """
        Initialize pH sensor
        
        Args:
            i2c_address: I2C address (default: 0x63 for Atlas Scientific)
        """
        super().__init__("ph", "Atlas Scientific pH Sensor")
        
        if not SMBUS_AVAILABLE:
            print("smbus2 not installed")
            self.sensor = None
            self.is_initialized = False
            return
        
        try:
            self.bus = smbus2.SMBus(1)  # I2C bus 1 on Raspberry Pi
            self.address = i2c_address
            
            # Test connection
            self._send_command("Status")
            time.sleep(0.3)
            
            self.is_initialized = True
            print(f"pH sensor initialized at address 0x{i2c_address:02x}")
            
        except Exception as e:
            print(f"Failed to initialize pH sensor: {e}")
            self.sensor = None
            self.is_initialized = False
    
    def _send_command(self, command: str):
        """Send command to pH sensor"""
        command_bytes = (command + "\00").encode('latin-1')
        self.bus.write_i2c_block_data(self.address, 0, list(command_bytes))
    
    def _read_response(self) -> str:
        """Read response from pH sensor"""
        time.sleep(0.9)  # Wait for sensor to process
        
        # Read response
        response = self.bus.read_i2c_block_data(self.address, 0, 31)
        
        # Remove null bytes and decode
        response_str = ''.join([chr(byte) for byte in response if byte != 0])
        
        return response_str.strip()
    
    def _blocking_i2c_read(self) -> Dict[str, Any]:
        """
        Synchronous I2C read (runs in thread pool)
        
        Returns:
            Dictionary with pH value and status
        """
        if not self.is_initialized:
            raise RuntimeError("pH sensor not initialized")
        
        # Send read command
        self._send_command("R")
        
        # Get response
        response = self._read_response()
        
        # Parse pH value
        try:
            ph_value = float(response)
        except ValueError:
            raise RuntimeError(f"Invalid pH reading: {response}")
        
        # Determine status based on typical hydroponic ranges
        if 5.5 <= ph_value <= 6.5:
            status = "optimal"
            status_message = "pH is in optimal range"
        elif 5.0 <= ph_value < 5.5 or 6.5 < ph_value <= 7.0:
            status = "acceptable"
            status_message = "pH is acceptable but not optimal"
        elif ph_value < 5.0:
            status = "low"
            status_message = "pH is too low (acidic)"
        else:
            status = "high"
            status_message = "pH is too high (alkaline)"
        
        return {
            "ph": round(ph_value, 2),
            "status": status,
            "status_message": status_message,
            "temperature_compensated": False  # Add temp compensation if needed
        }
    
    async def read(self) -> Dict[str, Any]:
        """
        Async wrapper for I2C read
        
        Returns:
            Sensor reading dictionary
        """
        if not self.is_initialized:
            raise RuntimeError("pH sensor not initialized")
        
        # Get event loop
        loop = asyncio.get_event_loop()
        
        # Run blocking I2C read in thread pool
        data = await loop.run_in_executor(None, self._blocking_i2c_read)
        
        # Store reading
        self.last_reading = data
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading


# Test function
if __name__ == "__main__":
    async def test():
        sensor = PHReal()
        if sensor.is_initialized:
            reading = await sensor.read()
            print(f"pH Reading: {reading}")
        else:
            print("Sensor not initialized")
    
    asyncio.run(test())
