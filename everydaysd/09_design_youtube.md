# Design YouTube / Netflix — Video Platform

## When Asked
"Design YouTube", "Design Netflix", "Design a video streaming platform", "Design TikTok"

## Requirements

```
FUNCTIONAL:
  - Upload videos
  - Stream/watch videos
  - Search videos
  - Like, comment, subscribe
  - Recommendations / feed

NON-FUNCTIONAL:
  - Availability > consistency (OK to see a like count slightly behind)
  - Low latency streaming
  - Scale: 1B+ users, 500M DAU, 5 videos/day per user = 2.5B views/day
  - Upload: ~500K videos/day
```

## Back-of-Envelope

```
Views:   2.5B/day ÷ 100K sec = 25K QPS (reads)
Uploads: 500K/day ÷ 100K sec = 5 QPS (writes) — but each is heavy (large file)
Storage: 500K videos × 300MB avg = 150TB/day → ~55PB/year
Bandwidth: 25K QPS × 5MB (avg chunk) = 125GB/sec
```

## High-Level Architecture

```
                        ┌──────────────┐
                        │   CDN        │ ← video chunks served from edge
                        └──────┬───────┘
                               │
  ┌─────────┐    ┌─────────┐   │   ┌───────────────┐
  │ Client  │───→│ API GW  │───┼──→│ Video Service  │ → metadata DB
  └─────────┘    └─────────┘   │   └───────────────┘
       │                       │   ┌───────────────┐
       │  upload               │   │ Search Service │ → Elasticsearch
       ▼                       │   └───────────────┘
  ┌──────────┐                 │   ┌───────────────┐
  │  S3      │ ← raw video     │   │ Recommend Svc │ → ML models
  └────┬─────┘                 │   └───────────────┘
       │ trigger               │
  ┌────▼─────────┐             │
  │ Transcode Q  │             │
  │ (Kafka/SQS)  │             │
  └────┬─────────┘             │
  ┌────▼─────────┐             │
  │ Transcoding  │──→ S3 (multiple resolutions) ──→ CDN
  │ Workers      │
  └──────────────┘
```

## Key Components

```
VIDEO UPLOAD FLOW:
  1. Client requests presigned S3 URL from API
  2. Client uploads raw video directly to S3
  3. S3 triggers event → Kafka/SQS
  4. Transcoding workers pull from queue
  5. Transcode to multiple resolutions (240p, 480p, 720p, 1080p, 4K)
  6. Generate thumbnails
  7. Store transcoded files in S3
  8. Update metadata DB: "video ready"
  9. Push to CDN

VIDEO STREAMING:
  - Adaptive Bitrate Streaming (HLS/DASH)
  - Video split into 2-10 second segments
  - Client requests manifest file → lists available qualities
  - Client picks quality based on bandwidth
  - Segments served from CDN (closest edge)

METADATA DB (SQL — PostgreSQL):
  videos: id, title, description, user_id, status, created_at, duration
  users: id, name, email, subscriber_count

SEARCH:
  - Elasticsearch for full-text search
  - Index: title, description, tags, captions
  - Typeahead: prefix matching on popular searches

RECOMMENDATIONS:
  - Collaborative filtering: "users who watched X also watched Y"
  - Content-based: similar tags, categories
  - ML model serving (pre-computed, cached)
```

## Deep Dive: Video Transcoding

```
WHY: Raw video is huge. Different devices need different formats/resolutions.

PIPELINE:
  Raw MP4 → Split into chunks → Parallel transcode → Reassemble

  Each chunk independently transcoded:
    → 240p, 480p, 720p, 1080p (H.264/H.265 codec)
    → Generate thumbnail at multiple timestamps

  Use: AWS MediaConvert, FFmpeg workers, or custom pipeline
  Scale: Auto-scale workers based on queue depth

COST OPTIMIZATION:
  - Only transcode to resolutions that make sense (don't upscale 480p source to 4K)
  - Defer cold resolutions (transcode 1080p immediately, 240p on first request)
```

## Deep Dive: CDN for Video

```
PRE-POPULATE: Push popular/trending videos to CDN proactively
LONG-TAIL: Less popular videos fetched from origin on demand

CACHE KEY: video_id + resolution + segment_number
  e.g., CDN key = "v123/1080p/segment_042.ts"

MULTI-CDN: Use multiple CDN providers for reliability
  Route based on geography, cost, or availability
```
