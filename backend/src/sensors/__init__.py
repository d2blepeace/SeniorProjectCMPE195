"""
Sensor package for Smart Hydroponic System
Provides sensor abstraction, mock implementations, and hardware interfaces
"""

from .base_sensor import BaseSensor
from .sensor_manager import SensorManager
from .sensor_factory import SensorFactory

__all__ = [
    'BaseSensor',
    'SensorManager',
    'SensorFactory',
]

__version__ = '1.0.0'