# API Design — REST, GraphQL, gRPC, Rate Limiting, Idempotency

## REST API Design

```
RESOURCES are nouns. METHODS are verbs.

  GET    /users          → list users
  GET    /users/123      → get user 123
  POST   /users          → create user
  PUT    /users/123      → replace user 123 (full update)
  PATCH  /users/123      → partial update user 123
  DELETE /users/123      → delete user 123

NESTED RESOURCES:
  GET /users/123/orders         → orders for user 123
  POST /users/123/orders        → create order for user 123

STATUS CODES:
  200 OK              → success
  201 Created         → resource created (POST)
  204 No Content      → success, no body (DELETE)
  400 Bad Request     → client sent invalid data
  401 Unauthorized    → not authenticated
  403 Forbidden       → authenticated but not allowed
  404 Not Found       → resource doesn't exist
  429 Too Many Reqs   → rate limited
  500 Internal Error  → server broke

PAGINATION:
  GET /users?page=2&limit=20
  GET /users?cursor=abc123&limit=20  (cursor-based, better for large datasets)

  Response:
  {
    "data": [...],
    "next_cursor": "xyz789",
    "has_more": true
  }

VERSIONING:
  /api/v1/users    → URL versioning (most common)
  Accept: application/vnd.api.v1+json  → header versioning
```

## REST vs GraphQL vs gRPC

```
REST:
  ✓ Simple, well-understood, cacheable
  ✓ Good for CRUD operations
  ✗ Over-fetching (get whole user when you need just name)
  ✗ Under-fetching (need 3 calls for related data)
  USE: Public APIs, simple CRUD, most web apps

GraphQL:
  ✓ Client specifies exactly what data it needs
  ✓ One endpoint, one request for complex nested data
  ✓ Great for mobile (minimize data transfer)
  ✗ Complex caching
  ✗ N+1 query problem on backend
  USE: Mobile apps, complex UIs, data-heavy dashboards

  query {
    user(id: "123") {
      name
      orders(last: 5) {
        total
        items { name }
      }
    }
  }

gRPC:
  ✓ Binary protocol (Protobuf), very fast
  ✓ Bi-directional streaming
  ✓ Strong typing with .proto files
  ✓ Auto-generated client libraries
  ✗ Not browser-friendly (needs proxy)
  ✗ Not human-readable
  USE: Internal microservice communication, real-time streaming
```

## Idempotency

```
DEFINITION: Making the same request multiple times has the same effect as making it once.

WHY IT MATTERS:
  Network fails after server processes request but before client gets response.
  Client retries. Without idempotency → double charge, duplicate order.

NATURALLY IDEMPOTENT:
  GET    → always safe (reading)
  PUT    → replace with same data = same result
  DELETE → deleting something already deleted = same result

NOT NATURALLY IDEMPOTENT:
  POST   → creating a resource twice = two resources!

HOW TO MAKE POST IDEMPOTENT:

  1. Client sends a unique IDEMPOTENCY KEY with each request:

     POST /payments
     Idempotency-Key: abc-123-xyz
     { "amount": 50, "to": "user_456" }

  2. Server checks: "Have I processed abc-123-xyz before?"
     - YES → return the stored response (don't process again)
     - NO  → process, store result with key, return response

  IMPLEMENTATION:
     def create_payment(idempotency_key, data):
         existing = redis.get(f"idem:{idempotency_key}")
         if existing:
             return existing  # already processed

         result = process_payment(data)
         redis.setex(f"idem:{idempotency_key}", 86400, result)  # store for 24h
         return result

STRIPE, AWS, ALL PAYMENT SYSTEMS use this pattern.
```

## Rate Limiting

```
WHY: Prevent abuse, protect servers, ensure fairness.

ALGORITHMS:

  1. TOKEN BUCKET (most common):
     - Bucket holds N tokens, refills at rate R tokens/sec
     - Each request takes 1 token
     - No tokens left → reject (429)
     - Allows bursts (up to bucket capacity)

     class TokenBucket:
         def __init__(self, capacity, refill_rate):
             self.tokens = capacity
             self.capacity = capacity
             self.refill_rate = refill_rate
             self.last_refill = time.time()

         def allow(self):
             self._refill()
             if self.tokens >= 1:
                 self.tokens -= 1
                 return True
             return False

         def _refill(self):
             now = time.time()
             elapsed = now - self.last_refill
             self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
             self.last_refill = now

  2. SLIDING WINDOW:
     - Count requests in the last N seconds
     - Use Redis sorted set: ZADD with timestamp, ZCOUNT for window
     - More precise than fixed window, no boundary burst issue

  3. FIXED WINDOW:
     - Count requests per minute/hour
     - Simple but has boundary problem (120 requests in 2 seconds across boundary)

  4. LEAKY BUCKET:
     - Process requests at fixed rate
     - Queue excess requests
     - Good for smoothing traffic

WHERE TO RATE LIMIT:
  API Gateway (global)  → rate limit by API key, IP
  Per-service           → rate limit by user, endpoint
  Database level        → connection pooling

RESPONSE:
  HTTP 429 Too Many Requests
  Retry-After: 30  (header telling client when to retry)
```

## Webhook vs Polling

```
POLLING:
  Client repeatedly asks: "Any updates? Any updates? Any updates?"
  Wastes resources if nothing changed.
  Simple to implement.

LONG POLLING:
  Client asks, server HOLDS the connection until there's data.
  Better than polling, but still one connection per client.

WEBHOOKS:
  Server calls YOUR endpoint when something happens.
  "Don't call us, we'll call you."
  ✓ Real-time, efficient
  ✗ Client must expose an endpoint
  ✗ Need retry logic for failed deliveries

SSE (Server-Sent Events):
  One-way stream from server to client over HTTP.
  Good for: live feeds, notifications
  ✓ Simple, works over HTTP
  ✗ One-way only

WEBSOCKETS:
  Full-duplex, persistent connection.
  Good for: chat, gaming, live collaboration
  ✓ True real-time, bidirectional
  ✗ More complex, stateful connections
```
