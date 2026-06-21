from cache import Cache
from cleaner import Cleaner
import time


cache = Cache(capacity=3)

cleaner = Cleaner(cache)

cleaner.start()

print("\n=== CACHE STARTED ===\n")

cache.set("A", 100, ttl=5)

cache.set("B", 200, ttl=10)

cache.set("C", 300, ttl=15)

print("A =", cache.get("A"))

# A becomes recently used
cache.get("A")

# Capacity exceeded
cache.set("D", 400)

print("\nWaiting 20 seconds...\n")

time.sleep(20)

print("A =", cache.get("A"))

print("B =", cache.get("B"))

print("C =", cache.get("C"))

print("D =", cache.get("D"))

print("\n=== CACHE FINISHED ===")