# Stores plant data
import sqlite3

class Database:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            ph REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        self.conn.execute(query)
        self.conn.commit()

    def insert_data(self, temp, hum, ph):

        query = """
        INSERT INTO sensor_data (temperature, humidity, ph)
        VALUES (?, ?, ?)
        """

        self.conn.execute(query, (temp, hum, ph))
        self.conn.commit()