# The 4-Step Framework for ANY System Design Interview

You have 35-45 minutes. Spend them like this:

## Step 1: Requirements (5 min)
Ask clarifying questions. Nail down scope BEFORE drawing anything.

```
FUNCTIONAL: What does the system DO?
  - "Users can upload videos and watch them"
  - "Users can send messages in real-time"
  - Write down 3-5 core features. Ignore nice-to-haves.

NON-FUNCTIONAL: What qualities does it need?
  - Scale: How many users? DAU? Requests/sec?
  - Latency: Real-time? Seconds? Minutes?
  - Availability: Can we afford downtime?
  - Consistency: Can we show stale data briefly?
```

### Template Questions to Ask
```
"Who are the users and how many?"
"What are the core features vs nice-to-have?"
"Is this read-heavy or write-heavy?"
"Do we need real-time or is eventual consistency OK?"
"What's the expected scale? DAU, storage, bandwidth?"
```

## Step 2: Back-of-Envelope Estimation (3 min)
Quick math to justify your decisions later.

```
KNOW THESE NUMBERS:
  1 day       = 86,400 sec ≈ 100K sec
  1 million   = 10^6
  1 billion   = 10^9

  QPS (queries/sec) = DAU × queries_per_user / 100K
  Storage = users × data_per_user × retention_days
  Bandwidth = QPS × avg_response_size

EXAMPLE (YouTube):
  DAU = 500M
  Videos watched/day = 5 per user
  Watch QPS = 500M × 5 / 100K = 25K QPS
  Upload = 1% of users = 500 uploads/sec
  Avg video = 300MB → Storage/day = 500 × 300MB × 86400... just say "petabytes/year"
```

## Step 3: High-Level Design (15 min)
Draw the big boxes and arrows. Cover the happy path.

```
ALWAYS DRAW THESE:
  Client → Load Balancer → API Servers → Database
                                      → Cache
                                      → Message Queue (if async needed)
                                      → Object Storage (if files/media)

WALK THROUGH THE CORE FLOWS:
  1. Write path: "User uploads a video → goes through API → stored in S3 → metadata in DB"
  2. Read path: "User requests feed → check cache → query DB → return results"
```

## Step 4: Deep Dive (15 min)
Interviewer will pick 1-2 areas. Go deep.

```
COMMON DEEP DIVES:
  - Database schema design
  - How to scale to 10x / 100x
  - How to handle failures
  - Data consistency model
  - Caching strategy
  - Security / rate limiting

THIS IS WHERE YOU SHOW DEPTH:
  Don't just say "add a cache" — say "Redis with write-through,
  TTL of 5 min, LRU eviction, cache-aside for user profiles"
```

## The Golden Rule
**Start simple. Add complexity only when you explain WHY.**

Don't jump to microservices, Kafka, and 12 databases.
Start with a monolith + single DB. Then say:
"At 10K QPS this DB becomes a bottleneck, so I'd shard by user_id"

## Answer Structure for ANY Question
```
1. "Let me clarify the requirements..."
2. "Quick estimation: we're looking at ~X QPS, ~Y storage..."
3. "Here's the high-level architecture..." (draw boxes)
4. "Let me walk through the main flows..."
5. "For scaling, I'd focus on..." (deep dive)
6. "For failure handling..." (show you think about edge cases)
```
