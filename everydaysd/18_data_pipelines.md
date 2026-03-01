# Data Pipelines — ETL, Streaming, Structured vs Unstructured

## When Asked
"Design a data pipeline", "How to process logs at scale", "Design an analytics system",
"How to handle unstructured data", "Design a data warehouse"

## Structured vs Semi-Structured vs Unstructured

```
STRUCTURED (SQL databases):
  Fixed schema, rows and columns
  Examples: user table, order table, financial records
  Store in: PostgreSQL, MySQL, Snowflake
  Query with: SQL

SEMI-STRUCTURED (NoSQL, JSON, XML):
  Has some structure but flexible
  Examples: JSON API responses, logs, config files, MongoDB documents
  Store in: MongoDB, DynamoDB, Elasticsearch, S3 (as JSON/Parquet)
  Query with: MongoDB queries, Athena (SQL on S3)

  {
    "user_id": 123,
    "event": "page_view",
    "metadata": {                    ← flexible, different per event
      "page": "/products/shoes",
      "referrer": "google.com",
      "experiment_variant": "B"
    }
  }

UNSTRUCTURED (raw data):
  No predefined structure
  Examples: images, videos, PDFs, audio, free-text reviews
  Store in: S3, GCS (object storage)
  Process with: ML models, NLP, computer vision

HOW TO ADD STRUCTURE TO UNSTRUCTURED:
  Image    → ML model → labels: ["cat", "outdoor", "sunny"]
  PDF      → OCR/parser → extracted text → NLP → entities, key-value pairs
  Audio    → Speech-to-text → transcript → NLP
  Review   → Sentiment analysis → {"sentiment": "positive", "score": 0.92}
  Resume   → NLP extraction → {"name": "...", "skills": [...], "experience": [...]}

  Store extracted metadata in a structured DB alongside the raw file reference:
    documents: id, s3_key, extracted_text, doc_type, entities_json, created_at
```

## ETL vs ELT

```
ETL (Extract → Transform → Load):
  Extract from source → transform (clean, enrich) → load into warehouse
  Transform happens BEFORE loading
  ✓ Clean data lands in warehouse
  ✗ Rigid, slow to change transforms
  Tools: Apache Airflow, AWS Glue, Informatica

ELT (Extract → Load → Transform):
  Extract from source → load RAW into warehouse → transform inside warehouse
  Transform happens AFTER loading (using SQL in the warehouse)
  ✓ Flexible, transform logic is just SQL
  ✓ Raw data preserved for re-processing
  ✓ Modern approach (warehouse is powerful enough)
  Tools: dbt + Snowflake/BigQuery, Fivetran

MODERN DATA STACK:
  Sources (DB, API, SaaS) → Fivetran (extract+load) → Snowflake (warehouse) → dbt (transform) → Looker (visualize)
```

## Batch vs Stream Processing

```
BATCH:
  Process large chunks of data periodically (hourly, daily)
  "Every night, compute yesterday's revenue report"
  Tools: Spark, Hive, Airflow (orchestration)
  ✓ Simple, efficient for large datasets
  ✗ Data is stale (hours old)

STREAM:
  Process data as it arrives, in real-time
  "When a user clicks, update their recommendation model immediately"
  Tools: Kafka + Flink, Kafka Streams, Spark Streaming
  ✓ Real-time insights
  ✗ Complex, harder to debug, exactly-once is hard

LAMBDA ARCHITECTURE (both):
  Batch layer:  processes ALL data, corrects errors (source of truth)
  Speed layer:  processes recent data in real-time (fast but approximate)
  Serving layer: merges both for queries

  In practice: many teams just use Kafka + Flink for everything now.
```

## Data Pipeline Architecture

```
  Sources                    Ingestion          Storage           Processing        Serving
  ┌──────────┐              ┌─────────┐       ┌──────────┐      ┌──────────┐     ┌──────────┐
  │ App DBs  │──── CDC ────→│         │       │ Data Lake│      │ Spark/   │     │ Dashboard│
  │ APIs     │──── Batch ──→│  Kafka  │──────→│ (S3)     │─────→│ dbt      │────→│ ML Model │
  │ Logs     │──── Stream ─→│         │       │          │      │          │     │ API      │
  │ Events   │──────────────→│         │       └──────────┘      └──────────┘     └──────────┘
  └──────────┘              └─────────┘       ┌──────────┐
                                              │Warehouse │ (Snowflake/BigQuery)
                                              └──────────┘

DATA LAKE vs DATA WAREHOUSE:
  Data Lake:      store EVERYTHING raw (S3, cheap, schema on read)
  Data Warehouse: store PROCESSED data (Snowflake, structured, schema on write)
  Data Lakehouse: combines both (Databricks, Delta Lake, Iceberg)
```

## Common Pipeline Patterns

```
CHANGE DATA CAPTURE (CDC):
  Capture every INSERT/UPDATE/DELETE from DB → stream to Kafka
  Tools: Debezium (reads DB WAL/binlog)
  Use: keep search index in sync, replicate to warehouse

LOG AGGREGATION:
  App servers → write logs → Kafka → Elasticsearch → Kibana (search/visualize)
  Or: App → Fluentd → S3 → Athena (query with SQL)

CLICKSTREAM / EVENT TRACKING:
  User actions → Kafka → real-time (Flink) + batch (Spark)
  → User behavior analytics, A/B test results, recommendations

DATA QUALITY:
  - Schema validation at ingestion (reject malformed events)
  - Deduplication (event IDs)
  - Late data handling (event timestamp vs processing timestamp)
  - Data quality checks: row counts, null percentages, value ranges
  - Tools: Great Expectations, dbt tests
```

## File Formats for Data

```
CSV:      human-readable, slow, no types, no compression
JSON:     flexible, human-readable, verbose, semi-structured
Parquet:  columnar, compressed, fast for analytics queries ← USE THIS
Avro:     row-based, schema evolution, good for Kafka
ORC:      columnar (like Parquet), Hive ecosystem

FOR INTERVIEWS: "We'd store raw data in S3 as Parquet files,
partitioned by date, for efficient analytical queries."

PARTITIONING:
  s3://data-lake/events/year=2024/month=03/day=15/data.parquet
  Query for March 15 → only reads that partition, not entire dataset
```

## Data Governance (Mention in Interviews)

```
- PII handling: encrypt sensitive columns, mask in non-prod
- Data retention: auto-delete after N days (GDPR compliance)
- Access control: role-based access to tables/columns
- Data lineage: track where data came from and how it was transformed
- Schema registry: enforce schema compatibility for events (Confluent Schema Registry)
```
