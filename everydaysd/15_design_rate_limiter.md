# Design Rate Limiter

## When Asked
"Design a rate limiter", "Design an API throttling system", "How would you implement rate limiting?"

## Requirements

```
FUNCTIONAL:
  - Limit requests per user/IP/API key
  - Different limits for different endpoints
  - Return 429 when limit exceeded
  - Distributed (works across multiple API servers)

NON-FUNCTIONAL:
  - Low latency (<1ms overhead per request)
  - Accurate (no significant over/under counting)
  - Fault tolerant (if rate limiter dies, traffic still flows)
```

## Where to Place It

```
  Client → [Rate Limiter] → API Server → DB

  OPTIONS:
  1. API Gateway level (AWS API Gateway, Kong)
     ✓ Centralized, easy to manage
     ✓ Blocks traffic before hitting your servers

  2. Middleware in API server
     ✓ More control, access to user context
     ✗ Each server needs to share state

  3. Separate rate limiter service
     ✓ Reusable across services
     ✗ Added network hop

  RECOMMENDATION: API Gateway for simple rules,
  middleware + Redis for complex per-user logic.
```

## Algorithms

```
1. TOKEN BUCKET ★ (most common, what AWS/Stripe use)
   - Bucket starts with N tokens
   - Each request takes 1 token
   - Tokens refill at rate R per second
   - No tokens → reject

   ✓ Allows bursts (up to bucket capacity)
   ✓ Smooth rate over time
   ✓ Simple to implement

   REDIS IMPLEMENTATION:
     Key: ratelimit:{user_id}
     Fields: tokens (float), last_refill (timestamp)

     def is_allowed(user_id, capacity, refill_rate):
         key = f"ratelimit:{user_id}"
         now = time.time()

         # Lua script for atomicity
         tokens, last = redis.hmget(key, "tokens", "last")
         if tokens is None:
             tokens, last = capacity, now

         # Refill
         elapsed = now - float(last)
         tokens = min(capacity, float(tokens) + elapsed * refill_rate)

         if tokens >= 1:
             tokens -= 1
             redis.hmset(key, {"tokens": tokens, "last": now})
             redis.expire(key, 3600)
             return True
         else:
             redis.hmset(key, {"tokens": tokens, "last": now})
             return False


2. SLIDING WINDOW LOG
   - Store timestamp of every request
   - Count requests in [now - window, now]
   - If count >= limit → reject

   REDIS: sorted set with timestamps
     ZADD ratelimit:user123 {timestamp} {request_id}
     ZREMRANGEBYSCORE ratelimit:user123 0 {now - window}
     count = ZCARD ratelimit:user123
     if count >= limit: reject

   ✓ Very precise
   ✗ Memory heavy (stores every request timestamp)


3. SLIDING WINDOW COUNTER (hybrid)
   - Combine fixed window counts with weighted overlap
   - Current window count + previous window count × overlap %

   Example: 60-sec window, limit 100
     Previous minute: 80 requests
     Current minute (25 sec in): 30 requests
     Weighted: 30 + 80 × (35/60) = 30 + 47 = 77 < 100 → allow

   ✓ Low memory (just two counters)
   ✓ Good enough precision
   ✓ Simple


4. FIXED WINDOW COUNTER
   - Count requests per time window (e.g., per minute)
   - INCR ratelimit:user123:1709123400, EXPIRE 60

   ✓ Simplest, low memory
   ✗ Boundary problem: 100 requests at :59 + 100 at :00 = 200 in 2 seconds


5. LEAKY BUCKET
   - Queue requests, process at fixed rate
   - Queue full → reject
   ✓ Smooth output rate
   ✗ Bursty input gets delayed, not rejected
```

## Distributed Rate Limiting

```
PROBLEM: 5 API servers, each with local counter.
User sends 20 requests, each server sees only 4. Nobody rate limits.

SOLUTION: Centralized counter in Redis
  All servers check/increment the SAME Redis key.
  Redis is fast enough (<1ms per operation).

  RACE CONDITION: Two servers read count=99, both increment, count=100.
  But limit is 100 → one should have been rejected.

  FIX: Use Redis Lua scripts (atomic operations):
    local count = redis.call('INCR', KEYS[1])
    if count == 1 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    return count

REDIS FAILURE:
  Option A: Allow all traffic (fail open) → better user experience
  Option B: Block all traffic (fail closed) → more secure
  Usually: fail open + alert engineers
```

## Multi-Level Rate Limits

```
Apply multiple rules simultaneously:

  Per-second: 10 requests/sec   (burst protection)
  Per-minute: 200 requests/min  (sustained load)
  Per-hour:   5000 requests/hr  (abuse prevention)
  Per-day:    50000 requests/day (quota)

  Request must pass ALL levels to be allowed.

PER-ENDPOINT LIMITS:
  POST /api/login:  5/min   (brute force protection)
  GET  /api/search: 30/min  (expensive query)
  GET  /api/profile: 100/min (cheap query)
```

## Response Headers

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1709123460

Always tell the client:
  - What the limit is
  - How many requests remain
  - When the limit resets
```
