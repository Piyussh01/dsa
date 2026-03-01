# Scaling Fundamentals

## Vertical vs Horizontal Scaling

```
VERTICAL (Scale Up):
  Bigger machine. More CPU, RAM, disk.
  Simple. But there's a ceiling. Single point of failure.
  Good for: databases (initially), small services

HORIZONTAL (Scale Out):
  More machines. Distribute the load.
  No ceiling. But adds complexity (state, routing, consistency).
  Good for: stateless API servers, read replicas, caches
```

**Rule of thumb:** Scale stateless things horizontally, stateful things vertically first then shard.

## Load Balancer

```
         ┌──→ Server 1
Client → LB ──→ Server 2
         └──→ Server 3

WHAT IT DOES:
  - Distributes traffic across servers
  - Health checks (removes dead servers)
  - SSL termination

ALGORITHMS:
  Round Robin      → simple, equal distribution
  Least Connections → send to least busy server
  IP Hash          → same user → same server (sticky sessions)
  Weighted         → stronger servers get more traffic

LAYERS:
  L4 (Transport) → routes by IP/port, fast, no content inspection
  L7 (Application) → routes by URL/headers, smarter, slower

USE: AWS ALB (L7), NLB (L4), Nginx, HAProxy
```

## CDN (Content Delivery Network)

```
Without CDN:  User in Tokyo → Server in Virginia → 200ms latency
With CDN:     User in Tokyo → CDN edge in Tokyo → 20ms latency

WHAT TO PUT ON CDN:
  ✓ Static files (JS, CSS, images, videos)
  ✓ API responses that don't change often
  ✗ User-specific dynamic data

HOW IT WORKS:
  1. User requests image.jpg
  2. CDN edge doesn't have it → fetches from origin server (cache miss)
  3. CDN caches it at the edge
  4. Next user in same region → served from edge (cache hit)

PUSH vs PULL:
  Pull CDN: fetches from origin on first request (most common)
  Push CDN: you upload to CDN proactively (good for large files you know will be popular)

USE: CloudFront, Cloudflare, Akamai
```

## Reverse Proxy vs API Gateway

```
REVERSE PROXY (Nginx):
  - Load balancing
  - SSL termination
  - Caching
  - Compression

API GATEWAY (Kong, AWS API Gateway):
  - Everything a reverse proxy does, PLUS:
  - Authentication
  - Rate limiting
  - Request transformation
  - Analytics / logging
  - API versioning

When to use:
  Small app → Nginx as reverse proxy is enough
  Microservices → API gateway to manage cross-cutting concerns
```

## Stateless vs Stateful Services

```
STATELESS:
  Server holds NO user state between requests.
  Any server can handle any request.
  State lives in DB / cache / client token.
  ✓ Easy to scale horizontally
  ✓ Any server can die, no data lost

STATEFUL:
  Server remembers user state (sessions in memory).
  User must return to the SAME server.
  ✗ Harder to scale
  ✗ Server death = state lost

RULE: Make API servers STATELESS. Store state in Redis/DB.
  Session data → Redis
  Auth → JWT tokens (client holds state)
  File uploads → S3 (not local disk)
```

## Microservices vs Monolith

```
MONOLITH:
  One codebase, one deployment.
  ✓ Simple to develop, test, deploy
  ✓ No network calls between components
  ✗ Hard to scale individual components
  ✗ One bad deploy takes down everything

MICROSERVICES:
  Each feature is its own service with its own DB.
  ✓ Scale independently
  ✓ Deploy independently
  ✓ Tech diversity (Python for ML, Go for API)
  ✗ Network latency between services
  ✗ Distributed transactions are HARD
  ✗ Operational complexity (monitoring, tracing, deployment)

RULE FOR INTERVIEWS:
  Start with monolith. Split into microservices when you can
  justify WHY: "Video transcoding is CPU-heavy and needs to
  scale independently from the API layer."
```

## Numbers to Know

```
LATENCY:
  L1 cache:           0.5 ns
  RAM access:         100 ns
  SSD read:           100 μs
  Network (same DC):  500 μs
  Network (cross DC): 50-150 ms
  Disk seek:          10 ms

THROUGHPUT:
  Single MySQL:       ~10K QPS (reads), ~5K QPS (writes)
  Single Redis:       ~100K QPS
  Single Kafka broker: ~100K messages/sec

STORAGE:
  1 char = 1 byte (ASCII) / 1-4 bytes (UTF-8)
  1 tweet (280 chars) ≈ 300 bytes with metadata
  1 image ≈ 200KB-2MB
  1 minute of video ≈ 50MB (compressed)
```
