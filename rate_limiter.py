import time
from collections import defaultdict
from fastapi import HTTPException
from logger import logger


class RateLimiter:

    def __init__(self):

        self.requests = defaultdict(list)

        self.limit = 100

        self.window = 60

    def check(self, api_key):

        current_time = time.time()

        valid_requests = []

        for request_time in self.requests[api_key]:

            if current_time - request_time < self.window:

                valid_requests.append(
                    request_time
                )

        self.requests[api_key] = valid_requests

        if len(valid_requests) >= self.limit:

            logger.warning(
                f"Rate Limit Exceeded for {api_key}"
            )

            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        self.requests[api_key].append(
            current_time
        )