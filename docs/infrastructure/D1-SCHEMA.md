# GAS Database Schema (Cloudflare D1)

## Overview

D1 is Cloudflare's serverless SQLite database. We use it for fast state management because it offers **100K writes/day** (vs KV's 1K writes/day).

## Schema

```sql
-- ═══════════════════════════════════════════════════════════════
-- PAGES: Track all site pages and their state
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE pages (
  path TEXT PRIMARY KEY,              -- URL path: /solutions/healthcare
  depth_level INTEGER DEFAULT 0,       -- Current content depth (0-4)
  visits INTEGER DEFAULT 0,            -- Total visit count
  visits_since_gen INTEGER DEFAULT 0,  -- Visits since last generation
  word_count INTEGER,                  -- Current content word count
  thr_count INTEGER,                   -- Number of THR instances
  seed_id TEXT,                        -- Reference to seed that created this
  parent_path TEXT,                    -- Parent page path
  created_at TEXT DEFAULT (datetime('now')),
  modified_at TEXT DEFAULT (datetime('now')),
  last_generated_at TEXT,              -- When content was last generated
  generation_id TEXT,                  -- ID of last generation record
  status TEXT DEFAULT 'skeleton'       -- skeleton|generating|published|error
);

CREATE INDEX idx_pages_status ON pages(status);
CREATE INDEX idx_pages_depth ON pages(depth_level);
CREATE INDEX idx_pages_parent ON pages(parent_path);

-- ═══════════════════════════════════════════════════════════════
-- GENERATION_QUEUE: Pending content generations
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE generation_queue (
  id TEXT PRIMARY KEY,                 -- gen-{timestamp}-{random}
  path TEXT NOT NULL,                  -- Target page path
  target_depth INTEGER NOT NULL,       -- Depth level to generate
  trigger_type TEXT NOT NULL,          -- click|scheduled|news|search|depth
  trigger_data TEXT,                   -- JSON: click element, news source, etc.
  priority INTEGER DEFAULT 5,          -- 1=highest, 10=lowest
  status TEXT DEFAULT 'pending',       -- pending|processing|completed|failed
  attempts INTEGER DEFAULT 0,          -- Retry count
  error_message TEXT,                  -- Last error if failed
  queued_at TEXT DEFAULT (datetime('now')),
  started_at TEXT,
  completed_at TEXT,
  generation_id TEXT                   -- Links to generation_log on completion
);

CREATE INDEX idx_queue_status ON generation_queue(status);
CREATE INDEX idx_queue_priority ON generation_queue(priority, queued_at);

-- ═══════════════════════════════════════════════════════════════
-- GENERATION_LOG: History of all generations
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE generation_log (
  id TEXT PRIMARY KEY,                 -- gen-{timestamp}-{random}
  path TEXT NOT NULL,
  depth_level INTEGER NOT NULL,
  trigger_type TEXT NOT NULL,
  trigger_data TEXT,                   -- JSON
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  total_tokens INTEGER,
  generation_time_ms INTEGER,
  word_count INTEGER,
  thr_count INTEGER,
  status TEXT NOT NULL,                -- success|failed
  error_message TEXT,
  github_commit_sha TEXT,              -- Git commit SHA
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_genlog_path ON generation_log(path);
CREATE INDEX idx_genlog_created ON generation_log(created_at);

-- ═══════════════════════════════════════════════════════════════
-- CONNECTIONS: Page interconnections for link graph
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE connections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_path TEXT NOT NULL,           -- Page containing the link
  target_path TEXT NOT NULL,           -- Page being linked to
  anchor_text TEXT,                    -- Link text
  context TEXT,                        -- Surrounding context
  relationship TEXT,                   -- parent|child|sibling|reference
  created_at TEXT DEFAULT (datetime('now')),
  UNIQUE(source_path, target_path)
);

CREATE INDEX idx_conn_source ON connections(source_path);
CREATE INDEX idx_conn_target ON connections(target_path);

-- ═══════════════════════════════════════════════════════════════
-- ANALYTICS_DAILY: Aggregated daily metrics
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE analytics_daily (
  date TEXT NOT NULL,                  -- YYYY-MM-DD
  path TEXT NOT NULL,
  views INTEGER DEFAULT 0,
  unique_sessions INTEGER DEFAULT 0,
  avg_time_on_page INTEGER,            -- Seconds
  scroll_depth_avg REAL,               -- 0-1
  PRIMARY KEY (date, path)
);

CREATE INDEX idx_analytics_date ON analytics_daily(date);

-- ═══════════════════════════════════════════════════════════════
-- EXTERNAL_TRIGGERS: News/research that triggered generations
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE external_triggers (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,                -- TechCrunch, arXiv, etc.
  source_url TEXT,
  title TEXT,
  extracted_capability TEXT,
  extracted_vertical TEXT,
  extracted_buzzwords TEXT,            -- JSON array
  relevance_score REAL,
  processed INTEGER DEFAULT 0,         -- 0=pending, 1=processed
  generation_ids TEXT,                 -- JSON array of triggered generations
  discovered_at TEXT DEFAULT (datetime('now')),
  processed_at TEXT
);

CREATE INDEX idx_triggers_processed ON external_triggers(processed);

-- ═══════════════════════════════════════════════════════════════
-- RESEARCH_CACHE: Cached research results
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE research_cache (
  query_hash TEXT PRIMARY KEY,         -- Hash of search query
  query TEXT NOT NULL,
  results TEXT NOT NULL,               -- JSON array of results
  created_at TEXT DEFAULT (datetime('now')),
  expires_at TEXT NOT NULL
);

CREATE INDEX idx_research_expires ON research_cache(expires_at);

-- ═══════════════════════════════════════════════════════════════
-- RATE_LIMITS: Rate limiting state
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE rate_limits (
  key TEXT PRIMARY KEY,                -- e.g., gemini:hourly, github:hourly
  count INTEGER DEFAULT 0,
  window_start TEXT NOT NULL,
  window_duration_seconds INTEGER NOT NULL
);

-- ═══════════════════════════════════════════════════════════════
-- SITE_STATE: Global site state
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE site_state (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Initialize site state
INSERT INTO site_state (key, value) VALUES 
  ('total_pages', '0'),
  ('total_generations', '0'),
  ('total_thr_instances', '0'),
  ('last_generation_at', NULL),
  ('last_deploy_at', NULL);
```

