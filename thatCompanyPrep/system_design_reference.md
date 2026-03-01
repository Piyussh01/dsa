# System Design Quick Reference
# For 30-min rounds

## The Framework (Memorize This)

```
30-MIN BREAKDOWN:
├── Requirements (3 min)
├── Estimation (2 min)
├── High-Level Design (8 min)
├── Detailed Design (12 min)
└── Scaling/Trade-offs (5 min)
```

---

## Step 1: Requirements (3 min)

**Functional Requirements (what it does):**
- "Users should be able to..."
- List 3-5 core features
- Clarify what's OUT of scope

**Non-Functional Requirements (how well it does it):**
- Scale: DAU, requests/sec
- Latency: <100ms, <1s?
- Availability: 99.9%? 99.99%?
- Consistency: Strong or eventual?

**Questions to Ask:**
- "How many users? DAU?"
- "Read-heavy or write-heavy?"
- "What's the expected data size?"
- "Global or single region?"

---

## Step 2: Estimation (2 min)

**Traffic:**
```
DAU = 10M
Requests/day = DAU × requests_per_user = 10M × 10 = 100M
QPS = 100M / 86400 ≈ 1200 QPS
Peak QPS = QPS × 3 = 3600 QPS
```

**Storage:**
```
Records/day = 100M
Record size = 1KB
Storage/day = 100GB
Storage/year = 36TB
```

**Bandwidth:**
```
Bandwidth = QPS × data_size = 1200 × 1KB = 1.2 MB/s
```

**Quick Math:**
- 1 day ≈ 100K seconds
- 1 year ≈ 30M seconds
- 1M requests/day ≈ 12 QPS

---

## Step 3: High-Level Design (8 min)

**Draw These Components:**

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐
│ Clients │────▶│Load Balancer │────▶│ App Servers │
└─────────┘     └──────────────┘     └─────────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
            ┌───────────┐           ┌───────────┐           ┌───────────┐
            │   Cache   │           │  Database │           │   Queue   │
            │  (Redis)  │           │(PostgreSQL)│          │  (Kafka)  │
            └───────────┘           └───────────┘           └───────────┘
                                          │
                                    ┌─────┴─────┐
                                    │           │
                                    ▼           ▼
                              ┌─────────┐ ┌─────────┐
                              │ Primary │ │Replica  │
                              └─────────┘ └─────────┘
```

**Data Flow:**
1. Client → Load Balancer
2. Load Balancer → App Server
3. App Server checks Cache
4. Cache miss → Database
5. Async tasks → Queue → Workers

---

## Step 4: Detailed Design (12 min)

### Database Schema (Always Draw This)

Example for URL Shortener:
```sql
urls (
    id          BIGINT PRIMARY KEY,
    short_code  VARCHAR(7) UNIQUE,
    long_url    VARCHAR(2048),
    user_id     BIGINT,
    created_at  TIMESTAMP,
    expires_at  TIMESTAMP,
    click_count INT DEFAULT 0
)
INDEX: short_code (for lookups)
INDEX: user_id (for user's URLs)
```

### API Endpoints (RESTful)

```
POST /api/urls           - Create short URL
GET  /api/urls/{code}    - Redirect to long URL
GET  /api/urls/{code}/stats - Get analytics
DELETE /api/urls/{code}  - Delete URL
```

### Key Algorithms/Logic

Pick 1-2 to dive deep:
- ID generation (UUID, Snowflake, base62 encoding)
- Caching strategy (write-through, write-behind, cache-aside)
- Sharding key selection
- Consistency model

---

## Step 5: Scaling & Trade-offs (5 min)

### Scaling Techniques

| Problem | Solution |
|---------|----------|
| High read traffic | Read replicas, caching |
| High write traffic | Sharding, write queues |
| Large data | Sharding, archival |
| Global users | CDN, geo-replication |
| Hot spots | Consistent hashing |

### Common Trade-offs

- **Consistency vs Availability** (CAP theorem)
- **Latency vs Throughput**
- **Cost vs Performance**
- **Complexity vs Flexibility**

### Bottlenecks to Address

1. Database as bottleneck → Add cache, read replicas
2. Single point of failure → Add redundancy
3. Slow writes → Async processing with queues
4. Hot partitions → Better sharding key

---

## Common System Designs

### 1. URL Shortener
- **Key insight:** Base62 encode auto-increment ID
- **Scale:** Cache popular URLs, shard by hash
- **Gotcha:** Collision handling

### 2. Rate Limiter
- **Key insight:** Sliding window counter in Redis
- **Scale:** Distributed counter with eventual consistency
- **Gotcha:** Race conditions

### 3. Notification System
```
Producer → Kafka → Consumer Groups → {Email, Push, SMS, In-App}
                          ↓
                    Preference Service
                          ↓
                    Template Service
```

### 4. Real-time Collaboration (Accord-relevant!)
- **Key insight:** Operational Transform or CRDTs
- **Components:** WebSocket servers, presence service, conflict resolution
- **Scale:** Room-based sharding, session affinity

### 5. Analytics Dashboard
- **Key insight:** Pre-aggregate data, time-series DB
- **Components:** Event ingestion → Stream processing → Data warehouse
- **Scale:** Columnar storage, materialized views

---

## Database Selection Guide

| Use Case | Database | Why |
|----------|----------|-----|
| General CRUD | PostgreSQL | ACID, flexible |
| High read volume | PostgreSQL + Redis | Caching |
| Time-series data | InfluxDB, TimescaleDB | Optimized for time |
| Full-text search | Elasticsearch | Inverted index |
| Graph relationships | Neo4j | Traversal queries |
| Massive scale writes | Cassandra | Write-optimized |
| Document storage | MongoDB | Schema flexibility |

---

## Vocabulary to Use

**Sound Smart:**
- "We need to think about the read-to-write ratio..."
- "Let's consider horizontal vs vertical scaling..."
- "For consistency, we could use..."
- "The bottleneck here would be..."
- "We can use eventual consistency because..."

**When Stuck:**
- "Let me think about the data flow..."
- "What's the most expensive operation here?"
- "Where would we see hot spots?"

---

## Quick Formulas

```python
# Server capacity
servers_needed = peak_qps / qps_per_server

# Storage growth
yearly_storage = daily_writes × record_size × 365

# Cache size
cache_size = working_set_size × 0.2  # 20% rule

# Replication lag tolerance
max_lag = request_timeout - processing_time
```

---

## Red Flags to Avoid

❌ Not asking clarifying questions  
❌ Jumping straight to database schema  
❌ Single database without considering scale  
❌ Ignoring failure scenarios  
❌ Not discussing trade-offs  
❌ Over-engineering for the stated scale  
