import sqlite3
import time


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

                value TEXT,

                expiry REAL,

                created_at REAL,

                updated_at REAL

            )
            """
        )

        self.connection.commit()

    def save(self, key, value, expiry):

        current_time = time.time()

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO cache_data
            (
                key,
                value,
                expiry,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                key,
                str(value),
                expiry,
                current_time,
                current_time
            )
        )

        self.connection.commit()

    def get(self, key):

        self.cursor.execute(
            """
            SELECT value, expiry
            FROM cache_data
            WHERE key = ?
            """,
            (key,)
        )

        result = self.cursor.fetchone()

        if result is None:
            return None

        value, expiry = result

        # TTL check from DB
        if expiry is not None:

            if time.time() > expiry:

                self.delete(key)

                return None

        return value

    def delete(self, key):

        self.cursor.execute(
            """
            DELETE FROM cache_data
            WHERE key = ?
            """,
            (key,)
        )

        self.connection.commit()

    def load_all_valid_keys(self):

        current_time = time.time()

        self.cursor.execute(
            """
            SELECT key, value, expiry
            FROM cache_data
            """
        )

        rows = self.cursor.fetchall()

        valid_rows = []

        for key, value, expiry in rows:

            if expiry is not None:

                if current_time > expiry:

                    self.delete(key)

                    continue

            valid_rows.append(
                (key, value, expiry)
            )

        return valid_rows

    def health_check(self):

        try:

            self.cursor.execute(
                "SELECT 1"
            )

            return True

        except Exception:

            return False