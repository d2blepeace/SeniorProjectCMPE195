"""Database storage module"""

from .db_manager import DatabaseManager

# Create singleton instance
db_manager = DatabaseManager()

__all__ = ["db_manager", "DatabaseManager"]
