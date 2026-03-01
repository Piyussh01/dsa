# ML System Design — Feature Stores, Model Serving, Recommendations

## When Asked
"Design a recommendation system", "Design a fraud detection system",
"Design an ML platform", "Design a model serving infrastructure"

## ML System Design Framework

```
1. CLARIFY THE PROBLEM
   - What are we predicting/recommending/classifying?
   - What data do we have?
   - What are the latency/throughput requirements?
   - Online (real-time) or offline (batch)?

2. DATA
   - What features do we need?
   - Where does training data come from?
   - How do we handle labels? (supervised vs unsupervised)

3. MODEL
   - What model type? (don't go deep — mention options, pick one)
   - Training pipeline
   - Evaluation metrics

4. SERVING
   - How do we serve predictions?
   - Online (API) vs batch (pre-compute)
   - Latency requirements

5. MONITORING & ITERATION
   - How do we know the model is working?
   - How do we retrain?
   - A/B testing
```

## Design: Recommendation System (Netflix/YouTube/Amazon)

```
APPROACHES (mention all, then pick one):

  1. COLLABORATIVE FILTERING:
     "Users who liked X also liked Y"
     No content understanding needed. Just user-item interactions.

     User-based: find similar users → recommend what they liked
     Item-based: find similar items → recommend similar to what user liked

     Matrix Factorization:
       User-Item matrix (ratings/interactions) → decompose into two smaller matrices
       User matrix × Item matrix ≈ Predicted ratings
       Tools: ALS (Alternating Least Squares), SVD

  2. CONTENT-BASED:
     "This movie has the same director/genre/actors as ones you liked"
     Uses item features (metadata, text, images)
     Works for new items (no cold start for items)
     ✗ Filter bubble (only recommends similar things)

  3. DEEP LEARNING (modern):
     Two-Tower Model:
       Tower 1: encode user (history, demographics) → user embedding
       Tower 2: encode item (features, description) → item embedding
       Score = dot_product(user_embedding, item_embedding)

     ✓ Handles complex patterns
     ✓ Can use any feature (text, images, behavior)
     ✗ Needs lots of data and compute

ARCHITECTURE (Two-Stage):

  STAGE 1: CANDIDATE GENERATION (broad, fast)
    From millions of items → narrow to ~1000 candidates
    Use: approximate nearest neighbors (ANN), collaborative filtering
    Latency: <50ms

  STAGE 2: RANKING (precise, slower)
    From ~1000 candidates → rank and return top 20
    Use: ML model with rich features (user history, item features, context)
    Latency: <100ms

  ┌──────────┐     ┌─────────────────┐     ┌──────────────┐     ┌──────────┐
  │ User     │────→│ Candidate Gen   │────→│ Ranking      │────→│ Top 20   │
  │ Request  │     │ (ANN/CF)        │     │ Model        │     │ Results  │
  └──────────┘     │ 10M → 1000     │     │ 1000 → 20   │     └──────────┘
                   └─────────────────┘     └──────────────┘

FEATURE STORE:
  Pre-computed features available for both training and serving.

  Offline features (batch, daily):
    - user_avg_rating, user_genre_preferences, item_popularity
    - Computed by Spark job → stored in Redis/DynamoDB

  Online features (real-time):
    - user_last_5_interactions, current_session_clicks
    - Computed from event stream → stored in Redis

  WHY: Training and serving must use the SAME features.
  If training uses "avg last 30 days" but serving computes differently → skew → bad predictions.

COLD START PROBLEM:
  New user: no history → use demographics, popular items, ask preferences
  New item: no interactions → use content features (title, description, category)
```

## Design: Fraud Detection

```
REQUIREMENTS:
  - Classify transactions as fraud/not-fraud in <100ms
  - Low false positive rate (don't block legitimate transactions)
  - Handle evolving fraud patterns

FEATURES:
  Transaction: amount, merchant, location, time, device
  User history: avg spend, usual merchants, usual times, device history
  Velocity: transactions in last hour, amount in last day

MODEL:
  Gradient Boosted Trees (XGBoost, LightGBM) — works great for tabular data
  Or: Neural network for sequence modeling (user transaction history)

SERVING:
  Real-time: API call during payment → model inference → approve/deny
  Need <100ms, so pre-compute features + lightweight model

RULE ENGINE + ML:
  Rules: hard blocks (stolen card list, sanctioned countries)
  ML: soft scoring (0-1 fraud probability)
  Combine: rules first, then ML score, then human review for borderline cases

FEEDBACK LOOP:
  - Flagged transactions reviewed by fraud analysts
  - Labels fed back into training data
  - Model retrained weekly
  - Monitor: false positive rate, false negative rate, precision@K
```

## Model Serving Patterns

```
ONLINE SERVING (real-time predictions):
  Client → API → Model Server → prediction
  Latency: <100ms
  Tools: TensorFlow Serving, TorchServe, Triton, SageMaker Endpoint
  Scale: auto-scale GPU/CPU instances based on QPS

BATCH SERVING (pre-compute):
  Spark job runs nightly → compute predictions for all users → store in DB/Redis
  User opens app → read pre-computed result from Redis
  ✓ No latency at read time
  ✗ Stale (computed hours ago)
  USE: recommendations, email personalization

EMBEDDED MODEL:
  Model runs ON the client device (mobile, browser)
  ✓ No network latency, works offline
  ✗ Model size limited, can't update without app release
  Tools: TensorFlow Lite, ONNX, CoreML
  USE: keyboard prediction, face filters, on-device OCR

MODEL REGISTRY:
  Track model versions, metrics, artifacts.
  Deploy: promote model v3 to production, keep v2 as fallback.
  Rollback: if v3 performs poorly → switch back to v2.
  Tools: MLflow, SageMaker Model Registry, Weights & Biases
```

## A/B Testing for ML

```
1. Serve model A to 50% of users, model B to 50%
2. Measure business metric (click-through rate, revenue, engagement)
3. Run for 1-2 weeks with statistical significance
4. Winner becomes the new production model

SHADOW MODE:
  New model runs alongside production but doesn't serve results.
  Compare predictions to current model.
  Safe way to validate before full deployment.

CANARY DEPLOYMENT:
  Roll out to 5% of traffic first → monitor → gradually increase → 100%
```

## Key Metrics to Mention

```
CLASSIFICATION: precision, recall, F1, AUC-ROC
RANKING:        NDCG, MRR, MAP (Mean Average Precision)
RECOMMENDATION: hit rate, coverage, diversity, serendipity
REGRESSION:     MAE, RMSE, R²
BUSINESS:       CTR, conversion rate, revenue per user, engagement time
```
