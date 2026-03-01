# Design Twitter / News Feed — Timeline & Fan-out

## When Asked
"Design Twitter", "Design Instagram feed", "Design a news feed", "Design a social network timeline"

## Requirements

```
FUNCTIONAL:
  - Post tweets/content
  - Follow/unfollow users
  - Home timeline (feed of posts from people you follow)
  - Like, retweet, comment

NON-FUNCTIONAL:
  - Feed generation: <200ms latency
  - Scale: 300M DAU, avg 300 follows, ~500M tweets/day
  - Availability > consistency (seeing a tweet 5 sec late is fine)
```

## The Core Problem: Fan-out

```
When User A posts a tweet, how do all followers see it?

TWO APPROACHES:

  FAN-OUT ON WRITE (Push model):
    When A tweets → push to every follower's feed cache
    ✓ Read is instant (feed is pre-computed)
    ✗ Expensive writes (celebrity with 50M followers → 50M writes)

    Tweet → Fanout Service → write to Redis list for each follower
    follower_1_feed: [tweet_id_new, tweet_id_old, ...]
    follower_2_feed: [tweet_id_new, tweet_id_old, ...]

  FAN-OUT ON READ (Pull model):
    When follower opens feed → query: "get latest from everyone I follow"
    ✓ Write is instant (just store the tweet)
    ✗ Read is slow (query N users, merge, sort)

    SELECT * FROM tweets
    WHERE user_id IN (SELECT following_id FROM follows WHERE user_id = me)
    ORDER BY created_at DESC LIMIT 20

HYBRID (Twitter's actual approach):
  - Regular users (<10K followers): fan-out on write
  - Celebrities (>10K followers): fan-out on read

  When you open your feed:
    1. Get pre-computed feed from Redis (pushed by non-celebrity follows)
    2. Fetch latest tweets from celebrities you follow (pulled on demand)
    3. Merge, sort, return
```

## High-Level Architecture

```
  ┌─────────┐    ┌──────────┐    ┌───────────────┐
  │ Client  │───→│ API GW   │───→│ Tweet Service  │──→ Tweet DB
  └────┬────┘    └──────────┘    └───────┬───────┘
       │                                 │ publish event
       │                          ┌──────▼───────┐
       │                          │ Fanout Service│
       │                          └──────┬───────┘
       │                                 │ write to each follower's feed
       │         ┌──────────┐     ┌──────▼───────┐
       └────────→│Feed Service│←──│ Feed Cache    │
                 └──────────┘     │ (Redis)       │
                                  └──────────────┘
```

## Key Components

```
TWEET STORAGE (SQL + NoSQL):
  SQL (PostgreSQL):
    tweets: id, user_id, content, media_urls, created_at, like_count, retweet_count
    users: id, username, follower_count
    follows: follower_id, following_id, created_at

  For high write volume:
    Shard tweets by user_id
    Or use Cassandra: partition by user_id, cluster by timestamp

FEED CACHE (Redis):
  Key: feed:{user_id}
  Value: sorted set of tweet_ids (sorted by timestamp)
  Keep only last 800 tweet IDs per user

  When user opens feed:
    1. ZREVRANGE feed:user123 0 19  → latest 20 tweet IDs
    2. MGET tweet:id1, tweet:id2... → fetch tweet details
    3. Return enriched feed

FANOUT SERVICE:
  1. Tweet published → Kafka event
  2. Fanout worker: get all followers of author
  3. For each follower: ZADD feed:{follower_id} {timestamp} {tweet_id}
  4. Trim: ZREMRANGEBYRANK feed:{follower_id} 0 -801 (keep latest 800)

  Optimization:
    - Only fan out to ACTIVE users (logged in last 7 days)
    - Inactive users → pull on demand when they return

TIMELINE RANKING:
  Simple: reverse chronological (newest first)
  Smart: ML ranking model considers:
    - Recency
    - Author engagement score
    - Your interaction history with author
    - Content type preference
    - Trending score
```

## Deep Dive: Social Graph

```
FOLLOW RELATIONSHIP:
  follows table: (follower_id, following_id)

  "Who do I follow?"   → WHERE follower_id = me
  "Who follows me?"    → WHERE following_id = me

  Index both columns.
  At scale: use a graph database or adjacency list in Redis

  Redis sets:
    following:user123 = {user456, user789, ...}
    followers:user456 = {user123, user111, ...}

  SADD following:user123 user456  → follow
  SREM following:user123 user456  → unfollow
  SMEMBERS following:user123      → who I follow
  SCARD followers:user456         → follower count
```

## Scaling

```
SHARDING:
  Tweets: shard by user_id (all tweets from one user on same shard)
  Feed cache: shard by user_id
  Social graph: shard by user_id

HOT USERS (celebrities):
  - Don't fan-out their tweets (pull model instead)
  - Cache their latest tweets aggressively
  - Separate infrastructure for viral content

MEDIA:
  - Images/videos stored in S3
  - Served via CDN
  - Tweet stores media_url, not media itself
```
