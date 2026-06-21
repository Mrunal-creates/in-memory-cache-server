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

        self.evictions = 0

        self.expired_keys = 0

        self.database_hits = 0

    def set(self, key, value, ttl=None):

        with self.lock:

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

            self.database.save(key, value)

            logger.info(f"SET Key={key}")

            if len(self.store) > self.capacity:

                removed_key, _ = self.store.popitem(last=False)

                self.evictions += 1

                logger.info(f"LRU EVICTION Key={removed_key}")

    def get(self, key):

        with self.lock:

            data = self.store.get(key)

            if data is None:

                logger.info(f"CACHE MISS Key={key}")

                self.misses += 1

                db_value = self.database.get(key)

                if db_value is not None:

                    self.database_hits += 1

                    self.store[key] = {
                        "value": db_value,
                        "expiry": None
                    }

                    return db_value

                return None

            expiry = data["expiry"]

            if expiry is not None and time.time() > expiry:

                del self.store[key]

                return None

            self.store.move_to_end(key)

            self.hits += 1

            logger.info(f"CACHE HIT Key={key}")

            return data["value"]

    def delete(self, key):

        logger.info(f"DELETE Key={key}")

        with self.lock:

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