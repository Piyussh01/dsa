# Message Queues — Kafka, Pub/Sub, Event-Driven

## Why Message Queues?

```
WITHOUT QUEUE:
  Service A calls Service B directly (synchronous)
  If B is slow or down → A is stuck / fails
  If A sends 10K requests/sec but B handles 1K → B crashes

WITH QUEUE:
  Service A → [Queue] → Service B
  A publishes, doesn't wait. B consumes at its own pace.
  If B dies, messages wait in queue. No data loss.
```

## Core Concepts

```
PRODUCER:   sends messages to the queue
CONSUMER:   reads messages from the queue
TOPIC:      named channel/category (e.g., "user-signups", "order-placed")
PARTITION:  subdivision of a topic for parallelism (Kafka)
OFFSET:     position in the queue (Kafka tracks where each consumer is)

TWO MODELS:

  POINT-TO-POINT (Queue):
    One message → one consumer
    Used for: task distribution, work queues
    Example: 10 workers processing jobs, each job handled once

  PUB/SUB (Publish-Subscribe):
    One message → ALL subscribers get a copy
    Used for: event broadcasting, notifications
    Example: "order-placed" event → inventory, email, analytics all consume it
```

## Kafka vs RabbitMQ vs SQS

```
KAFKA:
  ✓ Massive throughput (100K+ msg/sec per broker)
  ✓ Messages are PERSISTENT (stored on disk, replayable)
  ✓ Ordered within a partition
  ✓ Consumer groups for parallel processing
  ✗ Complex to operate
  USE: Event streaming, logs, analytics, data pipelines

RABBITMQ:
  ✓ Traditional message broker
  ✓ Flexible routing (exchanges, bindings)
  ✓ Message acknowledgment (guaranteed delivery)
  ✓ Simpler than Kafka for small-medium scale
  ✗ Lower throughput than Kafka
  USE: Task queues, RPC, microservice communication

SQS (AWS):
  ✓ Fully managed, zero ops
  ✓ Scales automatically
  ✓ Dead letter queue built in
  ✗ No ordering guarantee (standard queue)
  ✗ At-least-once delivery (may get duplicates)
  USE: Decoupling AWS services, async processing
```

## Event-Driven Architecture

```
INSTEAD OF:
  Order Service → calls Inventory Service → calls Email Service → calls Analytics
  (tight coupling, cascading failures)

DO THIS:
  Order Service → publishes "order.placed" event
    → Inventory Service listens → decrements stock
    → Email Service listens → sends confirmation
    → Analytics Service listens → records metrics

BENEFITS:
  ✓ Services are decoupled (don't know about each other)
  ✓ Add new consumers without changing producer
  ✓ Each service can fail independently
  ✓ Replay events to rebuild state

EVENT SOURCING (advanced):
  Store EVENTS, not current state.
  State = replay all events from beginning.
  "Added $50" + "Withdrew $20" + "Added $100" = balance $130
  ✓ Complete audit trail
  ✓ Can rebuild state at any point in time
  ✗ Complex, more storage
```

## Delivery Guarantees

```
AT-MOST-ONCE:   fire and forget. May lose messages.
AT-LEAST-ONCE:  retry until ack. May get duplicates. (most common)
EXACTLY-ONCE:   hardest. Kafka supports it within Kafka. Cross-system? Use idempotency.

HOW TO HANDLE DUPLICATES (AT-LEAST-ONCE):
  Make consumers IDEMPOTENT.
  - Use a unique message ID
  - Before processing, check "have I seen this ID?"
  - Store processed IDs in a set/DB
  - If seen → skip. If not → process and record.
```

## Common Patterns

```
WORK QUEUE:
  10K images to resize → push to queue → 50 workers consume and resize
  Each image processed exactly once.

FANOUT:
  User posts a tweet → publish "new-tweet" event
  → Feed service, notification service, analytics all consume

DEAD LETTER QUEUE (DLQ):
  Messages that fail processing N times → moved to DLQ for investigation
  Don't lose them, don't retry forever.

SAGA PATTERN:
  Distributed transaction across services:
  1. Order Service: create order → publish "order.created"
  2. Payment Service: charge card → publish "payment.completed"
  3. Inventory Service: reserve stock → publish "stock.reserved"
  If any step fails → publish compensating events to undo previous steps
```

## When to Use a Queue in System Design

```
✓ Async processing (video transcoding, email sending)
✓ Decoupling services
✓ Rate leveling (producer is bursty, consumer is steady)
✓ Guaranteed delivery (can't afford to lose the event)
✓ Multiple consumers need the same event

✗ Synchronous request-response (user needs answer NOW)
✗ Simple CRUD with single DB
✗ Over-engineering a small system
```
