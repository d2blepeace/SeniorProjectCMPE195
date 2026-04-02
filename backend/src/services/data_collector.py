"""
Data collection service - runs in background
Compatible with both mock sensors and real Raspberry Pi sensors
"""

import asyncio
from datetime import datetime
from typing import Optional

from backend.src.sensors.sensor_factory import SensorFactory
from backend.src.storage import db_manager
from backend.src.config.settings import settings
from backend.src.utils.logger import logger


class DataCollector:
    """
    Background service that periodically reads sensors

    Works with:
    - Mock sensors (development)
    - Real I2C sensors (Raspberry Pi)

    Automatically adjusts behavior based on USE_MOCK_SENSORS setting
    """

    def __init__(self):
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
        self.sensor_manager = None
        self.read_count = 0

    async def start(self):
        """Start background data collection"""
        if self.is_running:
            logger.warning("Data collector already running")
            return

        # Create sensor manager
        self.sensor_manager = SensorFactory.get_sensor_manager(
            use_mock=settings.use_mock_sensors
        )

        # Start background task
        self.is_running = True
        self.task = asyncio.create_task(self._collection_loop())

        sensor_type = "MOCK" if settings.use_mock_sensors else "REAL"
        logger.info(
            f"⏰ Data collector started ({sensor_type} sensors, "
            f"interval: {settings.sensor_read_interval}s)"
        )

    async def stop(self):
        """Stop background data collection"""
        if not self.is_running:
            return

        self.is_running = False

        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

        logger.info(f"🛑 Data collector stopped (collected {self.read_count} readings)")

    async def _collection_loop(self):
        """
        Main collection loop

        Continuously reads sensors at configured interval
        Works identically for mock and real sensors
        """
        logger.info("📊 Starting sensor collection loop...")

        while self.is_running:
            try:
                await self._read_and_store()

                # Wait for next interval
                await asyncio.sleep(settings.sensor_read_interval)

            except asyncio.CancelledError:
                logger.info("Collection loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in collection loop: {e}")
                # Continue despite errors (important for reliability)
                await asyncio.sleep(settings.sensor_read_interval)

    async def _read_and_store(self):
        """
        Read all sensors and store in database

        This method works identically whether sensors are mock or real
        The sensor_manager abstraction handles the difference
        """
        try:
            # Read all sensors (mock or real)
            readings = await self.sensor_manager.read_all()

            # Store each reading
            stored_count = 0
            for sensor_type, data in readings.items():
                if data.get("status") == "ok":
                    try:
                        await db_manager.insert_sensor_reading(sensor_type, data)
                        stored_count += 1
                    except Exception as e:
                        logger.error(f"Failed to store {sensor_type} reading: {e}")

            self.read_count += stored_count

            if stored_count > 0:
                logger.debug(
                    f"Stored {stored_count} readings " f"(total: {self.read_count})"
                )

        except Exception as e:
            logger.error(f"Error reading/storing sensors: {e}")

    def get_status(self) -> dict:
        """Get collector status"""
        return {
            "is_running": self.is_running,
            "total_readings": self.read_count,
            "using_mock": settings.use_mock_sensors,
            "interval_seconds": settings.sensor_read_interval,
        }


# Singleton instance
data_collector = DataCollector()
