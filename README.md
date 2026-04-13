# Smart Hydroponic Garden System

**CMPE 195A/B Senior Project | Team Expedition 23**

An IoT-enabled hydroponic monitoring system with real-time sensor data collection, web-based dashboard, and automated alert management.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Team](#team)

---

## Overview

Automates monitoring of hydroponic growing environments by tracking:
- **Temperature & Humidity** (BME280 & BME680 sensors)
- **Air Quality** (BME680 sensor)
- **pH Levels** (Atlas Scientific pH sensor)
- **Atmospheric Pressure** (BME280 & BME680 sensors)

The system stores historical data, provides real-time visualization, and sends alerts when conditions fall outside optimal ranges.

---

## Features

- REST API with FastAPI
- Mock sensor data generation (development/testing)
- Background auto-reads sensors every 60 seconds
- Configurable thresholds (plant profiles or custom settings)
- Interactive API documentation (Swagger UI)
- CORS-enabled for frontend development
- Remote access via ngrok tunnel

---

## Quick Start

### Prerequisites

- Raspberry Pi (or any Linux machine)
- Python 3.9+
- ngrok account (for remote access)

### Installation on Raspberry Pi

```bash
# 1. Clone repository
git clone <repository-url>
cd group-project-expedition-23

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running with Systemd (Persistent)

The backend runs as a system service and automatically restarts on boot.

```bash
# Service is already configured and running
sudo systemctl status backend

# View logs
sudo journalctl -u backend -f

# Restart after code changes
sudo systemctl restart backend
```

### Access the API

**Production (Remote Access):**
- **API Base:** `https://expedition-23.ngrok.app`
- **Interactive Docs:** `https://expedition-23.ngrok.app/docs`
- **Health Check:** `https://expedition-23.ngrok.app/api/health`

**Local (on Raspberry Pi):**
- **API Base:** `http://localhost:8000`

### Verify It's Working

```bash
# Remote access
curl https://expedition-23.ngrok.app/api/health

# Local access (on Pi)
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"...}
```

---

## API Reference

### Base URL

**Production:** `https://expedition-23.ngrok.app`  
**Local:** `http://localhost:8000`

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/sensors/current` | GET | Read sensors immediately |
| `/api/sensors/latest` | GET | Latest readings from database |
| `/api/sensors/historical` | GET | Historical data (query: `?hours=24&sensor_type=bme280`) |
| `/api/configurations/active` | GET | Get active threshold configuration |
| `/api/configurations/{id}/activate` | POST | Activate a configuration |
| `/api/alerts/` | GET | Get alerts (query: `?unread_only=true`) |

### Example Response

```bash
curl https://expedition-23.ngrok.app/api/sensors/current
```

```json
{
  "status": "success",
  "timestamp": "2025-01-10T18:30:00",
  "data": {
    "bme280": {
      "temperature": 22.5,
      "humidity": 58.3,
      "pressure": 1013.2
    },
    "ph": {
      "ph": 6.2,
      "status": "optimal"
    }
  }
}
```

**Complete documentation:** `https://expedition-23.ngrok.app/docs`

---

## Database Schema

### Tables

#### `sensor_readings`
Stores historical sensor data (updated every 60s).

**Key Columns:**
- `sensor_type` - "bme280", "bme680", or "ph"
- `temperature`, `humidity`, `pressure` - Environmental data
- `ph` - pH value (0-14)
- `timestamp` - Reading time

#### `threshold_configurations`
Stores alert threshold settings.

**Key Columns:**
- `name` - Configuration name (e.g., "Lettuce", "Tomatoes")
- `ph_min`, `ph_max`, `temp_min`, `temp_max`, etc. - Threshold ranges
- `is_active` - Boolean (only ONE can be active)

#### `alerts`
Stores system notifications.

**Key Columns:**
- `severity` - "info", "warning", "critical"
- `message` - Human-readable alert
- `is_read`, `is_resolved` - Status flags

---

## Development

### Project Structure

```
group-project-expedition-23/
├── backend/src/
│   ├── main.py              # Entry point
│   ├── api/                 # REST API routes
│   ├── sensors/             # Mock & hardware sensors
│   ├── storage/             # Database management
│   ├── services/            # Background tasks
│   └── config/              # Settings & schema
├── frontend/                # Web dashboard (TBD)
├── tests/                   # Test suite
├── data/                    # Runtime data (git-ignored)
└── requirements.txt
```

### Frontend Integration

Use the ngrok URL in your frontend:

```javascript
const API_BASE_URL = 'https://expedition-23.ngrok.app';

// Example API call
fetch(`${API_BASE_URL}/api/sensors/latest`)
  .then(res => res.json())
  .then(data => console.log(data));
```

### Running Tests

```bash
source venv/bin/activate
pytest
pytest --cov=backend  # With coverage
```

---

## Deployment

### Current Production Setup (Raspberry Pi)

The system is deployed with:

**Backend Service (backend.service):**
- Runs FastAPI application on port 8000
- Auto-starts on boot
- Auto-restarts on failure
- Uses real hardware sensors

**ngrok Tunnel (ngrok.service):**
- Exposes backend to internet via `https://expedition-23.ngrok.app`
- Persistent URL (doesn't change on restart)
- Auto-starts on boot

### Managing Services

```bash
# Check service status
sudo systemctl status backend
sudo systemctl status ngrok

# View logs
sudo journalctl -u backend -f
sudo journalctl -u ngrok -f

# Restart services
sudo systemctl restart backend
sudo systemctl restart ngrok

# Stop services
sudo systemctl stop backend
sudo systemctl stop ngrok
```

### Hardware Configuration

Update `.env` for production:

```env
# Use real hardware sensors
USE_MOCK_SENSORS=False

# Sensor read interval (seconds)
SENSOR_READ_INTERVAL=60
```

---

## Troubleshooting

### Backend Service Issues

**Issue:** Service won't start

```bash
# Check detailed logs
sudo journalctl -u backend -n 50

# Common fixes:
# 1. Verify Python path
which python3

# 2. Check file permissions
ls -la ~/group-project-expedition-23

# 3. Restart service
sudo systemctl restart backend
```

**Issue:** Import errors

```bash
# Reinstall dependencies
cd ~/group-project-expedition-23
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart backend
```

### ngrok Tunnel Issues

**Issue:** Tunnel not accessible

```bash
# Check ngrok service
sudo systemctl status ngrok

# Verify ngrok is running
curl http://localhost:4040/api/tunnels

# Restart ngrok
sudo systemctl restart ngrok
```

**Issue:** URL not working

```bash
# Verify correct URL in service file
sudo cat /etc/systemd/system/ngrok.service

# Should show: --url=expedition-23.ngrok.app 8000
```

### Database Issues

**Issue:** No data being stored

```bash
# Check if backend is running
sudo systemctl status backend

# View data collector logs
sudo journalctl -u backend | grep "collector"

# Verify database file exists
ls -la ~/group-project-expedition-23/data/
```

**Issue:** Database locked

```bash
# Close any SQLite browser tools
# Restart backend service
sudo systemctl restart backend
```

---

## Additional Resources

- **Interactive API Docs:** `https://expedition-23.ngrok.app/docs`
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **ngrok Documentation:** https://ngrok.com/docs

---

## License

This project is developed as part of CMPE 195A/B Senior Project at San Jose State University.

---

## Team

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
```
