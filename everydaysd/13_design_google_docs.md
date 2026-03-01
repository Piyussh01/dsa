# Design Google Docs — Real-Time Collaboration

## When Asked
"Design Google Docs", "Design collaborative editing", "Design a shared document editor", "Design Figma (collaborative)"

## Requirements

```
FUNCTIONAL:
  - Create/edit documents
  - Real-time collaboration (multiple users editing simultaneously)
  - See other users' cursors
  - Version history
  - Comments
  - Share with permissions (view, edit, comment)

NON-FUNCTIONAL:
  - Real-time sync (<100ms for edits to appear)
  - No data loss (every keystroke persisted)
  - Conflict resolution (two people edit same line)
  - Scale: millions of documents, ~100 concurrent editors per doc
```

## The Core Problem: Conflict Resolution

```
User A types "Hello" at position 5
User B deletes character at position 3
Both happen simultaneously. What's the final state?

TWO APPROACHES:

  OT (Operational Transformation):
    Transform operations against each other.
    A's insert at pos 5 + B's delete at pos 3
    → A's insert becomes pos 4 (shifted because B deleted before it)
    ✓ Well-proven (Google Docs uses this)
    ✗ Complex to implement correctly
    ✗ Requires a central server to order operations

  CRDT (Conflict-free Replicated Data Type):
    Each character has a unique ID and position between neighbors.
    Operations commute (order doesn't matter, same result).
    ✓ No central server needed (P2P possible)
    ✓ Mathematically guaranteed convergence
    ✗ More memory (each character needs metadata)
    ✗ Complex data structure

FOR INTERVIEWS: mention both, say "I'll use OT with a central server
for ordering" — it's simpler to explain.
```

## High-Level Architecture

```
  ┌─────────┐    WebSocket     ┌───────────────┐
  │Client A │◄════════════════►│ Collaboration │
  │(Editor) │                  │ Server        │──→ Document DB
  └─────────┘                  │ (OT Engine)   │    (MongoDB/Postgres)
                               └───────┬───────┘
  ┌─────────┐    WebSocket             │
  │Client B │◄═══════════════►─────────┘
  └─────────┘                          │
                               ┌───────▼───────┐
                               │ Redis         │ (presence, cursors)
                               └───────────────┘
                               ┌───────────────┐
                               │ S3            │ (version snapshots)
                               └───────────────┘
```

## Key Components

```
WEBSOCKET SESSION:
  - Client opens WebSocket to collaboration server for document X
  - Server tracks all active connections for document X
  - Each edit → send operation to server → server broadcasts to all others

OPERATIONAL TRANSFORMATION:
  Operations are: INSERT(char, position) or DELETE(position)

  Client sends:
    { type: "insert", char: "a", position: 5, version: 42 }

  Server:
    1. Receives operation from client A (version 42)
    2. If server is at version 44, transform operation against ops 43, 44
    3. Apply transformed operation
    4. Broadcast transformed operation to all other clients
    5. Increment version to 45

  Client receives:
    1. Receive server operation
    2. Transform against any local pending operations
    3. Apply to local document

DOCUMENT STORAGE:
  - Document content stored in DB (PostgreSQL or MongoDB)
  - Save every N seconds or after N operations (not every keystroke)
  - Operations buffered in memory on collaboration server

VERSION HISTORY:
  - Snapshot document state periodically (every 100 operations)
  - Store snapshots in S3
  - To view version X: find nearest snapshot before X, replay operations

PRESENCE & CURSORS:
  - Store cursor positions in Redis with TTL
  - Broadcast cursor updates via WebSocket (throttled to ~5 updates/sec)
  - Show colored cursors for each collaborator

PERMISSIONS:
  Document sharing model:
    doc_permissions: doc_id, user_id, role (owner/editor/viewer/commenter)
  Check on WebSocket connect and every operation
```

## Deep Dive: Document Partitioning

```
PROBLEM: Document with 100 users editing different sections.
All operations go through single server → bottleneck.

SOLUTIONS:
  1. One collaboration server per document (simple, limits doc scale)
  2. Partition document into blocks/paragraphs
     Each block can have its own OT session
     Operations within a block are independent
  3. Use CRDT for decentralized conflict resolution

FOR MOST INTERVIEWS: say "one collab server per doc, can handle
~100 concurrent editors which covers 99.9% of cases."
```

## Scaling

```
DOCUMENT ROUTING:
  - Hash doc_id → assign to specific collaboration server
  - Use consistent hashing so adding/removing servers is smooth
  - If server dies → clients reconnect → new server loads doc from DB

STORAGE TIERS:
  Hot (active docs):     in-memory on collab server + Redis
  Warm (recent docs):    PostgreSQL/MongoDB
  Cold (old versions):   S3

OFFLINE EDITING:
  - Client stores operations locally
  - On reconnect: send buffered operations
  - Server transforms against operations that happened while offline
  - This is where CRDTs shine (natural offline support)
```
