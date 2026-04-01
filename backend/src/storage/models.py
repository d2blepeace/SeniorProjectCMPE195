"""
Pydantic models for request/response validation

THRESHOLD CONFIGURATIONS:
These models support flexible configuration strategies:
  - Plant-centric: name="Lettuce", description="For leafy greens"
  - System-centric: name="My Indoor Garden", description="Basement setup"
  - Hybrid: name="Custom Lettuce", description="Based on lettuce template"
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# ==================== SENSOR READING MODELS ====================

class SensorReading(BaseModel):
    """Base sensor reading model"""
    sensor_type: str
    timestamp: datetime = Field(default_factory=datetime.now)


class BME280Reading(SensorReading):
    """BME280 sensor reading"""
    sensor_type: str = "bme280"
    temperature: float
    humidity: float
    pressure: float


class BME680Reading(SensorReading):
    """BME680 sensor reading"""
    sensor_type: str = "bme680"
    temperature: float
    humidity: float
    pressure: float
    gas_resistance: int
    air_quality: str


class PHReading(SensorReading):
    """pH sensor reading"""
    sensor_type: str = "ph"
    ph: float
    
    @validator('ph')
    def validate_ph(cls, v):
        if not 0 <= v <= 14:
            raise ValueError('pH must be between 0 and 14')
        return v


# ==================== THRESHOLD CONFIGURATION MODELS ====================
# 
# These models represent alert threshold configurations.
# They are intentionally generic to support multiple use cases:
#
# USE CASE 1: Plant-Specific Profiles
#   name = "Lettuce"
#   description = "Optimal ranges for lettuce cultivation"
#
# USE CASE 2: Custom System Settings
#   name = "My Greenhouse Setup"
#   description = "Custom ranges for mixed crop greenhouse"
#
# USE CASE 3: Environmental Presets
#   name = "Summer Configuration"
#   description = "Adjusted for high ambient temperatures"

class ThresholdConfigurationBase(BaseModel):
    """
    Base threshold configuration
    
    Can represent plant profiles, system settings, or environmental presets.
    Name and description fields allow flexible interpretation.
    """
    name: str = Field(
        ..., 
        description="Configuration name (e.g., 'Lettuce' or 'My Indoor Setup')"
    )
    description: Optional[str] = Field(
        None,
        description="Optional details about this configuration's purpose"
    )
    
    # pH thresholds
    ph_min: float = Field(ge=0, le=14, description="Minimum acceptable pH")
    ph_max: float = Field(ge=0, le=14, description="Maximum acceptable pH")
    
    # Temperature thresholds (Celsius)
    temp_min: float = Field(description="Minimum acceptable temperature (°C)")
    temp_max: float = Field(description="Maximum acceptable temperature (°C)")
    
    # Humidity thresholds (percentage)
    humidity_min: float = Field(
        ge=0, le=100, 
        description="Minimum acceptable humidity (%)"
    )
    humidity_max: float = Field(
        ge=0, le=100,
        description="Maximum acceptable humidity (%)"
    )
    
    @validator('ph_max')
    def validate_ph_range(cls, v, values):
        if 'ph_min' in values and v < values['ph_min']:
            raise ValueError('ph_max must be >= ph_min')
        return v
    
    @validator('temp_max')
    def validate_temp_range(cls, v, values):
        if 'temp_min' in values and v < values['temp_min']:
            raise ValueError('temp_max must be >= temp_min')
        return v
    
    @validator('humidity_max')
    def validate_humidity_range(cls, v, values):
        if 'humidity_min' in values and v < values['humidity_min']:
            raise ValueError('humidity_max must be >= humidity_min')
        return v


class ThresholdConfigurationCreate(ThresholdConfigurationBase):
    """
    Create a new threshold configuration
    
    Examples:
      - Plant-based: {"name": "Tomato", "description": "For tomato plants", ...}
      - System-based: {"name": "Main Reservoir", "description": "Indoor setup", ...}
    """
    pass


class ThresholdConfigurationUpdate(BaseModel):
    """Update threshold configuration (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    ph_min: Optional[float] = Field(None, ge=0, le=14)
    ph_max: Optional[float] = Field(None, ge=0, le=14)
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    humidity_min: Optional[float] = Field(None, ge=0, le=100)
    humidity_max: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None


class ThresholdConfiguration(ThresholdConfigurationBase):
    """
    Threshold configuration from database
    
    The active configuration (is_active=True) determines alert thresholds.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== ALERT MODELS ====================

class AlertCreate(BaseModel):
    """Create alert"""
    alert_type: str
    sensor_type: Optional[str] = None
    message: str
    severity: str = Field(default="warning", pattern="^(info|warning|critical)$")
    reading_value: Optional[float] = None
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None


class Alert(AlertCreate):
    """Alert from database"""
    id: int
    is_read: bool
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== RESPONSE MODELS ====================

class SensorReadingsResponse(BaseModel):
    """Response with sensor readings"""
    status: str = "success"
    timestamp: datetime = Field(default_factory=datetime.now)
    data: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    status: str
    message: str


class HistoricalDataResponse(BaseModel):
    """Response with historical data"""
    status: str = "success"
    count: int
    data: List[dict]
