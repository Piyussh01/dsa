# Design URL Shortener — TinyURL / Bit.ly

## When Asked
"Design TinyURL", "Design a URL shortener", "Design Bit.ly"

## Requirements

```
FUNCTIONAL:
  - Given a long URL, generate a short URL
  - Redirect short URL → long URL
  - Custom aliases (optional)
  - Expiration (optional)
  - Analytics: click count, geography (optional)

NON-FUNCTIONAL:
  - Low latency redirect (<50ms)
  - High availability (redirect must ALWAYS work)
  - Scale: 100M URLs created/day, 10:1 read/write ratio = 1B redirects/day
```

## Back-of-Envelope

```
Write: 100M/day ÷ 100K = 1K QPS
Read:  1B/day ÷ 100K = 10K QPS

Short URL length:
  Using base62 (a-z, A-Z, 0-9) = 62 characters
  7 characters = 62^7 = 3.5 trillion unique URLs (enough for decades)

Storage:
  Each URL entry ≈ 500 bytes (short_url + long_url + metadata)
  100M/day × 500B × 365 days × 5 years ≈ 90TB
```

## High-Level Architecture

```
  ┌─────────┐    ┌──────────┐    ┌─────────────┐    ┌─────────┐
  │ Client  │───→│ API GW   │───→│ URL Service  │───→│  DB     │
  └─────────┘    │(rate lim)│    └──────┬───────┘    │(Postgres)│
                 └──────────┘           │            └─────────┘
                                   ┌────▼────┐
                                   │  Cache  │
                                   │ (Redis) │
                                   └─────────┘
```

## Key Design Decisions

```
URL GENERATION — Three approaches:

  1. HASH + TRUNCATE:
     hash = MD5(long_url)[:7]  or SHA256[:7]
     ✓ Simple, deterministic (same URL → same hash)
     ✗ Collisions (need to check and retry)

  2. BASE62 ENCODE AN ID (recommended):
     Auto-increment ID in DB → convert to base62
     ID = 123456789 → base62 = "8M0kX"
     ✓ No collisions
     ✓ Predictable, simple
     ✗ Sequential (people can guess next URL)
     ✗ Single point of failure for ID generation

     def to_base62(num):
         chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
         result = []
         while num > 0:
             result.append(chars[num % 62])
             num //= 62
         return ''.join(reversed(result))

  3. PRE-GENERATED KEY SERVICE:
     Background service generates random 7-char keys in advance
     Store in a "key pool" table
     When new URL needed → grab a key from pool
     ✓ No collision, no computation at request time
     ✓ Keys are random (not guessable)
     ✗ Need to manage the key pool

REDIRECT FLOW:
  1. Client: GET /abc1234
  2. Check Redis cache → hit? Return 301/302 redirect
  3. Cache miss → query DB → cache result → return redirect
  4. Increment analytics counter (async, via Kafka)

301 vs 302:
  301 Permanent Redirect: browser caches, won't hit your server again
    ✓ Less load on your server
    ✗ Can't track clicks (browser goes directly next time)

  302 Temporary Redirect: browser hits your server every time
    ✓ Can track every click
    ✗ More load

  USE 302 if you need analytics (which you usually do).
```

## Database Schema

```sql
CREATE TABLE urls (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code  VARCHAR(7) UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    user_id     BIGINT,
    created_at  TIMESTAMP DEFAULT NOW(),
    expires_at  TIMESTAMP,
    click_count BIGINT DEFAULT 0
);

INDEX on short_code (for redirect lookups)
INDEX on user_id (for "my URLs" queries)
```

## Scaling

```
CACHING:
  Cache hot URLs in Redis. 20% of URLs get 80% of traffic.
  Cache key: short_code → long_url
  TTL: 24 hours (popular URLs stay cached)

DATABASE:
  Read-heavy → add read replicas
  Very high scale → shard by short_code hash
  Or use DynamoDB (key-value, auto-scales)

ID GENERATION AT SCALE:
  Problem: auto-increment doesn't work across multiple DB servers
  Solutions:
    a) Twitter Snowflake: distributed ID generation
       64 bits = timestamp(41) + machine_id(10) + sequence(12)
    b) UUID: globally unique, but long (128 bits → bad for short URLs)
    c) Zookeeper: assign ID ranges to servers (server 1 gets 1-1M, server 2 gets 1M-2M)
```
