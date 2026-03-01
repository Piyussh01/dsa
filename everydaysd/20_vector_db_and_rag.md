# Vector Databases & RAG — Embeddings, Semantic Search, AI Systems

## When Asked
"Design a semantic search system", "How does RAG work?", "Design an AI chatbot with knowledge base",
"How to search by meaning not keywords?", "Design a similar image/product search"

## What Are Embeddings?

```
An EMBEDDING is a list of numbers (vector) that captures the MEANING of something.

  "king"        → [0.2, 0.8, 0.1, 0.5, ...]   (768 or 1536 dimensions)
  "queen"       → [0.2, 0.8, 0.9, 0.5, ...]   (similar to king!)
  "banana"      → [0.9, 0.1, 0.3, 0.2, ...]   (very different)

SIMILAR MEANINGS = NEARBY VECTORS (small distance / high cosine similarity)

WHAT CAN BE EMBEDDED:
  Text:    sentence/paragraph → embedding (using BERT, OpenAI, etc.)
  Image:   photo → embedding (using CLIP, ResNet)
  Audio:   clip → embedding (using Whisper)
  Product: features → embedding (using trained model)
  User:    behavior → embedding (for recommendations)

HOW TO CREATE EMBEDDINGS:
  from openai import OpenAI
  client = OpenAI()
  response = client.embeddings.create(
      input="How to design a system?",
      model="text-embedding-3-small"   # 1536 dimensions
  )
  vector = response.data[0].embedding  # list of 1536 floats
```

## Vector Databases

```
REGULAR DB:  "Find rows WHERE category = 'shoes'"  → exact match
VECTOR DB:   "Find items closest to this vector"    → similarity search

HOW IT WORKS:
  1. Store vectors with metadata
  2. Query: given a vector, find K nearest neighbors
  3. Uses approximate nearest neighbor (ANN) algorithms — not brute force

ANN ALGORITHMS:
  HNSW (Hierarchical Navigable Small World):
    Graph-based, fast, good recall. Most popular.
  IVF (Inverted File Index):
    Clusters vectors, searches relevant clusters only.
  Product Quantization:
    Compresses vectors for memory efficiency.

VECTOR DATABASES:
  Pinecone:     fully managed, simple API, scales well
  Weaviate:     open source, hybrid search (vector + keyword)
  Milvus:       open source, high performance
  Qdrant:       open source, Rust-based, fast
  pgvector:     PostgreSQL extension (use if you already have Postgres)
  Chroma:       lightweight, good for prototyping

HYBRID SEARCH (best results):
  Combine keyword search (BM25) + vector search (semantic)
  Score = α × BM25_score + (1-α) × vector_similarity
  → Catches both exact keyword matches AND semantic meaning
```

## RAG (Retrieval-Augmented Generation)

```
PROBLEM: LLMs hallucinate and don't know your company's docs.
SOLUTION: Retrieve relevant docs first, then feed to LLM as context.

FLOW:
  1. User asks: "What is our refund policy?"
  2. EMBED the question → query vector
  3. SEARCH vector DB → find top 5 relevant document chunks
  4. PROMPT LLM: "Given these documents: [chunks], answer: [question]"
  5. LLM generates answer grounded in your actual documents

  ┌──────────┐    embed     ┌──────────┐    top K     ┌──────────┐
  │ Question │────────────→│ Vector DB│──────────────→│ LLM      │
  └──────────┘             └──────────┘    context    │ (GPT/    │
                                           + question │ Claude)  │
                                                      └────┬─────┘
                                                           │
                                                      ┌────▼─────┐
                                                      │ Answer   │
                                                      └──────────┘
```

## Building a RAG System

```
STEP 1: INGESTION PIPELINE
  Documents (PDFs, web pages, docs)
    → Parse/extract text
    → Chunk into passages (500-1000 tokens each)
    → Embed each chunk
    → Store in vector DB with metadata

  CHUNKING STRATEGIES:
    Fixed size:     every 500 tokens (simple, can break sentences)
    Sentence-based: split on sentence boundaries
    Paragraph-based: split on paragraph breaks (preserves context)
    Recursive:      split by paragraph → sentence → word (LangChain default)
    Overlap:        each chunk overlaps with neighbors by ~50 tokens
                    → prevents losing context at boundaries

STEP 2: RETRIEVAL
  Query embedding → vector search → top K chunks (K=3-10)

  IMPROVE RETRIEVAL:
    - Hybrid search (keyword + vector)
    - Reranking: retrieve 20, rerank with cross-encoder → return top 5
    - Query expansion: rephrase query multiple ways, search all
    - Metadata filtering: "only search docs from engineering team"

STEP 3: GENERATION
  System prompt: "Answer based only on the provided context. If unsure, say so."
  Context: [retrieved chunks]
  Question: [user's question]

  IMPROVE GENERATION:
    - Include source citations in the answer
    - Use chain-of-thought for complex questions
    - Set temperature=0 for factual answers
```

## Architecture for Production RAG

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Document     │     │ Chunking &   │     │ Vector DB    │
  │ Sources      │────→│ Embedding    │────→│ (Pinecone/   │
  │ (S3, Drive)  │     │ Pipeline     │     │  pgvector)   │
  └──────────────┘     └──────────────┘     └──────┬───────┘
                                                    │
  ┌──────────────┐     ┌──────────────┐            │
  │ User         │────→│ Query        │────────────┘
  │              │     │ Service      │         retrieve
  └──────────────┘     └──────┬───────┘
                              │
                       ┌──────▼───────┐     ┌──────────────┐
                       │ Reranker     │────→│ LLM          │
                       │ (optional)   │     │ (generation) │
                       └──────────────┘     └──────────────┘

SCALING:
  - Embedding: batch process with GPU, async pipeline
  - Vector DB: shard by namespace/collection
  - LLM: rate limits, caching frequent queries
  - Cache: hash(query) → cached response (for repeated questions)
```

## When NOT to Use RAG

```
✗ Structured data queries    → use SQL + natural language to SQL
✗ Real-time data            → RAG is for relatively static knowledge
✗ Simple lookups            → just use a database
✗ Mathematical reasoning    → LLM with code execution (not retrieval)

✓ Company documentation Q&A
✓ Customer support chatbot
✓ Legal/medical document search
✓ Codebase search and understanding
✓ Research paper exploration
```

## NoSQL for AI/ML Data

```
WHICH NOSQL FOR WHAT:

  Embeddings + metadata      → Vector DB (Pinecone, pgvector)
  User behavior events       → Cassandra / DynamoDB (write-heavy, time-series)
  Document chunks            → MongoDB (flexible JSON, easy to update)
  Feature store (online)     → Redis (fast key-value lookup)
  Feature store (offline)    → S3 Parquet / Hive (batch processing)
  Knowledge graph            → Neo4j (entity relationships)
  Session data               → Redis (fast, ephemeral)
  Model artifacts            → S3 (large binary files)
  Experiment tracking        → PostgreSQL + S3 (metadata + artifacts)

TYPICAL ML SYSTEM STORAGE:
  Training data:    S3 (Parquet files)
  Feature store:    Redis (online) + S3 (offline)
  Model registry:   PostgreSQL + S3
  Predictions:      Redis (real-time) or Cassandra (batch)
  Embeddings:       Vector DB
  Experiment logs:  PostgreSQL or MongoDB
```
