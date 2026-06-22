import threading
import time
import heapq
from logger import logger

class Cleaner:

    def __init__(self, cache):

        self.cache = cache

    def start(self):

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

    def run(self):

        while True:

            current_time = time.time()

            with self.cache.lock:

                while self.cache.expiry_heap:

                    expiry, key = self.cache.expiry_heap[0]

                    # earliest item has not expired yet
                    if current_time < expiry:
                        break

                    heapq.heappop(
                        self.cache.expiry_heap
                    )

                    if key in self.cache.store:

                        logger.info(
                            f"EXPIRED Key={key}"
                        )
                        del self.cache.store[key]

                        self.cache.database.delete(key)

                        self.cache.expired_keys += 1

            time.sleep(1)