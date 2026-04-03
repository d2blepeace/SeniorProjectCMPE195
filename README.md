# Smart Hydroponic Garden System

**CMPE 195A/B Senior Project | Team Expedition 23**

An IoT-enabled hydroponic monitoring system with real-time sensor data collection, web-based dashboard, and automated alert management.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Development](#development)
- [Deployment](#deployment)
- [Team](#team)

---

## Overview

The Smart Hydroponic Garden System automates the monitoring of hydroponic growing environments by tracking:
- **Temperature** (BME280 & BME680 sensors)
- **Humidity** (BME280 & BME680 sensors)
- **Air Quality** (BME680 sensor)
- **pH Levels** (Atlas Scientific pH sensor)
- **Atmospheric Pressure** (BME280 & BME680 sensors)

The system stores historical data, provides real-time visualization, and sends alerts when conditions fall outside optimal ranges.

---

## Features
- REST API with FastAPI
- Mock sensor data generation (development/testing)
- Background task auto-reads sensors every 60 seconds
- Threshold configurations (plant profiles or custom settings)
- Interactive API documentation (Swagger UI)
- CORS-enabled for frontend development

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                       │
│                    - HTML/CSS/JavaScript                    │
│                    - Chart.js for visualization             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI - Python)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Routes                                          │   │
│  │  - /api/health                                       │   │
│  │  - /api/sensors/*                                    │   │
│  │  - /api/configurations/*                             │   │
│  │  - /api/alerts/*                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────────────┐    │
│  │                                                     │    │
│  ▼                                                     ▼    │
│  ┌────────────────────┐                  ┌──────────────┐   │
│  │ Background Task    │                  │   Sensor     │   │
│  │ (Data Collector)   │◄────────────────►│   Manager    │   │
│  │                    │                  │              │   │
│  │ Runs every 60s     │                  │ Mock/Real    │   │
│  └────────┬───────────┘                  └──────┬───────┘   │
│           │                                     │           │
│           └─────────────┬───────────────────────┘           │
│                         ▼                                   │
│              ┌─────────────────────┐                        │
│              │ Database Manager    │                        │
│              │ (aiosqlite)         │                        │
│              └──────────┬──────────┘                        │
└─────────────────────────┼───────────────────────────────────┘
                          ▼
                ┌──────────────────┐
                │ SQLite Database  │
                │ (hydroponic.db)  │
                │                  │
                │ - sensor_readings│
                │ - configurations │
                │ - alerts         │
                └──────────────────┘
```

### Component Diagram

```
Backend Components:

┌──────────────────────────────────────────────────────┐
│                 backend/src/                         │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐    │
│  │   main.py  │  │   config/  │  │    utils/    │    │
│  │            │  │            │  │              │    │
│  │ - Startup  │  │ - settings │  │ - logger     │    │
│  │ - Lifespan │  │ - schema   │  │ - validators │    │
│  └────────────┘  └────────────┘  └──────────────┘    │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐    │
│  │    api/    │  │  sensors/  │  │  services/   │    │
│  │            │  │            │  │              │    │
│  │ - routes   │  │ - mock     │  │ - collector  │    │
│  │ - app      │  │ - hardware │  │ - alerts     │    │
│  └────────────┘  └────────────┘  └──────────────┘    │
│                                                      │
│  ┌────────────┐                                      │
│  │  storage/  │                                      │
│  │            │                                      │
│  │ - db_mgr   │                                      │
│  │ - models   │                                      │
│  └────────────┘                                      │
└──────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.9+
- Git
- Virtual environment support

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd group-project-expedition-23

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env if needed (defaults work for development)

# 6. Start the backend server
python -m backend.src.main
```

### Access the API

- **API Base:** `http://localhost:8000`
- **Interactive Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/api/health`

### Verify It's Working

```bash
# In another terminal
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","service":"Smart Hydroponic System API","timestamp":"..."}
```

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/status` | GET | Detailed system status |
| `/api/sensors/current` | GET | Read sensors immediately |
| `/api/sensors/latest` | GET | Latest readings from database |
| `/api/sensors/historical` | GET | Historical data for charts |
| `/api/configurations/` | GET | List all threshold configurations |
| `/api/configurations/active` | GET | Get active configuration |
| `/api/configurations/` | POST | Create new configuration |
| `/api/configurations/{id}` | PATCH | Update configuration |
| `/api/configurations/{id}/activate` | POST | Activate configuration |
| `/api/configurations/{id}` | DELETE | Delete configuration |
| `/api/alerts/` | GET | Get alerts |
| `/api/alerts/{id}/read` | PATCH | Mark alert as read |

### Example Requests

#### Get Current Sensor Readings

```bash
curl http://localhost:8000/api/sensors/current
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-01-10T18:30:00",
  "data": {
    "bme280": {
      "temperature": 22.5,
      "humidity": 58.3,
      "pressure": 1013.2,
      "unit_temp": "C",
      "unit_humidity": "%",
      "unit_pressure": "hPa"
    },
    "bme680": {
      "temperature": 22.3,
      "humidity": 59.1,
      "air_quality": "Good",
      "gas_resistance": 165432
    },
    "ph": {
      "ph": 6.2,
      "status": "optimal"
    }
  }
}
```

#### Get Historical Data

```bash
curl "http://localhost:8000/api/sensors/historical?hours=24&sensor_type=bme280"
```

#### Activate Configuration

```bash
curl -X POST http://localhost:8000/api/configurations/2/activate
```

**For complete API documentation, visit:** `http://localhost:8000/docs`

---

## Database Schema

### Entity Relationship Diagram

```
┌──────────────────────┐
│  sensor_readings     │
├──────────────────────┤
│ id (PK)              │
│ sensor_type          │◄──── "bme280", "bme680", "ph"
│ temperature          │
│ humidity             │
│ pressure             │
│ gas_resistance       │
│ air_quality          │
│ ph                   │
│ timestamp            │
└──────────────────────┘

┌─────────────────────────────┐
│  threshold_configurations   │
├─────────────────────────────┤
│ id (PK)                     │
│ name                        │◄──── "Lettuce", "My System"
│ description                 │
│ ph_min, ph_max              │
│ temp_min, temp_max          │
│ humidity_min, humidity_max  │
│ is_active (UNIQUE=1)        │◄──── Only one active
│ created_at, updated_at      │
└─────────────────────────────┘

┌──────────────────────┐
│  alerts              │
├──────────────────────┤
│ id (PK)              │
│ alert_type           │
│ sensor_type          │
│ message              │
│ severity             │◄──── "info", "warning", "critical"
│ reading_value        │
│ threshold_min/max    │
│ is_read, is_resolved │
│ created_at           │
└──────────────────────┘
```

### Tables

#### `sensor_readings`
Stores historical sensor data. Updated every 60 seconds by background task.

**Columns:**
- `id` - Primary key
- `sensor_type` - "bme280", "bme680", or "ph"
- `temperature` - Temperature in °C
- `humidity` - Humidity percentage
- `pressure` - Atmospheric pressure (hPa)
- `gas_resistance` - Air quality sensor value
- `air_quality` - "Good", "Moderate", "Poor"
- `ph` - pH value (0-14)
- `timestamp` - When reading was taken

#### `threshold_configurations`
Stores alert threshold settings (plant profiles or custom configurations).

**Columns:**
- `id` - Primary key
- `name` - Configuration name
- `description` - Optional description
- `ph_min`, `ph_max` - pH range
- `temp_min`, `temp_max` - Temperature range (°C)
- `humidity_min`, `humidity_max` - Humidity range (%)
- `is_active` - Boolean (only one can be active)
- `created_at`, `updated_at` - Timestamps

**Constraint:** Only ONE configuration can have `is_active = 1` at a time.

#### `alerts`
Stores system alerts and notifications.

**Columns:**
- `id` - Primary key
- `alert_type` - Type of alert
- `sensor_type` - Which sensor triggered it
- `message` - Human-readable message
- `severity` - "info", "warning", "critical"
- `reading_value` - Actual reading
- `threshold_min`, `threshold_max` - Expected range
- `is_read`, `is_resolved` - Status flags
- `created_at`, `resolved_at` - Timestamps

---

## Development

### Project Structure

```
group-project-expedition-23/
├── backend/
│   └── src/
│       ├── main.py              # Application entry point
│       ├── api/                 # REST API endpoints
│       ├── sensors/             # Sensor abstraction layer
│       ├── storage/             # Database layer
│       ├── services/            # Background tasks
│       ├── config/              # Configuration
│       └── utils/               # Utilities
├── frontend/                    # Web dashboard (TBD)
├── docs/                        # Documentation
├── tests/                       # Test suite
├── data/                        # Runtime data (git-ignored)
├── logs/                        # Application logs (git-ignored)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

### Environment Variables

Create a `.env` file in the project root:

```env
# Application
APP_NAME=Smart Hydroponic System
DEBUG=True
LOG_LEVEL=INFO

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_PATH=./data/hydroponic.db

# Sensors
USE_MOCK_SENSORS=True
SENSOR_READ_INTERVAL=60

# CORS
ALLOWED_ORIGINS=*
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_sensors.py
```

### Code Quality

```bash
# Format code
black backend/

# Check linting (optional)
flake8 backend/

# Type checking (optional)
mypy backend/
```

---

## Data Flow

### Background Data Collection

```
┌─────────────────────────────────────────────────────────┐
│                    Server Startup                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Initialize Database                           │
│   - Create tables if not exist                          │
│   - Load default configurations                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│       Start Background Data Collector                   │
│   - Creates sensor_manager (mock or real)               │
│   - Starts async collection loop                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Every 60s    │
              └──────┬───────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Read All Sensors                              │
│   sensor_manager.read_all()                             │
│                                                         │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│   │  BME280  │  │  BME680  │  │    pH    │              │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│        │             │             │                    │
│        └─────────────┴─────────────┘                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Store in Database                               │
│   db_manager.insert_sensor_reading()                    │
│                                                         │
│   For each sensor type:                                 │
│   - INSERT INTO sensor_readings                         │
│   - Log success/failure                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Wait 60s     │
              └──────┬───────┘
                     │
                     └──────► Loop back to "Read All Sensors"
```                     
### Frontend Request Flow

```
┌─────────────┐
│  Frontend   │  HTTP GET /api/sensors/latest
│  (Browser)  ├───────────────────────────────┐
└─────────────┘                               │
                                              ▼
                                   ┌──────────────────┐
                                   │  API Route       │
                                   │  sensors.py      │
                                   └────────┬─────────┘
                                            │
                                            ▼
                                   ┌──────────────────┐
                                   │ Database Manager │
                                   │ get_latest()     │
                                   └────────┬─────────┘
                                            │
                                            ▼
                                   ┌──────────────────┐
                                   │ SQLite Query     │
                                   └────────┬─────────┘
                                            │
                                            ▼
                                   ┌──────────────────┐
                                   │ JSON Response    │
                                   └────────┬─────────┘
                                            │
                                            ▼
┌─────────────┐                   ┌──────────────────┐
│  Frontend   │◄──────────────────┤ Return Data      │
│  Renders    │                   └──────────────────┘
└─────────────┘
```
---

## Deployment

### Development (Current)

```bash
# Use mock sensors
python -m backend.src.main
```

### Production (Raspberry Pi - Future)

```bash
# 1. Install hardware dependencies
pip install adafruit-circuitpython-bme280 adafruit-circuitpython-bme680

# 2. Update .env
USE_MOCK_SENSORS=False

# 3. Run server
python -m backend.src.main
```

### Run as System Service (systemd)

Create `/etc/systemd/system/hydroponic.service`:

```ini
[Unit]
Description=Smart Hydroponic System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/group-project-expedition-23
Environment="PATH=/home/pi/group-project-expedition-23/venv/bin"
ExecStart=/home/pi/group-project-expedition-23/venv/bin/python -m backend.src.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable hydroponic
sudo systemctl start hydroponic
sudo systemctl status hydroponic
```

---

## Troubleshooting

### Server Won't Start

**Issue:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Issue:** Port 8000 already in use

**Solution:**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn backend.src.main:app --port 8001
```

---

### Database Errors

**Issue:** Database file not found

**Solution:**
```bash
# Database is created automatically on first run
# Make sure you're running from project root
cd ~/group-project-expedition-23
python -m backend.src.main
```

---

**Issue:** Database locked

**Solution:**
```bash
# Close any SQLite browser/tool accessing the database
# Restart the server
```

---

### No Data Accumulating

**Issue:** Background task not running

**Solution:**
```bash
# Check server logs for "Stored X readings"
# Verify data collector status:
curl http://localhost:8000/ | jq '.data_collector'

# Should show: "is_running": true
```

---

## Additional Resources

- **Interactive API Docs:** `http://localhost:8000/docs`
- **ReDoc API Docs:** `http://localhost:8000/redoc`
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Raspberry Pi Setup:** `docs/HARDWARE_SETUP.md`
- **Frontend Integration:** `docs/FRONTEND_API_GUIDE.md`

---

## License

This project is developed as part of CMPE 195A/B Senior Project at San Jose State University.

---

##  Team

**Team Expedition 23**

| Name | Role | GitHub | Email |
|------|------|--------|-------|
| Hoa Tuong Minh Nguyen | Backend Lead | [@MinhHoaNguyen](https://github.com/MinhHoaNguyen) | hoatuongminh.nguyen@sjsu.edu |
| [Team Member 2] | Frontend Lead | [@username](https://github.com/username) | name@sjsu.edu |
| [Team Member 3] | Hardware Integration | [@username](https://github.com/username) | name@sjsu.edu |
| [Team Member 4] | Testing & Documentation | [@username](https://github.com/username) | name@sjsu.edu |

**Faculty Advisor:** [Advisor Name]

**Course:** CMPE 195A/B - Senior Design Project  
**Institution:** San Jose State University  
**Academic Year:** 2024-2025

---

## Acknowledgments

- FastAPI framework and community
- Adafruit for sensor libraries
- Chart.js for data visualization
- San Jose State University Computer Engineering Department

---

