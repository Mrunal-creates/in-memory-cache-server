from fastapi import Header, HTTPException
from logger import logger


API_KEY = "mysecretkey123"


def verify_api_key(
    x_api_key: str = Header(...)
):

    if x_api_key != API_KEY:
        logger.warning("Unauthorized Access Attempt")

        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return True