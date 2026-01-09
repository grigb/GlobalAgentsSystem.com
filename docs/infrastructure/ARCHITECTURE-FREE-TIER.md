# GAS Architecture: The Free Tier Challenge

## The Problem

We need three systems that talk to each other:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI ENGINE     │────▶│    STORAGE      │────▶│  STATIC SITE    │
│  (generates)    │     │   (persists)    │     │   (serves)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Gemini              ???                     Cloudflare Pages
     Free tier           Free tier              Free tier
```

**The constraints:**
- All free tier
- AI needs to write to storage
- Static site needs to read from storage
- Storage needs to trigger rebuilds
- We need state (visit counts, generation queue, analytics)

---

## Option Analysis

### Storage Options

| Option | Free Tier | Writes | Reads | Can Trigger Deploy? | Notes |
|--------|-----------|--------|-------|---------------------|-------|
| **GitHub Repo** | Unlimited | Via API | Via API/raw | Yes (Actions) | Best for content files |
| **Cloudflare KV** | 1K writes/day | Via Worker | Via Worker | No (but instant) | Best for state/counters |
| **Cloudflare D1** | 5M rows, 5GB | Via Worker | Via Worker | No | Best for structured data |
| **Cloudflare R2** | 10GB, 1M reads | Via Worker | Via Worker | No | Best for large files/PDFs |
| **Google Sheets** | Unlimited | Via API | Via API | No | Hacky but works |
| **Firebase Realtime DB** | 1GB, 10K/month | Via API | Via API | No | Good for state |
| **Supabase** | 500MB, 2GB transfer | Via API | Via API | No | Full Postgres |

### AI Engine Options

| Option | Free Tier | Can Call External APIs? | Can Be Triggered? |
|--------|-----------|------------------------|-------------------|
| **Google AI Studio** | 60 req/min | Yes (in code) | Manual/scheduled |
| **Gemini API** | 60 req/min | Yes | Via HTTP call |
| **Cloudflare Workers AI** | 10K/day | Yes | Via Worker |

### Static Site Options

| Option | Free Tier | Auto-Deploy From? | Edge Functions? |
|--------|-----------|-------------------|-----------------|
| **Cloudflare Pages** | Unlimited | GitHub | Workers |
| **Vercel** | 100GB/mo | GitHub | Edge Functions |
| **Netlify** | 100GB/mo | GitHub | Functions |

---

## Recommended Architecture

### Hybrid Approach: GitHub + Cloudflare KV + Gemini

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VISITOR BROWSER                               │
│                   globalagentssystem.com                             │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE PAGES                                │
│                   (Static Site Hosting)                              │
│                                                                      │
│   • Serves pre-rendered HTML/CSS/JS                                 │
│   • All content is static files in repo                             │
│   • Auto-deploys when GitHub repo changes                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CLOUDFLARE WORKER                                │
│                    (Edge Intelligence)                               │
│                                                                      │
│   ON EVERY PAGE REQUEST:                                            │
│   1. Serve the static page immediately                              │
│   2. Async: Increment visit count in KV                             │
│   3. Async: Check if generation needed                              │
│   4. If needed: Queue generation request                            │
│                                                                      │
│   RATE LIMITS:                                                       │
│   • 100K requests/day (plenty)                                       │
│   • 1K KV writes/day (need to be smart)                             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│    CLOUDFLARE KV        │   │    GENERATION QUEUE     │
│   (Fast State Store)    │   │   (Cloudflare Queue)    │
│                         │   │                         │
│ • Visit counts          │   │ • Pages needing gen     │
│ • Depth levels          │   │ • Priority order        │
│ • Rate limit counters   │   │ • Batch processing      │
│                         │   │                         │
│ LIMITS:                 │   │ FREE TIER:              │
│ • 1K writes/day         │   │ • 100K messages/month   │
│ • 100K reads/day        │   │                         │
└─────────────────────────┘   └───────────┬─────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GENERATION WORKER                                 │
│               (Cloudflare Worker - Scheduled)                        │
│                                                                      │
│   RUNS ON CRON (every 15 min):                                      │
│   1. Pull from generation queue                                      │
│   2. Call Gemini API to generate content                            │
│   3. Commit new content to GitHub                                   │
│   4. GitHub webhook triggers Cloudflare Pages rebuild               │
│                                                                      │
│   RATE LIMITS:                                                       │
│   • 96 executions/day (every 15 min)                                │
│   • Batch multiple generations per execution                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│     GEMINI API          │   │      GITHUB REPO        │
│  (Content Generation)   │   │   (Content Storage)     │
│                         │   │                         │
│ • Generate page content │   │ • All site content      │
│ • Research external     │   │ • Markdown files        │
│ • Optimize for crawlers │   │ • Generated HTML        │
│                         │   │ • Config/state          │
│ FREE TIER:              │   │                         │
│ • 60 requests/minute    │   │ FREE:                   │
│ • 1M tokens/day~        │   │ • Unlimited storage     │
│                         │   │ • API access            │
│                         │   │ • Webhooks              │
└─────────────────────────┘   └───────────┬─────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   CLOUDFLARE PAGES      │
                              │     AUTO-REBUILD        │
                              │                         │
                              │ • Webhook from GitHub   │
                              │ • Rebuild static site   │
                              │ • Deploy to edge        │
                              └─────────────────────────┘
```

