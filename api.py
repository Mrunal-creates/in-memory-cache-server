from fastapi import FastAPI
from pydantic import BaseModel

from cache import Cache
from cleaner import Cleaner
from fastapi import Depends
from auth import verify_api_key


app = FastAPI(
    title="In-Memory KV Store",
    version="1.0.0"
)

cache = Cache(capacity=100)

cleaner = Cleaner(cache)

cleaner.start()


class CacheRequest(BaseModel):

    key: str

    value: str | int | float

    ttl: int | None = None


@app.get("/")
def home():

    return {
        "message": "Cache Server Running"
    }


@app.post("/set")
def set_value(request: CacheRequest, authorized: bool = Depends(verify_api_key)):

    cache.set(
        request.key,
        request.value,
        request.ttl
    )

    return {
        "status": "success"
    }


@app.get("/get/{key}")
def get_value(key: str, authorized: bool = Depends(verify_api_key)):

    value = cache.get(key)

    return {
        "key": key,
        "value": value
    }


@app.delete("/delete/{key}")
def delete_value(key: str, authorized: bool = Depends(verify_api_key)):

    cache.delete(key)

    return {
        "status": "deleted"
    }

@app.get("/stats")
def stats(authorized: bool = Depends(verify_api_key)):

    return cache.get_stats()