# Databases — SQL vs NoSQL, Sharding, Replication, Indexing

## SQL vs NoSQL — When to Use Which

```
SQL (PostgreSQL, MySQL):
  ✓ Structured data with relationships (users, orders, products)
  ✓ ACID transactions (money, inventory)
  ✓ Complex queries with JOINs
  ✓ Strong consistency
  ✗ Hard to scale horizontally
  ✗ Schema changes can be painful

NoSQL — FOUR TYPES:

  Key-Value (Redis, DynamoDB):
    ✓ Simple lookups by key
    ✓ Caching, sessions, leaderboards
    ✓ Blazing fast (100K+ QPS)
    ✗ No complex queries

  Document (MongoDB, Firestore):
    ✓ Semi-structured data (JSON documents)
    ✓ Flexible schema (each doc can differ)
    ✓ Nested objects, arrays
    ✓ Good for: user profiles, product catalogs, CMS
    ✗ No JOINs (denormalize instead)

  Wide-Column (Cassandra, HBase):
    ✓ Time-series, IoT, analytics
    ✓ Write-heavy workloads
    ✓ Distributed by design
    ✗ Limited query patterns

  Graph (Neo4j):
    ✓ Highly connected data (social networks, recommendations)
    ✓ "Friends of friends" queries
    ✗ Niche use case
```

### Quick Decision
```
Need transactions?        → SQL
Need flexible schema?     → Document DB
Need blazing fast cache?  → Key-Value
Need time-series writes?  → Wide-Column
Need relationship traversal? → Graph DB
Don't know?               → Start with PostgreSQL (it does 80% of things well)
```

## Indexing

```
WITHOUT INDEX:  Scan every row → O(n) → slow at scale
WITH INDEX:     B-tree lookup  → O(log n) → fast

WHAT TO INDEX:
  ✓ Columns you WHERE on (user_id, email, created_at)
  ✓ Columns you JOIN on (foreign keys)
  ✓ Columns you ORDER BY
  ✗ Don't index everything (writes become slower, storage grows)

TYPES:
  B-Tree index:    default, good for ranges (>, <, BETWEEN)
  Hash index:      exact matches only (=), faster than B-tree for equality
  Composite index: (user_id, created_at) — order matters!
                   Works for: WHERE user_id = X AND created_at > Y
                   Doesn't work for: WHERE created_at > Y alone

RULE: If a query is slow, EXPLAIN it. Add index on the filter column.
```

## Replication

```
PURPOSE: Availability + Read performance

SINGLE LEADER (most common):
  ┌──────────┐     writes     ┌─────────┐
  │  Leader   │ ←──────────── │  Client  │
  └─────┬────┘               └─────┬───┘
        │ replicate                 │ reads
  ┌─────▼────┐               ┌─────▼───┐
  │ Follower1 │               │ Follower2│
  └──────────┘               └─────────┘

  - All writes go to leader
  - Followers replicate and serve reads
  - If leader dies → promote a follower
  - Replication lag → eventual consistency on reads

MULTI-LEADER:
  - Multiple write nodes (used for multi-region)
  - Conflict resolution needed
  - Complex. Avoid unless you need multi-region writes.

LEADERLESS (Cassandra, DynamoDB):
  - Write to multiple nodes, read from multiple nodes
  - Quorum: W + R > N ensures consistency
  - W=2, R=2, N=3 → always read latest write
```

## Sharding (Partitioning)

```
PURPOSE: Single DB can't handle the load → split data across multiple DBs

HOW TO SHARD:

  By Hash (most common):
    shard = hash(user_id) % num_shards
    ✓ Even distribution
    ✗ Adding shards requires reshuffling (use consistent hashing)

  By Range:
    Users A-M → Shard 1, N-Z → Shard 2
    ✓ Range queries within a shard
    ✗ Hot spots (if some ranges are more popular)

  By Geography:
    US users → US shard, EU users → EU shard
    ✓ Low latency for regional access
    ✗ Cross-region queries are expensive

PROBLEMS WITH SHARDING:
  - JOINs across shards are expensive/impossible
  - Resharding when adding nodes
  - Hot shards (celebrity problem)
  - Transactions across shards are very hard

WHEN TO SHARD:
  Don't shard until you MUST. Try these first:
  1. Add read replicas
  2. Add caching (Redis)
  3. Optimize queries / add indexes
  4. Vertical scaling (bigger machine)
  5. THEN shard
```

## Consistent Hashing

```
PROBLEM: hash(key) % N breaks when N changes (all keys reshuffle)

SOLUTION: Consistent hashing
  - Arrange servers on a ring (hash circle)
  - Each key goes to the next server clockwise
  - Adding/removing a server only affects nearby keys

  USE: DynamoDB, Cassandra, CDN routing, distributed caches

  Virtual nodes: each server gets multiple positions on the ring
  → more even distribution
```

## ACID vs BASE

```
ACID (SQL):
  Atomicity    → all or nothing
  Consistency  → data always valid
  Isolation    → concurrent txns don't interfere
  Durability   → committed = permanent

BASE (NoSQL):
  Basically Available  → system always responds
  Soft state           → state may change over time
  Eventually consistent → reads may be stale briefly

WHEN YOU NEED ACID: money transfers, inventory counts, order placement
WHEN BASE IS OK:    social feeds, analytics, recommendations
```