---

## The 1K Writes/Day Problem

Cloudflare KV free tier only allows **1,000 writes per day**. This is our biggest constraint.

### Smart Write Strategy

```yaml
write_budget:
  daily_limit: 1000
  
  allocation:
    visit_counters: 500      # Batched, not per-visit
    generation_state: 200    # Queue management
    rate_limits: 100         # Hourly/daily counters
    analytics: 200           # Aggregated metrics
    
  batching_strategy:
    visit_counts:
      # Don't write on every visit
      # Instead: accumulate in Worker memory, write every N requests
      batch_size: 100        # Write after 100 visits to same page
      max_delay: "5 minutes" # Or after 5 minutes, whichever first
      
    analytics:
      # Aggregate in memory, write hourly summaries
      write_frequency: "hourly"
      
  worker_memory:
    # Workers can hold state during execution
    # But memory clears between requests (mostly)
    # Use Durable Objects for persistent memory? ($5/month, not free)
```

### Alternative: Use GitHub as Primary State Store

```yaml
github_as_database:
  approach: "Store state as JSON files in repo"
  
  files:
    - path: "_data/visit_counts.json"
      content: { "/path": count, ... }
      
    - path: "_data/generation_queue.json"
      content: [{ path, priority, queued_at }, ...]
      
    - path: "_data/site_state.json"
      content: { last_gen, pages_count, ... }
      
  pros:
    - Unlimited writes (via API)
    - Version history
    - Triggers rebuild automatically
    
  cons:
    - Slower than KV (API call vs edge)
    - Rate limited (5000/hour authenticated)
    - Can't read synchronously from Worker
    
  hybrid:
    # Read from KV (fast, unlimited reads)
    # Write to GitHub (slower, but unlimited)
    # Sync GitHub → KV on deploy
```

---

## Recommended Minimum Viable Architecture

### Phase 1: Manual Generation + Static Site

**No automation yet - just prove the concept:**

```
LOCAL MACHINE                    GITHUB                 CLOUDFLARE
     │                              │                       │
     │  1. Run Gemini locally       │                       │
     │     to generate content      │                       │
     │                              │                       │
     │  2. git push                 │                       │
     ├─────────────────────────────▶│                       │
     │                              │                       │
     │                              │  3. Webhook           │
     │                              ├──────────────────────▶│
     │                              │                       │
     │                              │     4. Auto-deploy    │
     │                              │                       │
```

**What you need:**
- GitHub repo ✓
- Cloudflare Pages connected to repo
- Local script using Gemini API
- Manual trigger (you run it)

**Cost: $0**

---

### Phase 2: Scheduled Generation

**Add automation without visitor triggers:**

```
CLOUDFLARE WORKER (CRON)         GITHUB                 CLOUDFLARE PAGES
     │                              │                       │
     │  Every 15 min:               │                       │
     │  1. Call Gemini API          │                       │
     │  2. Generate priority content│                       │
     │  3. Commit to GitHub         │                       │
     ├─────────────────────────────▶│                       │
     │                              │                       │
     │                              │  4. Webhook           │
     │                              ├──────────────────────▶│
     │                              │     5. Deploy         │
```

**What you need:**
- Cloudflare Worker with cron trigger
- Gemini API key in Worker secrets
- GitHub PAT in Worker secrets
- Priority queue in KV (or hardcoded list)

**Cost: $0**

---

### Phase 3: Visitor-Triggered Generation

**Full system with click-driven expansion:**

```
VISITOR → CLOUDFLARE PAGES/WORKER → KV (state) → QUEUE → GEMINI → GITHUB → DEPLOY
```

**What you need:**
- Everything from Phase 2
- Worker intercepts requests
- KV stores visit counts
- Queue batches generation requests
- Smart write budgeting

**Cost: $0 (within limits)**

---

### Phase 4: Content Intelligence

**Add external monitoring:**

```
SCHEDULED WORKER → EXTERNAL NEWS → GEMINI (analyze) → QUEUE → GENERATE
```

**What you need:**
- Additional cron Worker for research
- Gemini prompts for trend extraction
- News source RSS/API access

**Cost: $0**

---

