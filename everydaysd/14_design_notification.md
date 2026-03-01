# Design Notification System — Push, Email, SMS

## When Asked
"Design a notification system", "Design push notifications", "Design an alerting system"

## Requirements

```
FUNCTIONAL:
  - Send notifications via: push (mobile), email, SMS, in-app
  - User preferences (opt-in/out per channel, per type)
  - Templated messages
  - Scheduled notifications
  - Priority levels (urgent vs marketing)
  - Rate limiting (don't spam users)

NON-FUNCTIONAL:
  - Soft real-time (push within 1-2 sec, email within minutes)
  - At-least-once delivery
  - Scale: 10B notifications/day
  - No duplicate sends
```

## High-Level Architecture

```
  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Services    │────→│ Notification │────→│ Kafka        │
  │ (triggers)  │     │ API          │     │ (priority Qs)│
  └─────────────┘     └──────────────┘     └──────┬───────┘
                                                   │
                            ┌──────────────────────┼────────────────┐
                            │                      │                │
                       ┌────▼─────┐          ┌─────▼────┐    ┌─────▼────┐
                       │Push Worker│          │Email     │    │SMS Worker│
                       │          │          │Worker    │    │          │
                       └────┬─────┘          └─────┬────┘    └─────┬────┘
                            │                      │               │
                       ┌────▼─────┐          ┌─────▼────┐    ┌─────▼────┐
                       │APNs/FCM  │          │SendGrid/ │    │Twilio    │
                       │          │          │SES       │    │          │
                       └──────────┘          └──────────┘    └──────────┘
```

## Key Components

```
NOTIFICATION API:
  POST /notifications
  {
    "user_ids": [123, 456],
    "template_id": "order_shipped",
    "data": {"order_id": "abc", "eta": "2pm"},
    "channels": ["push", "email"],
    "priority": "high"
  }

  1. Validate request
  2. Check user preferences (user 456 opted out of email → skip)
  3. Render template with data
  4. Publish to Kafka (separate topics per priority)

TEMPLATE SERVICE:
  Templates stored in DB:
    "order_shipped": {
      "push_title": "Order Shipped!",
      "push_body": "Your order {{order_id}} arrives by {{eta}}",
      "email_subject": "Your order is on its way",
      "email_body": "<html>..."
    }

  Render at send time with user's data.

USER PREFERENCES (Redis + DB):
  user:123:prefs = {
    "push": true,
    "email": true,
    "sms": false,
    "marketing_push": false,
    "quiet_hours": "22:00-07:00"
  }

  Check BEFORE queuing to avoid wasted work.

RATE LIMITING:
  Per user: max 5 push notifications per hour (non-urgent)
  Per user per type: max 1 "price alert" per day
  Global: max 1M emails per hour (sender reputation)

  Use Redis: INCR user:123:push_count, EXPIRE 3600

DEDUPLICATION:
  Each notification gets a unique ID.
  Before sending: check Redis SET "sent:{notification_id}"
  If exists → skip (already sent). If not → send and record.

PRIORITY QUEUES:
  Kafka topics by priority:
    notifications.critical   → processed immediately (security alerts)
    notifications.high       → processed within seconds (order updates)
    notifications.medium     → processed within minutes (social)
    notifications.low        → processed in batch (marketing, digest)

DELIVERY TRACKING:
  Track status: created → queued → sent → delivered → opened
  Store in analytics DB (ClickHouse/BigQuery)
  Useful for: delivery rates, open rates, optimization
```

## Push Notification Deep Dive

```
MOBILE PUSH FLOW:
  1. App registers with APNs (iOS) / FCM (Android)
  2. Receives device token → sends to your server
  3. Store: user_123 → [device_token_1, device_token_2]
  4. To send push: call APNs/FCM API with device token + payload

  HANDLE TOKEN INVALIDATION:
    APNs/FCM tells you token is invalid → remove from DB
    User uninstalls app → token becomes invalid

  PAYLOAD LIMITS:
    APNs: 4KB max
    FCM: 4KB max
    Keep it short. Don't send full content, just enough to display.

  SILENT PUSH:
    Push without visible notification → triggers app to sync data
    Used for: badge count update, background content refresh
```

## Scaling

```
WORKERS:
  Scale push/email/SMS workers independently based on queue depth.
  Email: batch sends (SES supports 50 recipients per API call)
  Push: batch sends (FCM supports 500 devices per multicast)

VENDOR FAILOVER:
  Primary email: SES
  Fallback: SendGrid
  If SES fails → retry with SendGrid (circuit breaker pattern)

ANALYTICS AT SCALE:
  Don't write to SQL for every notification.
  Use Kafka → ClickHouse/BigQuery for analytics.
  Aggregate: delivery rate, open rate, click rate per template/channel.
```
