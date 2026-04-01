"""
Database manager for SQLite operations
"""

import aiosqlite
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

from backend.src.config.settings import settings
from backend.src.utils.logger import logger


class DatabaseManager:
    """Manages SQLite database operations"""

    def __init__(self):
        self.db_path = settings.database_path
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Database directory: {db_dir}")

    async def initialize(self):
        """Initialize database with schema"""
        try:
            schema_path = (
                Path(__file__).parent.parent / "config" / "database_schema.sql"
            )

            if not schema_path.exists():
                raise FileNotFoundError(f"Schema file not found: {schema_path}")

            async with aiosqlite.connect(self.db_path) as db:
                with open(schema_path, "r") as f:
                    schema_sql = f.read()

                await db.executescript(schema_sql)
                await db.commit()

            logger.success(f"✅ Database initialized: {self.db_path}")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    # ==================== SENSOR READINGS ====================

    async def insert_sensor_reading(
        self, sensor_type: str, data: Dict[str, Any]
    ) -> int:
        """
        Insert sensor reading into database

        Args:
            sensor_type: Type of sensor (bme280, bme680, ph)
            data: Sensor reading data

        Returns:
            ID of inserted row
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """
                    INSERT INTO sensor_readings 
                    (sensor_type, temperature, humidity, pressure, 
                     gas_resistance, air_quality, ph)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        sensor_type,
                        data.get("temperature"),
                        data.get("humidity"),
                        data.get("pressure"),
                        data.get("gas_resistance"),
                        data.get("air_quality"),
                        data.get("ph"),
                    ),
                )
                await db.commit()
                return cursor.lastrowid

        except Exception as e:
            logger.error(f"Error inserting sensor reading: {e}")
            raise

    async def get_latest_readings(self) -> List[Dict]:
        """Get most recent reading from each sensor"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                cursor = await db.execute(
                    """
                    SELECT * FROM sensor_readings 
                    WHERE id IN (
                        SELECT MAX(id) 
                        FROM sensor_readings 
                        GROUP BY sensor_type
                    )
                    ORDER BY sensor_type
                """
                )

                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting latest readings: {e}")
            return []

    async def get_historical_data(
        self, hours: int = 24, limit: int = 1000, sensor_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Get historical sensor data

        Args:
            hours: Number of hours to look back
            limit: Maximum number of records
            sensor_type: Filter by sensor type (optional)

        Returns:
            List of sensor readings
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                if sensor_type:
                    cursor = await db.execute(
                        """
                        SELECT * FROM sensor_readings 
                        WHERE sensor_type = ?
                        AND timestamp >= datetime('now', '-' || ? || ' hours')
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (sensor_type, hours, limit),
                    )
                else:
                    cursor = await db.execute(
                        """
                        SELECT * FROM sensor_readings 
                        WHERE timestamp >= datetime('now', '-' || ? || ' hours')
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """,
                        (hours, limit),
                    )

                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return []

    async def delete_old_readings(self, days: int = 30) -> int:
        """
        Delete sensor readings older than specified days

        Args:
            days: Delete readings older than this many days

        Returns:
            Number of rows deleted
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """
                    DELETE FROM sensor_readings 
                    WHERE timestamp < datetime('now', '-' || ? || ' days')
                """,
                    (days,),
                )
                await db.commit()
                deleted = cursor.rowcount

                if deleted > 0:
                    logger.info(f"Deleted {deleted} old sensor readings")

                return deleted

        except Exception as e:
            logger.error(f"Error deleting old readings: {e}")
            return 0

    # ==================== THRESHOLD CONFIGURATIONS ====================

    async def get_configurations(self) -> List[Dict]:
        """Get all threshold configurations"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                cursor = await db.execute(
                    """
                    SELECT * FROM threshold_configurations 
                    ORDER BY name
                """
                )

                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting configurations: {e}")
            return []

    async def get_configuration(self, config_id: int) -> Optional[Dict]:
        """Get specific configuration by ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                cursor = await db.execute(
                    """
                    SELECT * FROM threshold_configurations 
                    WHERE id = ?
                """,
                    (config_id,),
                )

                row = await cursor.fetchone()
                return dict(row) if row else None

        except Exception as e:
            logger.error(f"Error getting configuration: {e}")
            return None

    async def get_active_configuration(self) -> Optional[Dict]:
        """Get currently active threshold configuration"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                cursor = await db.execute(
                    """
                    SELECT * FROM threshold_configurations 
                    WHERE is_active = 1 
                    LIMIT 1
                """
                )

                row = await cursor.fetchone()
                return dict(row) if row else None

        except Exception as e:
            logger.error(f"Error getting active configuration: {e}")
            return None

    async def create_configuration(self, config_data: Dict[str, Any]) -> int:
        """
        Create new threshold configuration

        Args:
            config_data: Configuration data

        Returns:
            ID of created configuration
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """
                    INSERT INTO threshold_configurations 
                    (name, description, ph_min, ph_max, temp_min, temp_max, 
                     humidity_min, humidity_max)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        config_data["name"],
                        config_data.get("description"),
                        config_data["ph_min"],
                        config_data["ph_max"],
                        config_data["temp_min"],
                        config_data["temp_max"],
                        config_data["humidity_min"],
                        config_data["humidity_max"],
                    ),
                )
                await db.commit()

                config_id = cursor.lastrowid
                logger.info(
                    f"Created configuration: {config_data['name']} (ID: {config_id})"
                )
                return config_id

        except Exception as e:
            logger.error(f"Error creating configuration: {e}")
            raise

    async def update_configuration(
        self, config_id: int, config_data: Dict[str, Any]
    ) -> bool:
        """
        Update threshold configuration

        Args:
            config_id: ID of configuration to update
            config_data: Fields to update

        Returns:
            True if successful
        """
        try:
            # Build dynamic UPDATE query based on provided fields
            fields = []
            values = []

            for key, value in config_data.items():
                if key != "id" and value is not None:
                    fields.append(f"{key} = ?")
                    values.append(value)

            if not fields:
                return False

            fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(config_id)

            query = f"""
                UPDATE threshold_configurations 
                SET {', '.join(fields)}
                WHERE id = ?
            """

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(query, values)
                await db.commit()

            logger.info(f"Updated configuration ID: {config_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            return False

    async def set_active_configuration(self, config_id: int) -> bool:
        """
        Set a configuration as active (deactivates all others)

        Args:
            config_id: ID of configuration to activate

        Returns:
            True if successful
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Deactivate all
                await db.execute(
                    """
                    UPDATE threshold_configurations 
                    SET is_active = 0
                """
                )

                # Activate specified one
                cursor = await db.execute(
                    """
                    UPDATE threshold_configurations 
                    SET is_active = 1, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """,
                    (config_id,),
                )

                await db.commit()

                if cursor.rowcount > 0:
                    logger.info(f"Activated configuration ID: {config_id}")
                    return True
                else:
                    logger.warning(f"Configuration ID {config_id} not found")
                    return False

        except Exception as e:
            logger.error(f"Error setting active configuration: {e}")
            return False

    async def delete_configuration(self, config_id: int) -> bool:
        """
        Delete threshold configuration

        Args:
            config_id: ID of configuration to delete

        Returns:
            True if successful
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Check if it's the active one
                cursor = await db.execute(
                    """
                    SELECT is_active FROM threshold_configurations 
                    WHERE id = ?
                """,
                    (config_id,),
                )
                row = await cursor.fetchone()

                if row and row[0] == 1:
                    logger.warning("Cannot delete active configuration")
                    return False

                # Delete it
                cursor = await db.execute(
                    """
                    DELETE FROM threshold_configurations 
                    WHERE id = ?
                """,
                    (config_id,),
                )
                await db.commit()

                if cursor.rowcount > 0:
                    logger.info(f"Deleted configuration ID: {config_id}")
                    return True
                return False

        except Exception as e:
            logger.error(f"Error deleting configuration: {e}")
            return False

    # ==================== ALERTS ====================

    async def create_alert(self, alert_data: Dict[str, Any]) -> int:
        """
        Create new alert

        Args:
            alert_data: Alert data

        Returns:
            ID of created alert
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """
                    INSERT INTO alerts 
                    (alert_type, sensor_type, message, severity, 
                     reading_value, threshold_min, threshold_max)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        alert_data["alert_type"],
                        alert_data.get("sensor_type"),
                        alert_data["message"],
                        alert_data.get("severity", "warning"),
                        alert_data.get("reading_value"),
                        alert_data.get("threshold_min"),
                        alert_data.get("threshold_max"),
                    ),
                )
                await db.commit()
                return cursor.lastrowid

        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise

    async def get_alerts(
        self, unread_only: bool = False, limit: int = 50
    ) -> List[Dict]:
        """
        Get alerts

        Args:
            unread_only: Only return unread alerts
            limit: Maximum number of alerts

        Returns:
            List of alerts
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row

                if unread_only:
                    cursor = await db.execute(
                        """
                        SELECT * FROM alerts 
                        WHERE is_read = 0
                        ORDER BY created_at DESC
                        LIMIT ?
                    """,
                        (limit,),
                    )
                else:
                    cursor = await db.execute(
                        """
                        SELECT * FROM alerts 
                        ORDER BY created_at DESC
                        LIMIT ?
                    """,
                        (limit,),
                    )

                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            return []

    async def mark_alert_read(self, alert_id: int) -> bool:
        """Mark alert as read"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """
                    UPDATE alerts 
                    SET is_read = 1 
                    WHERE id = ?
                """,
                    (alert_id,),
                )
                await db.commit()
                return True

        except Exception as e:
            logger.error(f"Error marking alert as read: {e}")
            return False
