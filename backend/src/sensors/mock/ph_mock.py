"""
Mock pH sensor for development
Simulates pH readings for hydroponic solution
"""
import random
from datetime import datetime
from typing import Dict, Any
from ..base_sensor import BaseSensor


class PHMock(BaseSensor):
    """Mock pH sensor for hydroponic solution monitoring"""
    
    def __init__(self):
        super().__init__(
            sensor_id="ph",
            name="Atlas Scientific pH Sensor (MOCK)"
        )
        # Base pH value (ideal for most hydroponic plants: 5.5-6.5)
        self.base_ph = 6.0
        self.ph_variation = 0.3
    
    async def read(self) -> Dict[str, Any]:
        """
        Generate mock pH reading
        
        Returns:
            Dictionary with pH value and status
        """
        # Add random variation
        ph = self.base_ph + random.uniform(
            -self.ph_variation,
            self.ph_variation
        )
        
        # Ensure pH stays in realistic range (0-14)
        ph = max(0, min(14, ph))
        
        # Determine status based on typical hydroponic ranges
        if 5.5 <= ph <= 6.5:
            status = "optimal"
            status_message = "pH is in optimal range"
        elif 5.0 <= ph < 5.5 or 6.5 < ph <= 7.0:
            status = "acceptable"
            status_message = "pH is acceptable but not optimal"
        elif ph < 5.0:
            status = "low"
            status_message = "pH is too low (acidic)"
        else:  # ph > 7.0
            status = "high"
            status_message = "pH is too high (alkaline)"
        
        # Store reading
        self.last_reading = {
            "ph": round(ph, 2),
            "status": status,
            "status_message": status_message,
            "temperature_compensated": True  # Mock sensors always compensated
        }
        self.last_reading_time = datetime.now().isoformat()
        
        return self.last_reading
    
    def set_ph(self, ph: float):
        """
        Set base pH value for testing
        
        Args:
            ph: pH value (0-14)
        """
        self.base_ph = max(0, min(14, ph))
    
    def simulate_low_ph(self):
        """Simulate low pH condition for testing alerts"""
        self.base_ph = 4.5
    
    def simulate_high_ph(self):
        """Simulate high pH condition for testing alerts"""
        self.base_ph = 7.8
    
    def simulate_optimal_ph(self):
        """Simulate optimal pH condition"""
        self.base_ph = 6.0