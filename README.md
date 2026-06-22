# In-Memory Key Value Store

A Redis-inspired in-memory cache server built using Python and FastAPI.

## Features

- O(1) Key-Value Storage
- LRU Eviction Policy
- TTL Expiration Support
- Min Heap Expiry Optimization
- SQLite Persistence
- Background Cleanup Thread
- API Key Authentication
- Rate Limiting
- Health Monitoring
- Metrics Dashboard
- Interactive Frontend Dashboard
- Logging and Observability

## Tech Stack

- Python
- FastAPI
- SQLite
- HTML
- CSS
- JavaScript
- Jinja2

## API Endpoints

- POST /set
- GET /get/{key}
- DELETE /delete/{key}
- GET /metrics
- GET /health

## Run Locally

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

Open:

```text
http://127.0.0.1:8000/dashboard
```
