# In-Memory Key-Value Store

A production-inspired in-memory caching system built from scratch using Python and FastAPI. The project simulates several core concepts used in modern distributed caching solutions such as Redis, Memcached, and high-performance backend systems.

The primary objective of this project is to provide extremely fast key-value data access while supporting automatic expiration, persistence, eviction strategies, monitoring, authentication, and a real-time management dashboard.

Unlike a simple CRUD application, this project focuses heavily on data structures, system design, backend engineering, concurrency, and performance optimization.

---

## Project Overview

Applications frequently access the same data repeatedly. Querying a database every time can become expensive and increase response times. To solve this problem, modern systems use caches that store frequently accessed data in memory.

This project implements a complete cache server capable of:

* Storing key-value pairs in memory
* Supporting configurable Time-To-Live (TTL)
* Automatically removing expired entries
* Persisting data to SQLite
* Applying Least Recently Used (LRU) eviction
* Exposing REST APIs for cache operations
* Securing endpoints using API Key Authentication
* Limiting request rates
* Providing operational metrics
* Visualizing system activity through a web dashboard

The project combines algorithmic concepts with practical backend engineering principles commonly used in large-scale software systems.

---

## Core Features

### High-Speed In-Memory Storage

Data is stored in memory using optimized Python data structures to provide near O(1) lookup performance.

Operations supported:

* Create
* Read
* Update
* Delete

---

### Time-To-Live (TTL) Support

Each key can be assigned an expiration time.

Example:

* Session Tokens
* OTP Storage
* Temporary User Data
* Cached API Responses

Once the TTL expires, the key is automatically removed.

---

### Automatic Expiration Cleanup

A dedicated background cleaner thread continuously monitors expiration times and removes stale records without user intervention.

This mimics the behavior of production cache systems.

---

### LRU (Least Recently Used) Eviction

When cache capacity is reached, the system automatically removes the least recently accessed item.

Benefits:

* Efficient memory utilization
* Better cache hit rates
* Production-like cache management

---

### Min Heap Expiration Optimization

Instead of scanning the entire cache for expired entries, a Min Heap is used to efficiently track the next key scheduled for expiration.

Advantages:

* Faster expiration checks
* Reduced CPU usage
* Better scalability

---

### Persistent Storage Using SQLite

While the cache primarily operates in memory, data is also persisted to SQLite.

Benefits:

* Data survives application restarts
* Simulates cache persistence strategies
* Enables database fallback

---

### Database Recovery

If data is not present in memory but exists in SQLite, the system automatically retrieves it and restores it back into the cache.

This demonstrates cache warming and fallback mechanisms commonly used in production environments.

---

### Thread-Safe Operations

Multiple requests may attempt to modify cache contents simultaneously.

To prevent race conditions:

* Thread Locks are used
* Shared resources are protected
* Concurrent access remains safe

---

### REST API Layer

The cache can be interacted with through REST APIs built using FastAPI.

Supported endpoints:

* Set Key
* Get Key
* Delete Key
* Health Status
* Metrics
* Dashboard

The API layer makes the cache accessible to external applications and services.

---

### API Key Authentication

Protected endpoints require valid API keys.

This prevents unauthorized access and demonstrates basic backend security practices.

---

### Rate Limiting

The server tracks incoming requests and restricts excessive traffic.

Benefits:

* Prevents abuse
* Protects resources
* Demonstrates backend traffic control

---

### Logging System

All critical operations are logged.

Examples:

* Cache Hits
* Cache Misses
* Evictions
* Expirations
* Unauthorized Access Attempts

Logs help with monitoring and debugging.

---

### Real-Time Metrics

The cache continuously tracks operational statistics.

Examples:

* Total Hits
* Total Misses
* Database Hits
* Evictions
* Expired Keys
* Cache Size
* Capacity Usage

These metrics provide visibility into cache effectiveness.

---

### Health Monitoring

A dedicated health endpoint provides operational information such as:

* Server Status
* Uptime
* Request Statistics
* Cache Performance

Useful for monitoring and maintenance.

---

### Interactive Dashboard

The project includes a web-based dashboard built using:

* HTML
* CSS
* JavaScript
* Jinja2 Templates

Dashboard Features:

* Set Cache Values
* Retrieve Keys
* Delete Keys
* View Metrics
* View Health Information
* Real-Time Analytics
* Live Charts

This provides a user-friendly interface for managing cache operations.

---

## Data Structures and Algorithms Used

This project intentionally focuses on fundamental computer science concepts.

### Hash Map

Used for:

* O(1) Key Lookup
* O(1) Insertions
* O(1) Updates

### Ordered Dictionary

Used to maintain access order and implement LRU behavior.

### Min Heap

Used to efficiently manage key expiration scheduling.

### Thread Locks

Used to ensure safe concurrent access.

These structures are frequently discussed in software engineering interviews and system design discussions.

---

## Architecture

User Request

↓

FastAPI API Layer

↓

Authentication & Rate Limiting

↓

In-Memory Cache

↓

TTL Validation

↓

LRU Management

↓

SQLite Persistence Layer

↓

Metrics & Logging

↓

Dashboard Visualization

---

## Tech Stack

### Backend

* Python
* FastAPI

### Storage

* SQLite

### Data Structures

* OrderedDict
* Heap Queue (Min Heap)
* Hash Maps

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2

### Monitoring

* Logging
* Metrics Tracking
* Health Checks

---

## Learning Outcomes

This project demonstrates practical understanding of:

* Data Structures & Algorithms
* Backend Development
* API Design
* System Design Fundamentals
* Concurrency
* Caching Mechanisms
* Database Persistence
* Authentication
* Monitoring & Observability
* Performance Optimization

---

## Future Improvements

Potential production-grade enhancements include:

* Redis Integration
* PostgreSQL Support
* Multi-Level Caching
* Distributed Cache Nodes
* Consistent Hashing
* Cache Replication
* Prometheus Metrics Export
* Docker & Kubernetes Deployment
* JWT Authentication
* WebSocket-Based Live Monitoring

---

## Why This Project Matters

Caching is one of the most important performance optimization techniques used in modern software systems.

This project goes beyond basic CRUD development and focuses on concepts that are directly relevant to backend engineering, distributed systems, infrastructure development, and large-scale application design.

By building the cache from scratch, the project demonstrates not only framework usage but also an understanding of the underlying algorithms and architectural decisions that power real-world systems.


<img width="1902" height="978" alt="image" src="https://github.com/user-attachments/assets/8cfdb208-5c0c-4932-bb88-7503ff38bf3f" />

<img width="1882" height="977" alt="image" src="https://github.com/user-attachments/assets/0ffdc943-1d53-45e0-8b51-2d6ac85aea09" />

<img width="1887" height="963" alt="image" src="https://github.com/user-attachments/assets/04ca88c8-88f2-4fb0-bd42-1c1ea9c5cb07" />

<img width="1880" height="972" alt="image" src="https://github.com/user-attachments/assets/0e463cc5-4781-4d02-9ea5-601d7595016f" />

