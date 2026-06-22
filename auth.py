from fastapi import Header, HTTPException
from logger import logger
from rate_limiter import RateLimiter


API_KEY = "mysecretkey123"
limiter = RateLimiter()


def verify_api_key(
    x_api_key: str = Header(...)
):

    if x_api_key != API_KEY:

        logger.warning(
            "Unauthorized Access Attempt"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    limiter.check(x_api_key)

    return True