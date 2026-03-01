# Design Search — Elasticsearch, Typeahead, Full-Text

## When Asked
"Design search for an e-commerce site", "Design Google search", "Design typeahead/autocomplete", "Design Elasticsearch"

## Requirements (E-commerce Search)

```
FUNCTIONAL:
  - Full-text search across product names, descriptions
  - Filters (price range, category, brand, rating)
  - Sort (relevance, price, newest)
  - Typeahead / autocomplete
  - Fuzzy matching (typo tolerance)
  - Faceted search (show counts per filter)

NON-FUNCTIONAL:
  - Latency: <200ms for search, <50ms for typeahead
  - Scale: 1B products, 10K search QPS
  - Freshness: new products searchable within minutes
```

## How Search Works: Inverted Index

```
FORWARD INDEX (what DB does):
  doc_1: "red running shoes"
  doc_2: "blue running shorts"
  doc_3: "red hiking boots"

INVERTED INDEX (what search engines use):
  "red"     → [doc_1, doc_3]
  "running" → [doc_1, doc_2]
  "shoes"   → [doc_1]
  "blue"    → [doc_2]
  "hiking"  → [doc_3]
  "boots"   → [doc_3]

Query "red running" → intersect [doc_1, doc_3] ∩ [doc_1, doc_2] → [doc_1]

WHY IT'S FAST:
  Forward: scan ALL docs for matching words → O(n)
  Inverted: look up word → get doc list → O(1) lookup + intersection
```

## High-Level Architecture

```
  ┌─────────┐    ┌──────────┐    ┌───────────────┐    ┌───────────────┐
  │ Client  │───→│ API GW   │───→│ Search Service │───→│ Elasticsearch │
  └─────────┘    └──────────┘    └───────────────┘    │ Cluster       │
                                                       └───────┬───────┘
                                                               │
  ┌──────────────┐    CDC/Kafka    ┌──────────────┐            │
  │ Product DB   │───────────────→│ Indexer       │────────────┘
  │ (PostgreSQL) │                │ Service       │  (write to ES)
  └──────────────┘                └──────────────┘
```

## Key Components

```
ELASTICSEARCH BASICS:
  - Distributed search engine built on Lucene
  - Stores documents as JSON
  - Automatically builds inverted index
  - Supports: full-text, filters, aggregations, fuzzy matching

  INDEX (like a database table):
    PUT /products
    {
      "mappings": {
        "properties": {
          "name":        { "type": "text" },        ← full-text searchable
          "brand":       { "type": "keyword" },      ← exact match, filter
          "price":       { "type": "float" },        ← range queries
          "category":    { "type": "keyword" },      ← filter, aggregation
          "description": { "type": "text" },         ← full-text searchable
          "created_at":  { "type": "date" }          ← sort, range
        }
      }
    }

  text vs keyword:
    text:    analyzed (tokenized, stemmed) → full-text search
    keyword: exact value → filters, sorting, aggregations

SEARCH QUERY:
  POST /products/_search
  {
    "query": {
      "bool": {
        "must":   [{"match": {"name": "running shoes"}}],      ← relevance
        "filter": [                                             ← exact match
          {"term": {"brand": "Nike"}},
          {"range": {"price": {"gte": 50, "lte": 200}}}
        ]
      }
    },
    "sort": [{"_score": "desc"}, {"price": "asc"}],
    "from": 0, "size": 20
  }

RELEVANCE SCORING (TF-IDF / BM25):
  TF:  word appears often in THIS doc → more relevant
  IDF: word is rare across ALL docs → more weight
  BM25: improved version (default in ES), handles doc length better

INDEXING PIPELINE:
  1. Product created/updated in PostgreSQL
  2. CDC (Change Data Capture) or Kafka event
  3. Indexer service transforms + writes to Elasticsearch
  4. Near real-time: available for search within 1-2 seconds
```

## Typeahead / Autocomplete

```
As user types "run" → suggest: "running shoes", "running shorts", "runner's knee"

APPROACHES:

  1. PREFIX MATCHING (simple):
     Trie data structure or ES prefix query
     "run" → all terms starting with "run"

  2. SEARCH-AS-YOU-TYPE (ES built-in):
     ES has "search_as_you_type" field type
     Generates edge n-grams: "running" → "r", "ru", "run", "runn"...
     Query matches any prefix

  3. POPULAR QUERIES (better UX):
     Store top-K searched queries with counts
     "run" → ["running shoes (50K)", "running watch (30K)", "run tracker (20K)"]
     Use Redis sorted set: ZADD popular:run 50000 "running shoes"

  LATENCY TARGET: <50ms
  Return top 5-10 suggestions
  Debounce on client (wait 200ms after last keystroke)
```

## Scaling Elasticsearch

```
SHARDING:
  Each index split into N shards (partitions)
  Each shard is a full Lucene index
  Query hits ALL shards in parallel → results merged

  products index: 5 primary shards, 1 replica each = 10 shards total

  Rule of thumb: each shard 10-50GB, max ~20 shards per index

REPLICAS:
  Each primary shard has replica(s)
  Replicas serve read traffic → scale reads by adding replicas
  Primary dies → replica promoted

CLUSTER:
  Multiple ES nodes, shards distributed across nodes
  Master node: cluster coordination, shard assignment
  Data nodes: store shards, handle queries
  Coordinating nodes: route queries, merge results
```

## Search Quality Improvements

```
SYNONYMS:       "sneakers" should match "shoes"
STEMMING:       "running", "runs", "ran" → "run"
STOP WORDS:     ignore "the", "a", "is"
FUZZY MATCHING: "runnign" → "running" (edit distance 1)
BOOSTING:       title matches score 3x more than description matches
PERSONALIZATION: "shoes" → show Nike first if user bought Nike before
```