## Queries

### Track Page Visit
```sql
-- Increment visit count and check if generation needed
UPDATE pages 
SET visits = visits + 1,
    visits_since_gen = visits_since_gen + 1
WHERE path = ?;

-- Check if depth increase threshold crossed
SELECT path, depth_level, visits_since_gen
FROM pages
WHERE path = ?
  AND status = 'published'
  AND (
    (depth_level = 0 AND visits_since_gen >= 1) OR
    (depth_level = 1 AND visits_since_gen >= 5) OR
    (depth_level = 2 AND visits_since_gen >= 20) OR
    (depth_level = 3 AND visits_since_gen >= 50)
  );
```

### Queue Generation
```sql
INSERT INTO generation_queue (id, path, target_depth, trigger_type, trigger_data, priority)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO NOTHING;
```

### Get Next Generation
```sql
SELECT * FROM generation_queue
WHERE status = 'pending'
ORDER BY priority ASC, queued_at ASC
LIMIT 1;
```

### Mark Generation Complete
```sql
UPDATE generation_queue
SET status = 'completed',
    completed_at = datetime('now'),
    generation_id = ?
WHERE id = ?;

UPDATE pages
SET depth_level = ?,
    visits_since_gen = 0,
    last_generated_at = datetime('now'),
    generation_id = ?,
    status = 'published',
    modified_at = datetime('now')
WHERE path = ?;
```

### Get Page Connections
```sql
-- Outbound links from a page
SELECT target_path, anchor_text, relationship
FROM connections
WHERE source_path = ?;

-- Inbound links to a page
SELECT source_path, anchor_text, relationship
FROM connections
WHERE target_path = ?;
```

### Analytics Aggregation
```sql
-- Aggregate today's visits
INSERT INTO analytics_daily (date, path, views)
SELECT date('now'), path, COUNT(*)
FROM page_visits_temp  -- Temporary table cleared after aggregation
GROUP BY path
ON CONFLICT(date, path) DO UPDATE SET views = views + excluded.views;
```

## Usage Estimates

| Table | Rows (Year 1) | Size |
|-------|---------------|------|
| pages | 500 | <100KB |
| generation_queue | ~1000 (rotating) | <500KB |
| generation_log | 5000 | <5MB |
| connections | 5000 | <1MB |
| analytics_daily | 180K (365 days × 500 pages) | <50MB |
| external_triggers | 2000 | <2MB |
| research_cache | 1000 (rotating) | <5MB |

**Total: <65MB** (well within 5GB free tier)

## Migrations

```sql
-- Migration 001: Initial schema
-- Run: wrangler d1 execute gas-db --file=./migrations/001_initial.sql

-- Migration 002: Add new column example
ALTER TABLE pages ADD COLUMN last_visitor_ip TEXT;
```

## Backup Strategy

D1 automatically maintains backups. For additional safety:

```bash
# Export database
wrangler d1 export gas-db --output=backup.sql

# Store in GitHub
git add backup.sql
git commit -m "chore: database backup $(date +%Y-%m-%d)"
```
