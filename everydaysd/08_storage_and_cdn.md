# Storage & CDN — Blob Storage, Hot/Cold, File Systems

## Storage Types

```
BLOCK STORAGE (EBS, local SSD):
  - Raw blocks, like a hard drive
  - Attach to one server
  - Low latency, good for databases
  - USE: DB storage, OS disk

FILE STORAGE (EFS, NFS):
  - Shared file system across servers
  - POSIX compatible (like regular files)
  - USE: shared config, legacy apps needing file system

OBJECT STORAGE (S3, GCS, Azure Blob):
  - Store any blob (file) with a key
  - key = "videos/user123/video456.mp4", value = file bytes
  - Infinitely scalable, cheap
  - No directory hierarchy (flat namespace, "/" in key is cosmetic)
  - Immutable: can't edit in place, only replace
  - USE: images, videos, backups, logs, static assets

  S3 TIERS:
    Standard:          frequent access, low latency
    Infrequent Access: cheaper storage, retrieval fee
    Glacier:           archive, minutes-to-hours retrieval, very cheap
    Glacier Deep:      rarely accessed, 12-hour retrieval, cheapest
```

## Hot, Warm, Cold Storage

```
HOT:   frequently accessed, fast, expensive
       → SSD, Redis, S3 Standard
       → Recent posts, active user data, current orders

WARM:  occasionally accessed, moderate speed/cost
       → HDD, S3 Infrequent Access
       → Last month's logs, older user data

COLD:  rarely accessed, slow retrieval, cheap
       → S3 Glacier, tape
       → Compliance archives, old backups

DESIGN PATTERN:
  Recent data (7 days)   → Redis cache + hot DB
  Recent data (90 days)  → warm DB / S3 IA
  Historical (years)     → S3 Glacier

  Move data between tiers with lifecycle policies:
  "After 30 days, move to IA. After 1 year, move to Glacier."
```

## CDN Deep Dive

```
ARCHITECTURE:
  Origin Server (your server / S3)
    ↓ pull on first request
  CDN Edge Nodes (globally distributed)
    ↓ cached response
  User (low latency from nearby edge)

CACHE INVALIDATION ON CDN:
  TTL-based:     set max-age, content refreshes after expiry
  Versioned URLs: style.v2.css or style.css?v=abc123
  Purge API:      manually invalidate specific paths

WHEN TO USE CDN:
  ✓ Static assets (JS, CSS, images, fonts)
  ✓ Video streaming (pre-cached segments)
  ✓ API responses that are same for all users
  ✗ Personalized content (user-specific data)
  ✗ Real-time data (stock prices, chat messages)

VIDEO STREAMING:
  Don't serve the whole file. Use:
  - HLS (HTTP Live Streaming): chop video into 2-10 sec segments
  - Adaptive bitrate: multiple quality levels, client switches based on bandwidth
  - Pre-cache popular segments at edge nodes
```

## Database File Storage Anti-Pattern

```
DON'T store files in the database.

BAD:  INSERT INTO users (avatar) VALUES (binary_blob_of_image)
  → DB becomes huge, backups slow, queries slow

GOOD: Upload file to S3, store the URL in DB
  INSERT INTO users (avatar_url) VALUES ('https://cdn.example.com/avatars/123.jpg')

FLOW:
  1. Client requests presigned upload URL from API
  2. Client uploads directly to S3 (no load on your servers)
  3. Client sends the S3 key to your API
  4. API stores the key/URL in DB
```

## Data Backup & Disaster Recovery

```
BACKUP STRATEGIES:
  Full backup:        entire DB dump (weekly)
  Incremental backup: only changes since last backup (daily)
  WAL archiving:      stream write-ahead logs to S3 (continuous)

RPO (Recovery Point Objective): how much data can you lose?
  RPO = 0      → synchronous replication (expensive)
  RPO = 1 hour → hourly backups
  RPO = 1 day  → daily backups

RTO (Recovery Time Objective): how fast must you recover?
  RTO = 0      → active-active multi-region (expensive)
  RTO = minutes → hot standby (replicas ready to promote)
  RTO = hours  → restore from backup

MULTI-REGION:
  Active-Passive: one region serves traffic, other is standby
  Active-Active:  both regions serve traffic (complex, conflict resolution needed)
```
