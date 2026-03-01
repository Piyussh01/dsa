# Caching — Strategies, Redis, Eviction, Invalidation

## Why Cache?
```
Database: 5-10ms per query, ~10K QPS max
Redis:    <1ms per query, ~100K QPS

Cache = store frequently accessed data in fast storage (RAM)
Trade: memory cost + stale data risk → massive speed gain
```

## Where to Cache

```
CLIENT SIDE:     Browser cache, mobile app cache
                 → HTTP headers: Cache-Control, ETag, Last-Modified

CDN:             Static assets cached at edge locations
                 → Images, videos, JS/CSS bundles

APPLICATION:     In-memory cache in the app (local)
                 → Fast but not shared across servers
                 → python: functools.lru_cache, dict

DISTRIBUTED:     Redis, Memcached (shared across servers)
                 → Most common in system design interviews
                 → Shared state, survives server restarts (Redis)

DATABASE:        Query cache, buffer pool
                 → Usually handled by the DB itself
```

## Cache Strategies (READ)

```
1. CACHE-ASIDE (Lazy Loading) — most common
   ┌────────┐  miss   ┌────┐  query  ┌────┐
   │ Client │───────→ │Cache│        │ DB │
   │        │←───────  │    │←────── │    │
   │        │  return  │    │ fill   │    │
   └────────┘         └────┘        └────┘

   Read:  Check cache → miss → read DB → write to cache → return
   Write: Write to DB → delete cache entry (or let it expire)

   ✓ Only caches what's actually requested
   ✓ Cache failure doesn't break reads (fallback to DB)
   ✗ First request is always a cache miss
   ✗ Cache can become stale

2. READ-THROUGH
   Same as cache-aside but the CACHE talks to DB (not the app).
   App only talks to cache. Cache handles misses internally.
   ✓ Simpler app code
   ✗ Cache library must support it

3. WRITE-THROUGH
   Write:  Write to cache AND DB simultaneously
   ✓ Cache is always fresh
   ✗ Higher write latency (two writes)
   ✗ Caches data that may never be read

4. WRITE-BEHIND (Write-Back)
   Write:  Write to cache → async write to DB later
   ✓ Super fast writes
   ✗ Risk of data loss if cache crashes before DB write
   ✗ Complex

5. WRITE-AROUND
   Write:  Write to DB only, cache fills on next read
   ✓ Doesn't pollute cache with write-once data
   ✗ First read after write is slow
```

### When to Use What
```
Read-heavy, tolerates staleness  → Cache-aside (default choice)
Read-heavy, needs freshness      → Read-through + short TTL
Write-heavy, speed critical      → Write-behind
Write-heavy, consistency needed  → Write-through
Write-once data                  → Write-around
```

## Eviction Policies

```
When cache is full, what do we kick out?

LRU (Least Recently Used):   remove what hasn't been accessed longest
  → Default choice for most systems. Redis default.

LFU (Least Frequently Used): remove what's accessed least often
  → Good when some items are permanently popular

FIFO (First In First Out):   remove oldest entry
  → Simple but not smart

TTL (Time To Live):          expire after N seconds
  → Not eviction per se, but controls staleness
  → Set TTL on every cache entry. No TTL = stale forever.

Random:                       remove random entry
  → Surprisingly decent. Used in some CPU caches.
```

## Cache Invalidation

```
THE HARD PROBLEM: keeping cache in sync with DB

STRATEGIES:
  1. TTL-based:     set expiry, tolerate staleness within window
  2. Event-based:   on DB write, publish event → consumer deletes cache
  3. Write-through: update cache on every write
  4. Manual purge:  API to explicitly clear cache entries

COMMON PATTERN (Cache-Aside):
  def get_user(user_id):
      user = redis.get(f"user:{user_id}")
      if user is None:
          user = db.query("SELECT * FROM users WHERE id = ?", user_id)
          redis.setex(f"user:{user_id}", 300, serialize(user))  # TTL 5 min
      return user

  def update_user(user_id, data):
      db.update("UPDATE users SET ... WHERE id = ?", user_id)
      redis.delete(f"user:{user_id}")  # invalidate, don't update
```

## Cache Stampede / Thundering Herd

```
PROBLEM: Popular cache key expires → 1000 servers all hit DB at once

SOLUTIONS:
  1. Lock: first request locks, others wait
     if not redis.get(key):
         if redis.setnx(lock_key, 1, ex=5):  # acquire lock
             data = db.query(...)
             redis.set(key, data, ex=300)
         else:
             sleep(0.1)  # wait and retry

  2. Early refresh: refresh cache BEFORE it expires
     Store (value, expiry). If expiry is near, async refresh.

  3. Never expire: always keep in cache, update via events
```

## Redis Specific

```
DATA STRUCTURES:
  String:     simple key-value, counters (INCR)
  List:       queues, recent items
  Set:        unique items, membership check
  Sorted Set: leaderboards, rankings (score-based)
  Hash:       object with fields (user profile)

COMMON USE CASES:
  Sessions:      SET session:abc123 {user_data} EX 3600
  Rate limiting: INCR requests:user:123, EXPIRE 60
  Leaderboard:   ZADD leaderboard score user_id
  Pub/Sub:       PUBLISH channel message
  Distributed lock: SET lock:resource NX EX 5

PERSISTENCE:
  RDB: snapshot to disk periodically (fast restart, some data loss)
  AOF: append every write to log (slower, less data loss)
  Both: RDB for fast restart + AOF for safety
```
