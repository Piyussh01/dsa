# Consistency & Availability — CAP, Consensus, Distributed Systems

## CAP Theorem

```
In a distributed system, during a NETWORK PARTITION, you can only guarantee:
  CP: Consistency + Partition tolerance  (sacrifice availability)
  AP: Availability + Partition tolerance (sacrifice consistency)

You CANNOT have all three simultaneously during a partition.

  CP SYSTEMS (consistency first):
    - MongoDB (default), HBase, Redis Cluster
    - During partition: refuse to serve if can't guarantee consistency
    - Good for: banking, inventory, anything where wrong data = disaster

  AP SYSTEMS (availability first):
    - Cassandra, DynamoDB, CouchDB
    - During partition: serve potentially stale data
    - Good for: social feeds, recommendations, analytics

IN INTERVIEWS: Don't just say "CAP theorem." Say:
  "For a banking system, I'd choose CP because showing wrong balance
   is worse than brief unavailability. For a social feed, AP is fine
   because seeing a post 2 seconds late doesn't matter."
```

## Consistency Models

```
STRONG CONSISTENCY:
  After a write completes, ALL subsequent reads return the new value.
  Every reader sees the same data at the same time.
  Cost: slower writes, lower availability.
  Use: bank balance, inventory count.

EVENTUAL CONSISTENCY:
  After a write, reads MAY return old value for a while.
  Eventually (milliseconds to seconds), all replicas converge.
  Cost: may read stale data.
  Use: social media feed, DNS, email.

CAUSAL CONSISTENCY:
  If event A caused event B, everyone sees A before B.
  But unrelated events can be seen in any order.
  Example: "I posted, then commented" — comment always after post.

READ-YOUR-WRITES:
  After you write, YOUR reads see the update.
  Other users may see stale data.
  Implementation: read from leader after writing, or use session stickiness.

MONOTONIC READS:
  You never see data go "backward."
  If you read version 5, you'll never see version 4 next.
```

## Consensus — How Distributed Systems Agree

```
PROBLEM: 5 servers, 1 goes down. How do the remaining agree on state?

RAFT PROTOCOL (easier to understand):
  1. Elect a LEADER (majority vote)
  2. Leader accepts writes, replicates to followers
  3. Write is "committed" when majority (3/5) acknowledge
  4. If leader dies → new election

  WHY MAJORITY?
    5 servers, need 3 to agree.
    If 2 die, 3 can still work.
    No two majorities can disagree (they overlap by at least 1 node).

PAXOS:
  Same idea, more formal, harder to understand.
  Just say "similar to Raft" in interviews.

ZOOKEEPER:
  Distributed coordination service using ZAB (like Raft).
  Used for: leader election, config management, distributed locking.
  Kafka uses Zookeeper (moving away from it though).

REAL-WORLD:
  etcd (Kubernetes uses it) → Raft
  CockroachDB → Raft
  Kafka KRaft → Raft (replacing Zookeeper)
```

## Distributed Transactions

```
PROBLEM: Transfer $100 from Bank A to Bank B. Both must succeed or both must fail.

TWO-PHASE COMMIT (2PC):
  Phase 1 (Prepare): Coordinator asks A and B: "Can you commit?"
  Phase 2 (Commit):  If both say YES → "Commit." If any says NO → "Abort."

  ✗ Blocking: if coordinator dies after prepare, everyone waits
  ✗ Slow: two round-trips
  USE: within a single data center, traditional databases

SAGA PATTERN (preferred for microservices):
  Break transaction into steps. Each step has a COMPENSATING action.

  1. Order Service: create order
  2. Payment Service: charge card
  3. Inventory: reserve stock

  If step 3 fails:
    → Compensate step 2: refund card
    → Compensate step 1: cancel order

  Two types:
    Choreography: each service listens for events and acts
    Orchestration: central coordinator tells each service what to do

  ✓ No distributed locks
  ✓ Each service is independent
  ✗ Complex compensation logic
  ✗ Temporary inconsistency between steps
```

## Distributed Locking

```
PROBLEM: Two servers try to update the same resource simultaneously.

REDIS LOCK (simple):
  acquired = redis.set("lock:order:123", my_id, nx=True, ex=30)
  if acquired:
      try:
          process_order()
      finally:
          if redis.get("lock:order:123") == my_id:
              redis.delete("lock:order:123")

  NX = only set if not exists
  EX = expire after 30 seconds (prevent deadlock)

REDLOCK (more robust):
  Acquire lock on majority of Redis instances (3/5).
  Tolerates individual Redis node failures.

ZOOKEEPER LOCK:
  Create ephemeral sequential node.
  If yours has the lowest sequence number → you have the lock.
  If not → watch the node before yours.
  ✓ No expiry games, ephemeral nodes auto-delete on disconnect.
```
