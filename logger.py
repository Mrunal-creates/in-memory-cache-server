import logging
import os

# Create logs folder automatically
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/cache.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("CacheLogger")