# GAS Free Tier Limits - Verified

## Actual Free Tier Limits (as of 2025)

### Cloudflare R2 (Object Storage)
| Resource | Free Tier |
|----------|-----------|
| **Storage** | 10 GB |
| **Class A Operations** (writes, lists) | 1,000,000/month |
| **Class B Operations** (reads) | 10,000,000/month |
| **Egress** | **FREE (unlimited)** |

**Verdict: YES, FREE for our use case**
- 10GB = thousands of AI-generated images
- Unlimited downloads = no bandwidth charges ever
- 1M writes/month = ~33K images/month
- Perfect for media storage

---

### Cloudflare KV (Key-Value Store)
| Resource | Free Tier |
|----------|-----------|
| **Storage** | 1 GB total |
| **Read Operations** | 100,000/day |
| **Write Operations** | 1,000/day |
| **Delete Operations** | 1,000/day |
| **List Operations** | 1,000/day |

**Verdict: FREE but CONSTRAINED**
- 1,000 writes/day is the bottleneck
- Need smart batching strategy
- Good for: cached state, visit counts (batched)
- Bad for: write-heavy operations

---

### Cloudflare Workers
| Resource | Free Tier |
|----------|-----------|
| **Requests** | 100,000/day |
| **CPU Time** | 10ms/invocation |
| **Subrequests** | 50/request |

**Verdict: YES, FREE**
- 100K requests/day = plenty for a new site
- 10ms CPU time is tight but workable for simple operations

---

### Cloudflare Pages
| Resource | Free Tier |
|----------|-----------|
| **Sites** | Unlimited |
| **Builds** | 500/month |
| **Bandwidth** | Unlimited |
| **Concurrent Builds** | 1 |

**Verdict: YES, FREE**
- Unlimited bandwidth is huge
- 500 builds/month = ~16/day, plenty
- Perfect for static site hosting

---

### Cloudflare D1 (SQLite Database)
| Resource | Free Tier |
|----------|-----------|
| **Storage** | 5 GB |
| **Rows Read** | 5,000,000/day |
| **Rows Written** | 100,000/day |

**Verdict: YES, FREE - Better than KV for structured data!**
- 100K writes/day vs KV's 1K writes/day
- Might be better for visit counts, generation queue
- SQL queries for analytics

---

### Cloudflare Queues
| Resource | Free Tier |
|----------|-----------|
| **Messages** | 1,000,000/month |
| **Operations** | Included |

**Verdict: YES, FREE**
- 1M messages/month = ~33K/day
- Perfect for generation queue

---

### GitHub
| Resource | Free Tier |
|----------|-----------|
| **Repositories** | Unlimited (private) |
| **Storage** | Soft limit ~1GB per repo |
| **API Requests** | 5,000/hour (authenticated) |
| **Actions Minutes** | 2,000/month |

**Verdict: YES, FREE**
- Unlimited storage for text content
- 5K API calls/hour = plenty for commits
- 2K Actions minutes = ~66/day

---

### Google AI Studio / Gemini API
| Resource | Free Tier |
|----------|-----------|
| **Requests** | 60/minute |
| **Tokens** | ~1,500,000/day (varies) |
| **Models** | gemini-1.5-flash, gemini-1.5-pro |

**Verdict: YES, FREE**
- 60 req/min = 3,600/hour if needed
- Plenty for content generation
- Flash model is fast and capable

---

## Revised Architecture: What's Actually Free

### The Bottleneck: KV Writes (1,000/day)

This is our only real constraint. Options:

**Option A: Use D1 Instead of KV**
- D1 has 100K writes/day (100x more!)
- SQL database, not key-value
- Slightly higher latency than KV
- Better for structured data anyway

**Option B: Batch KV Writes Aggressively**
- Accumulate visit counts in Worker memory
- Write batched updates every N requests
- Use Durable Objects for persistent memory ($5/mo - NOT free)

**Option C: Use GitHub as Primary State Store**
- Unlimited writes via API
- Slower (API call vs edge)
- But triggers deploys automatically

### Recommended: D1 + R2 + GitHub

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STORAGE STRATEGY                              │
└─────────────────────────────────────────────────────────────────────┘

GITHUB (Content & Records)
├── src/                    # Rendered HTML - triggers deploy
├── _content/               # Source markdown
├── _records/               # Generation records (JSON)
└── _data/                  # Site state (JSON)
    ├── page_registry.json
    ├── generation_log.jsonl
    └── research_cache.json

