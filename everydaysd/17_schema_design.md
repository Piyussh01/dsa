# Schema Design — Tables, Columns, Fast Decisions

## The 5-Minute Schema Recipe

```
For any entity the interviewer mentions, immediately think:

1. WHAT IS THE ENTITY?        → that's your table name
2. WHAT UNIQUELY IDENTIFIES IT? → that's your primary key
3. WHAT BELONGS TO IT?         → those are your columns
4. WHAT DOES IT RELATE TO?     → those are your foreign keys
5. WHAT WILL YOU QUERY BY?     → those need indexes
```

## Template: Rapid Table Design

```sql
-- Say it out loud: "A [entity] has [attributes] and belongs to [other entity]"

-- "A user has a name, email, and password"
CREATE TABLE users (
    id          BIGINT PRIMARY KEY,         -- always use BIGINT, not INT
    email       VARCHAR(255) UNIQUE NOT NULL,
    name        VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW()
);

-- "An order belongs to a user and has a total and status"
CREATE TABLE orders (
    id          BIGINT PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id),
    total_cents BIGINT NOT NULL,            -- store money as cents (avoid float!)
    status      VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT NOW()
);

-- "An order has many items, each item is a product with a quantity"
CREATE TABLE order_items (
    id          BIGINT PRIMARY KEY,
    order_id    BIGINT NOT NULL REFERENCES orders(id),
    product_id  BIGINT NOT NULL REFERENCES products(id),
    quantity    INT NOT NULL,
    price_cents BIGINT NOT NULL             -- price at time of order (snapshot!)
);
```

## Relationship Patterns

```
ONE-TO-MANY (most common):
  User has many Orders
  → Put user_id foreign key on orders table

  users: id, name
  orders: id, user_id (FK), total

MANY-TO-MANY:
  Students take many Courses, Courses have many Students
  → Create a JOIN TABLE

  students: id, name
  courses: id, title
  enrollments: student_id, course_id, enrolled_at   ← join table

ONE-TO-ONE:
  User has one Profile (with optional/large data)
  → Either put in same table OR separate table with FK

  users: id, name, email
  profiles: user_id (FK + PK), bio, avatar_url
```

## Common Schema Patterns

```
SOFT DELETE:
  Don't actually DELETE rows. Add a deleted_at column.
  WHERE deleted_at IS NULL  ← only show active records
  ✓ Can recover data
  ✓ Audit trail
  ✗ Queries need the filter everywhere

STATUS / STATE MACHINE:
  status VARCHAR(20): 'pending' → 'processing' → 'completed' → 'failed'
  Or use ENUM type if your DB supports it.
  Add status_changed_at for tracking.

POLYMORPHISM (different types in one table):
  -- Option A: Single Table (simple, some NULL columns)
  notifications: id, type ('email'|'push'|'sms'), recipient, content,
                 email_subject (NULL for non-email), device_token (NULL for non-push)

  -- Option B: Separate Tables (cleaner, more JOINs)
  notifications: id, type, recipient, content
  email_details: notification_id, subject, html_body
  push_details: notification_id, device_token, badge_count

AUDIT LOG / HISTORY:
  Store changes as events, not just current state.
  order_events: id, order_id, event_type, old_value, new_value, created_at, actor_id

TAGGING / LABELS:
  items: id, name
  tags: id, name
  item_tags: item_id, tag_id   ← many-to-many

TREE / HIERARCHY:
  categories: id, name, parent_id (self-referencing FK)
  Use adjacency list (simple) or materialized path ("electronics/phones/iphone")
```

## Normalization — Quick Rules

```
1NF: No arrays in columns (each cell = one value)
  BAD:  users: id, phone_numbers="555-1234,555-5678"
  GOOD: user_phones: user_id, phone_number

2NF: No partial dependencies (every column depends on FULL primary key)
  BAD:  order_items: order_id, product_id, product_name ← name depends only on product_id
  GOOD: product_name belongs in products table

3NF: No transitive dependencies
  BAD:  orders: order_id, customer_id, customer_name ← name depends on customer_id, not order
  GOOD: customer_name belongs in customers table

WHEN TO DENORMALIZE:
  - Read-heavy system (avoid JOINs for performance)
  - Pre-compute expensive aggregations
  - Store a "snapshot" (price at time of order, not current price)
  - NoSQL databases (no JOINs, embed related data)
```

## Index Design Decisions

```
ASK: "What queries will this table serve?"

users table queries:
  - Login: WHERE email = ?          → INDEX on email
  - Profile: WHERE id = ?          → PK (automatic)
  - Search: WHERE name LIKE 'jo%'  → INDEX on name (prefix only)
  - List active: WHERE status = 'active' ORDER BY created_at
                                    → COMPOSITE INDEX (status, created_at)

COMPOSITE INDEX ORDER MATTERS:
  INDEX (a, b, c) works for:
    WHERE a = ?
    WHERE a = ? AND b = ?
    WHERE a = ? AND b = ? AND c = ?
    WHERE a = ? AND b = ? ORDER BY c

  Does NOT work for:
    WHERE b = ?          ← leftmost prefix not included
    WHERE c = ?
    WHERE b = ? AND c = ?

COVERING INDEX:
  If the index contains ALL columns the query needs → DB doesn't even touch the table.
  INDEX (user_id, created_at) covers: SELECT created_at FROM orders WHERE user_id = ?
```

## Money, Time, and Other Gotchas

```
MONEY:     Use BIGINT for cents. NEVER use FLOAT.
           $19.99 → 1999 cents. Do math on ints, format for display.

TIMESTAMPS: Use UTC always. Let the frontend convert to local time.
           TIMESTAMP WITH TIME ZONE in PostgreSQL.

ENUMS:     Use VARCHAR(20) or a separate lookup table.
           DB ENUMs are hard to modify in production.

IDs:       BIGINT auto-increment (simple) or UUID (distributed).
           UUIDs: no coordination needed, but 128 bits vs 64 for BIGINT.
           Snowflake IDs: sortable + distributed (Twitter's approach).

BOOLEANS:  is_active, is_deleted, is_verified → clear naming with "is_" prefix

NULLS:     Avoid where possible. Use DEFAULT values.
           NULL != NULL (makes queries tricky). Use NOT NULL + defaults.
```
