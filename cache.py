from collections import OrderedDict
from database import Database
from logger import logger
import threading
import time
import heapq


class Cache:

    def __init__(self, capacity=5):

        self.capacity = capacity

        self.store = OrderedDict()

        self.lock = threading.Lock()

        self.database = Database()

        # Min Heap
        self.expiry_heap = []

        self.hits = 0

        self.misses = 0

        self.start_time = time.time()

        self.evictions = 0

        self.expired_keys = 0

        self.database_hits = 0

        self.total_requests = 0

        self.load_cache_from_database()

    def load_cache_from_database(self):

        rows = self.database.load_all_valid_keys()

        for key, value, expiry in rows:

            self.store[key] = {
                "value": value,
                "expiry": expiry
            }

            if expiry is not None:

                heapq.heappush(
                    self.expiry_heap,
                    (expiry, key)
                )

    def set(self, key, value, ttl=None):

        with self.lock:

            self.total_requests += 1

            expiry = None

            if ttl is not None:
                expiry = time.time() + ttl

                heapq.heappush(
                    self.expiry_heap,
                    (expiry, key)
                )

            if key in self.store:
                self.store.move_to_end(key)

            self.store[key] = {
                "value": value,
                "expiry": expiry
            }

            self.database.save(key, value, expiry)

            logger.info(f"SET Key={key}")

            if len(self.store) > self.capacity:

                removed_key, _ = self.store.popitem(last=False)

                self.evictions += 1

                logger.info(f"LRU EVICTION Key={removed_key}")

    def get(self, key):

        with self.lock:

            self.total_requests += 1

            data = self.store.get(key)

            if data is None:
                db_value = self.database.get(key)

                if db_value is not None:

                    self.database_hits += 1

                    self.store[key] = {
                        "value": db_value,
                        "expiry": None
                    }

                    return db_value

                self.misses += 1

                return None

            expiry = data["expiry"]

            if expiry is not None and time.time() > expiry:

                del self.store[key]

                self.database.delete(key)

                self.expired_keys += 1

                return None

            self.store.move_to_end(key)

            self.hits += 1

            logger.info(f"CACHE HIT Key={key}")

            return data["value"]

    def delete(self, key):

        logger.info(f"DELETE Key={key}")

        with self.lock:

            self.total_requests += 1

            if key in self.store:

                del self.store[key]

            self.database.delete(key)

            print(f"Deleted Key: {key}")

    def get_stats(self):

        with self.lock:

            return {

                "hits": self.hits,

                "misses": self.misses,

                "database_hits": self.database_hits,

                "evictions": self.evictions,

                "expired_keys": self.expired_keys,

                "current_size": len(self.store),

                "capacity": self.capacity
            }

    def get_hit_ratio(self):

        total = self.hits + self.misses

        if total == 0:
            return 0

        return round(
            (self.hits / total) * 100,
            2
        )

    def get_metrics(self):

        uptime = int(
            time.time() - self.start_time
        )

        hours = uptime // 3600

        minutes = (
            uptime % 3600
        ) // 60

        seconds = uptime % 60

        uptime_text = (
            f"{hours}h "
            f"{minutes}m "
            f"{seconds}s"
        )

        return {

            "uptime": uptime_text,

            "total_requests": self.total_requests,

            "hit_ratio": self.get_hit_ratio(),

            "hits": self.hits,

            "misses": self.misses,

            "database_hits": self.database_hits,

            "evictions": self.evictions,

            "expired_keys": self.expired_keys,

            "current_size": len(self.store),

            "capacity": self.capacity
        }