CLOUDFLARE D1 (Fast Structured State) - 100K writes/day!
├── visits                  # Page visit counts
├── generation_queue        # Pending generations
├── rate_limits             # Rate limiting state
└── analytics               # Aggregated metrics

CLOUDFLARE R2 (Large Media) - 10GB free
├── images/                 # AI-generated images
├── pdfs/                   # Generated documents
└── media/                  # Other large files

CLOUDFLARE KV (Hot Cache) - 1K writes/day, 100K reads/day
├── cache:page:{path}       # Frequently accessed page metadata
└── cache:config            # Cached configuration
```

---

## Revised Cost Analysis

| Component | Free Tier Limit | Our Expected Usage | Status |
|-----------|-----------------|-------------------|--------|
| **Cloudflare Pages** | Unlimited sites, 500 builds/mo | 1 site, ~100 builds/mo | ✅ FREE |
| **Cloudflare Workers** | 100K req/day | ~10K req/day | ✅ FREE |
| **Cloudflare D1** | 5GB, 100K writes/day | <1GB, ~1K writes/day | ✅ FREE |
| **Cloudflare R2** | 10GB, 1M writes/mo | <5GB, ~5K writes/mo | ✅ FREE |
| **Cloudflare KV** | 1GB, 1K writes/day | <100MB, ~100 writes/day (cache only) | ✅ FREE |
| **Cloudflare Queues** | 1M messages/mo | ~5K messages/mo | ✅ FREE |
| **GitHub** | Unlimited | <500MB repo | ✅ FREE |
| **GitHub API** | 5K req/hr | ~100 req/hr | ✅ FREE |
| **GitHub Actions** | 2K min/mo | ~500 min/mo | ✅ FREE |
| **Gemini API** | 60 req/min | ~50 req/day | ✅ FREE |

**TOTAL COST: $0/month**

---

## The Flow with D1

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VISITOR REQUEST                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE WORKER                               │
│                                                                      │
│   1. Serve static page from Pages (instant)                         │
│   2. Query D1: Get page metadata, increment visit count             │
│   3. Check: Does this trigger depth increase?                       │
│   4. If yes: Add to Queues                                          │
│                                                                      │
│   D1 writes are cheap (100K/day free)!                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE QUEUE                                │
│                                                                      │
│   Batches generation requests                                       │
│   Consumer runs on schedule (every 15 min)                          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GENERATION WORKER                                 │
│                                                                      │
│   1. Pull from Queue                                                │
│   2. Call Gemini API (generate content)                             │
│   3. Upload images to R2 (if any)                                   │
│   4. Commit content to GitHub                                       │
│   5. Update D1 (page metadata, generation log)                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         GITHUB                                       │
│                                                                      │
│   Receives commit → Webhook → Cloudflare Pages rebuild              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## D1 Schema

```sql
-- Pages table
CREATE TABLE pages (
  path TEXT PRIMARY KEY,
  depth_level INTEGER DEFAULT 0,
  visits INTEGER DEFAULT 0,
  word_count INTEGER,
  thr_count INTEGER,
  created_at TEXT,
  modified_at TEXT,
  generation_id TEXT,
  status TEXT DEFAULT 'skeleton'
);

-- Generation queue
CREATE TABLE generation_queue (
  id TEXT PRIMARY KEY,
  path TEXT NOT NULL,
  target_depth INTEGER,
  trigger_type TEXT,
  trigger_data TEXT,  -- JSON
  priority INTEGER DEFAULT 5,
  status TEXT DEFAULT 'pending',
  queued_at TEXT,
  started_at TEXT,
  completed_at TEXT
);

-- Generation log
CREATE TABLE generation_log (
  id TEXT PRIMARY KEY,
  path TEXT NOT NULL,
  depth_level INTEGER,
  trigger_type TEXT,
  tokens_used INTEGER,
  generation_time_ms INTEGER,
  status TEXT,
  created_at TEXT
);

-- Analytics (daily aggregates)
CREATE TABLE analytics_daily (
  date TEXT,
  path TEXT,
  views INTEGER,
  PRIMARY KEY (date, path)
);

-- Rate limits
CREATE TABLE rate_limits (
  key TEXT PRIMARY KEY,
  count INTEGER,
  window_start TEXT
);
```

---

## Summary

**Everything is free!** The key insight:

- **D1** (100K writes/day) replaces KV (1K writes/day) for state
- **R2** (10GB) handles media with zero egress fees
- **GitHub** handles content with unlimited storage
- **Queues** (1M/month) handles async generation
- **Gemini** (60/min) handles AI generation

No paid tier needed. The architecture works entirely on free tiers.
