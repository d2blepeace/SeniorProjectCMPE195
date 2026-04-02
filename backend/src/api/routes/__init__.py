"""API route modules"""

from . import health
from . import sensors
from . import configurations
from . import alerts

__all__ = ["health", "sensors", "configurations", "alerts"]
