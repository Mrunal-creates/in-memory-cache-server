import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "cache.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache_data (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

        self.connection.commit()

    def save(self, key, value):

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO cache_data
            (key, value)
            VALUES (?, ?)
            """,
            (key, str(value))
        )

        self.connection.commit()

    def get(self, key):

        self.cursor.execute(
            """
            SELECT value
            FROM cache_data
            WHERE key = ?
            """,
            (key,)
        )

        result = self.cursor.fetchone()

        if result:
            return result[0]

        return None

    def delete(self, key):

        self.cursor.execute(
            """
            DELETE FROM cache_data
            WHERE key = ?
            """,
            (key,)
        )

        self.connection.commit()