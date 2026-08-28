# tests/test_sensor_factory.py
"""Tests for SensorFactory to run without hardware"""

import sys
import types
import pytest

from backend.src.sensors.sensor_factory import SensorFactory, SENSOR_SPECS
from backend.src.sensors.base_sensor import BaseSensor


def test_forced_mock_returns_all_mocks():
    sensors = SensorFactory.create_sensors(use_mock=True)
    assert set(sensors) == set(SENSOR_SPECS)
    assert all(s.is_mock for s in sensors.values())


def test_missing_hardware_falls_back_per_sensor():
    """No hardware present: every sensor degrades to mock, nothing raises"""
    sensors = SensorFactory.create_sensors(use_mock=False)
    assert set(sensors) == set(SENSOR_SPECS)
    assert all(s.is_mock for s in sensors.values())
    assert all(isinstance(s, BaseSensor) for s in sensors.values())


def test_sensor_that_constructs_but_fails_init_is_treated_as_unavailable(monkeypatch):
    """
    Guards the PHReal case: __init__ succeeds but sets is_initialized=False.
    Without the explicit check this would be reported as REAL.
    """
    class HalfDeadSensor(BaseSensor):
        def __init__(self):
            super().__init__("ph", "Half-dead pH")
            self.is_initialized = False  # device or library missing

        async def read(self):
            raise RuntimeError("not connected")

    fake = types.ModuleType("backend.src.sensors.hardware.ph")
    fake.PHReal = HalfDeadSensor
    monkeypatch.setitem(sys.modules, "backend.src.sensors.hardware.ph", fake)

    sensors = SensorFactory.create_sensors(use_mock=False)
    assert sensors["ph"].is_mock is True


def test_working_hardware_is_reported_as_real(monkeypatch):
    """The success branch can't run on a laptop, so stub a healthy sensor."""
    class HealthySensor(BaseSensor):
        def __init__(self):
            super().__init__("bme280", "Fake BME280")

        async def read(self):
            return {"temperature": 22.0}

    fake = types.ModuleType("backend.src.sensors.hardware.bme280")
    fake.BME280Real = HealthySensor
    monkeypatch.setitem(sys.modules, "backend.src.sensors.hardware.bme280", fake)

    sensors = SensorFactory.create_sensors(use_mock=False)
    assert sensors["bme280"].is_mock is False   # real one used
    assert sensors["ph"].is_mock is True        # others still degrade


def test_hybrid_respects_explicit_lists():
    sensors = SensorFactory.create_hybrid_sensors(
        mock_sensors=["ph"], real_sensors=["bme280"]
    )
    assert set(sensors) == {"ph", "bme280"}
    assert sensors["ph"].is_mock is True


def test_hybrid_ignores_unknown_sensor_ids():
    sensors = SensorFactory.create_hybrid_sensors(mock_sensors=["not_a_sensor"])
    assert sensors == {}


def test_manager_exposes_all_sensor_ids():
    manager = SensorFactory.get_sensor_manager(use_mock=True)
    assert set(manager.get_sensor_ids()) == set(SENSOR_SPECS)