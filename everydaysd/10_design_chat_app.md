# Design Chat App — WhatsApp / Slack / Messenger

## When Asked
"Design WhatsApp", "Design Slack", "Design a real-time messaging system", "Design Facebook Messenger"

## Requirements

```
FUNCTIONAL:
  - 1:1 messaging
  - Group chat
  - Online/offline status (presence)
  - Read receipts, delivered status
  - Message history
  - Media sharing (images, files)
  - Push notifications (offline users)

NON-FUNCTIONAL:
  - Real-time delivery (<100ms for online users)
  - Availability > consistency
  - Message ordering (within a conversation)
  - Scale: 500M DAU, 40 messages/user/day = 20B messages/day
```

## High-Level Architecture

```
  ┌─────────┐    WebSocket     ┌──────────────────┐
  │ Client  │◄═══════════════►│ Chat Server       │
  └─────────┘                  │ (WebSocket layer) │
                               └────────┬─────────┘
                                        │
                    ┌───────────────────┤────────────────────┐
                    │                   │                    │
               ┌────▼────┐       ┌─────▼──────┐     ┌──────▼──────┐
               │ Message │       │ Presence   │     │ Notification│
               │ Service │       │ Service    │     │ Service     │
               └────┬────┘       └─────┬──────┘     └──────┬──────┘
                    │                  │                    │
               ┌────▼────┐       ┌─────▼──────┐     ┌──────▼──────┐
               │ Msg DB  │       │ Redis      │     │ Push (APNs/ │
               │(Cassandra)│     │ (presence) │     │  FCM)       │
               └─────────┘       └────────────┘     └─────────────┘
```

## Key Components

```
WEBSOCKET CONNECTION:
  - Client opens persistent WebSocket to chat server
  - Assigned to a specific chat server (connection mapping stored in Redis)
  - Heartbeat every 30 seconds to detect disconnection

CONNECTION MAPPING (Redis):
  user_123 → chat_server_5
  "Which server is this user connected to?"

MESSAGE FLOW (1:1):
  1. User A sends message via WebSocket → Chat Server
  2. Chat Server looks up: "Where is User B connected?"
     → Redis: user_B → chat_server_3
  3. If User B is ONLINE:
     → Forward message to chat_server_3 → deliver via WebSocket
  4. If User B is OFFLINE:
     → Store in DB → send push notification
  5. When User B comes online:
     → Pull undelivered messages from DB

MESSAGE FLOW (Group):
  1. User A sends message to group_456
  2. Lookup group members (cached in Redis)
  3. For each member: same as 1:1 (online → WebSocket, offline → push)
  4. Fan-out: small groups (< 200) → fan out immediately
     Large groups → pull model (members fetch on open)

MESSAGE STORAGE:
  Use Cassandra or HBase (write-heavy, time-series data)

  Table: messages
    partition_key: conversation_id
    clustering_key: timestamp (sorted within partition)
    columns: sender_id, content, type, status

  This gives O(1) lookup for "all messages in conversation, sorted by time"

PRESENCE (Online/Offline):
  - Heartbeat-based: client pings every 30 sec
  - No heartbeat for 90 sec → mark offline
  - Store in Redis: SET user:123:status online EX 90
  - Publish status changes to friends/group members

READ RECEIPTS:
  - Message states: sent → delivered → read
  - "delivered": server confirms recipient's device received it
  - "read": recipient's app reports it was displayed
  - Update message status in DB + notify sender via WebSocket

MEDIA SHARING:
  - Upload image/file to S3 (presigned URL)
  - Send message with media_url instead of text
  - Thumbnail generated asynchronously
```

## Deep Dive: Message Ordering

```
PROBLEM: Messages arrive out of order due to network delays

SOLUTION:
  - Client generates local timestamp
  - Server assigns server timestamp + sequence number
  - Display order: sorted by (conversation_id, server_sequence)
  - Within same millisecond: use Lamport clock or server sequence

IDEMPOTENCY:
  - Client attaches unique message_id (UUID)
  - Server deduplicates: if message_id exists → skip
  - Prevents duplicate messages on retry
```

## Scaling Considerations

```
CHAT SERVERS:
  - Each handles ~50K-100K WebSocket connections
  - 500M users → need ~5000-10000 chat servers
  - Stateful (holds connections) → can't just kill them
  - Graceful shutdown: drain connections to other servers

CROSS-SERVER MESSAGING:
  User A on server 1, User B on server 7
  Options:
    a) Direct RPC between chat servers (simple, coupling)
    b) Message queue between servers (decoupled, slightly more latency)
    c) Pub/sub (Redis Pub/Sub): server 1 publishes, server 7 subscribes

SHARDING MESSAGES:
  Shard by conversation_id → all messages for a chat on same shard
  Hot conversations (celebrity groups) → dedicated shard
```