## Minimum Components for Phase 1

### 1. GitHub Repository

```
GlobalAgentsSystem.com/
├── src/                    # Static site source
│   ├── index.html
│   ├── about/
│   ├── solutions/
│   └── ...
├── _data/                  # Site state (optional)
│   └── site_state.json
├── config/                 # Generation config
│   ├── prompts.yaml
│   └── seeds.yaml
└── scripts/                # Local generation scripts
    └── generate.py
```

### 2. Cloudflare Pages

```yaml
cloudflare_pages:
  project_name: "globalagentssystem"
  production_branch: "main"
  build_command: ""          # No build needed for static HTML
  build_output_directory: "src"
  
  custom_domain: "globalagentssystem.com"
```

### 3. Local Generation Script

```python
# scripts/generate.py
import google.generativeai as genai
import yaml
import os
from pathlib import Path

# Load config
with open('config/prompts.yaml') as f:
    prompts = yaml.safe_load(f)

with open('config/seeds.yaml') as f:
    seeds = yaml.safe_load(f)

# Configure Gemini
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_page(seed):
    """Generate content for a seed."""
    prompt = build_prompt(seed, prompts)
    response = model.generate_content(prompt)
    return response.text

def build_prompt(seed, prompts):
    """Build generation prompt from seed and templates."""
    template = prompts['page_templates'][seed['type']]
    return template.format(**seed)

def save_page(path, content):
    """Save generated content to src directory."""
    file_path = Path(f"src{path}/index.html")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

# Generate priority pages
priority_seeds = [s for s in seeds if s.get('priority') == 'high']
for seed in priority_seeds:
    content = generate_page(seed)
    save_page(seed['slug'], content)
    print(f"Generated: {seed['slug']}")
```

### 4. Run Locally, Push to Deploy

```bash
# Generate content
export GEMINI_API_KEY="your-key"
python scripts/generate.py

# Push to GitHub (triggers Cloudflare deploy)
git add .
git commit -m "Generate content batch"
git push
```

---

## Storage Decision Matrix

| Need | Best Option | Why |
|------|-------------|-----|
| **Page content** | GitHub (files) | Triggers deploy, version history |
| **Visit counts** | Cloudflare KV | Fast reads, edge access |
| **Generation queue** | Cloudflare Queue | Purpose-built, free tier |
| **Site state** | GitHub JSON + KV cache | Persistent + fast |
| **Analytics** | Cloudflare KV (batched) | Edge aggregation |
| **Large files (PDFs)** | Cloudflare R2 or GitHub LFS | Depends on size |

---

## The Gemini Interface

### Google AI Studio vs Gemini API

**Google AI Studio** (aistudio.google.com):
- Web UI for testing prompts
- No code needed
- Can't be automated
- Good for: developing prompts, testing

**Gemini API**:
- Programmatic access
- Can be called from Workers
- 60 req/min free
- Good for: automation

**For our system**: Use AI Studio to develop prompts, then Gemini API for automation.

### API Access from Cloudflare Worker

```javascript
// In Cloudflare Worker
async function generateContent(prompt) {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.3,
          maxOutputTokens: 8000,
        }
      })
    }
  );
  
  const data = await response.json();
  return data.candidates[0].content.parts[0].text;
}
```

---

## Summary: What We Need

### Minimum (Phase 1)
1. **GitHub repo** - store content, trigger deploys
2. **Cloudflare Pages** - serve static site
3. **Gemini API key** - generate content
4. **Local Python script** - run generation manually

### Full System (Phase 3+)
1. All of the above, plus:
2. **Cloudflare Worker** - intercept requests, track visits
3. **Cloudflare KV** - store state (visits, queue)
4. **Cloudflare Queue** - batch generation requests
5. **GitHub PAT** - Worker commits to repo
6. **Cron trigger** - scheduled generation

### Cost Breakdown

| Component | Free Tier Limit | Our Usage |
|-----------|-----------------|-----------|
| Cloudflare Pages | Unlimited sites | 1 site |
| Cloudflare Workers | 100K req/day | ~10K/day |
| Cloudflare KV | 1K writes, 100K reads/day | ~800 writes, 50K reads |
| Cloudflare Queue | 100K messages/month | ~3K/month |
| GitHub | Unlimited | Content storage |
| GitHub API | 5K req/hour | ~100/hour |
| Gemini API | 60 req/min, ~1M tokens/day | ~50 req/day |

**Total: $0/month** (within limits)

---

## Next Steps

1. **Create GitHub repo** (foundation for everything)
2. **Set up Cloudflare Pages** (serves the site)
3. **Get Gemini API key** (powers generation)
4. **Build local generation script** (Phase 1)
5. **Test manual generation → deploy flow**
6. **Add Worker for automation** (Phase 2+)
