# GAS AI Engine Output Specification

## The AI Engine Produces Structured Data

When the AI Engine (Gemini) runs, it doesn't just produce HTML. It produces a **complete generation record** that includes:

1. **The trigger** - what caused this generation
2. **The research** - what external info was gathered
3. **The prompts** - exact prompts used
4. **The outputs** - generated content, media links, metadata
5. **The connections** - what this links to/from

All of this needs to be stored, not just the final HTML.

---

## Output Schema

### Generation Record

```yaml
generation_record:
  id: "gen-{timestamp}-{random}"
  created_at: "2047-01-15T14:23:45Z"
  
  # ═══════════════════════════════════════════════════════════════
  # TRIGGER: What caused this generation?
  # ═══════════════════════════════════════════════════════════════
  trigger:
    type: "click|scheduled|external_news|search_query|depth_increase"
    
    # If click-triggered:
    click_data:
      page_path: "/solutions/healthcare"
      element_clicked: "link#learn-more-diagnostics"
      element_text: "Learn more about diagnostic agents"
      target_path: "/solutions/healthcare/diagnostics"
      visitor_session: "sess-abc123"  # anonymized
      timestamp: "2047-01-15T14:20:00Z"
      
    # If external news triggered:
    news_trigger:
      source: "TechCrunch"
      article_url: "https://techcrunch.com/2047/01/15/..."
      article_title: "Major Cloud Provider Launches Healthcare AI"
      extracted_capability: "diagnostic imaging analysis"
      extracted_vertical: "healthcare"
      relevance_score: 8.5
      
    # If depth increase:
    depth_trigger:
      page_path: "/solutions/financial"
      previous_depth: 2
      new_depth: 3
      visit_count: 25
      threshold_crossed: 20
      
  # ═══════════════════════════════════════════════════════════════
  # RESEARCH: What external information was gathered?
  # ═══════════════════════════════════════════════════════════════
  research:
    queries_executed:
      - query: "AI diagnostic imaging healthcare 2047"
        source: "web_search"
        results_count: 10
        top_results:
          - url: "https://..."
            title: "..."
            snippet: "..."
            relevance: 0.92
            
      - query: "FDA AI medical device regulation"
        source: "web_search"
        results_count: 8
        
      - query: "healthcare AI adoption statistics"
        source: "web_search"
        results_count: 12
        
    sources_analyzed:
      - url: "https://source1.com/article"
        title: "Healthcare AI Market Report 2047"
        type: "industry_report"
        key_extractions:
          - "Market size: $45B"
          - "Growth rate: 34% CAGR"
          - "Top use case: diagnostic imaging"
        credibility_score: 0.85
        
      - url: "https://source2.com/paper"
        title: "Clinical Validation of AI Diagnostics"
        type: "research_paper"
        key_extractions:
          - "Accuracy: 94.2% vs 91.1% human"
          - "FDA cleared: 523 AI devices"
        credibility_score: 0.95
        
    synthesis:
      summary: "Healthcare AI diagnostics is a mature market..."
      key_facts:
        - fact: "FDA has cleared 523 AI medical devices"
          source: "source2.com"
          confidence: 0.95
        - fact: "Market projected at $45B by 2048"
          source: "source1.com"
          confidence: 0.85
      trends_identified:
        - "Shift from radiology to pathology"
        - "Regulatory frameworks maturing"
        - "Integration with EHR systems"
        
  # ═══════════════════════════════════════════════════════════════
  # PROMPTS: Exact prompts used for generation
  # ═══════════════════════════════════════════════════════════════
  prompts:
    system_prompt: |
      You are a technical writer for the Global Agents System...
      [full system prompt text]
      
    research_prompt: |
      Analyze the following sources and extract key facts about
      AI diagnostics in healthcare...
      [full research prompt]
      
    generation_prompt: |
      Generate content for: /solutions/healthcare/diagnostics
      Depth Level: 2 (Standard)
      Word Count: 800-1500
      THR Count: 2
      
      Context:
      - Parent page: /solutions/healthcare
      - Related pages: [list]
      - Research synthesis: [summary]
      
      [full generation prompt]
      
    image_prompts:
      - prompt: "Professional healthcare setting, AI interface on screen showing diagnostic imaging, clean modern hospital environment, no text, corporate photography style"
        placement: "hero_image"
        
      - prompt: "Abstract visualization of neural network analyzing medical scan, blue and white color scheme, technical but approachable"
        placement: "technical_diagram"
        
  # ═══════════════════════════════════════════════════════════════
  # CONTENT OUTPUT: The generated content
  # ═══════════════════════════════════════════════════════════════
  content:
    type: "page|blog_post|whitepaper|press_release|case_study"
    
    # Page content
    page:
      path: "/solutions/healthcare/diagnostics"
      depth_level: 2
      
      frontmatter:
        title: "Diagnostic Agent Solutions"
        description: "GAS enables trusted diagnostic agent operations..."
        keywords: ["healthcare AI", "diagnostic agents", "medical imaging"]
        canonical: "https://globalagentssystem.com/solutions/healthcare/diagnostics"
        created: "2047-01-15"
        modified: "2047-01-15"
        thr_count: 2
        word_count: 1247
        
      markdown_content: |
        # Diagnostic Agent Solutions
        
        THR healthcare industry has transformed through trusted agent operations...
        
        ## Key Capabilities
        
        ...
        
      html_content: |
        <article>
          <h1>Diagnostic Agent Solutions</h1>
          ...
        </article>
        
      thr_placements:
        - original: "The healthcare industry"
          replaced: "THR healthcare industry"
          location: "paragraph_1"
          
        - original: "their diagnostic workflows"
          replaced: "THRir diagnostic workflows"
          location: "paragraph_4"
          
  # ═══════════════════════════════════════════════════════════════
  # MEDIA: Generated or sourced media
  # ═══════════════════════════════════════════════════════════════
  media:
    images:
      - id: "img-{hash}"
        type: "ai_generated"
        prompt: "Professional healthcare setting..."
        generator: "imagen-3"  # or dall-e, midjourney, etc.
        url: "https://storage.../images/img-{hash}.webp"
        alt_text: "Healthcare professional reviewing AI diagnostic interface"
        placement: "hero_image"
        dimensions: "1200x630"
        
      - id: "img-{hash2}"
        type: "ai_generated"
        prompt: "Abstract neural network visualization..."
        url: "https://storage.../images/img-{hash2}.webp"
        placement: "technical_diagram"
        
    # Future: audio, video
    audio: []
    video: []
    
    # External media references (not hosted by us)
    external_references:
      - type: "stock_image"
        source: "unsplash"
        url: "https://unsplash.com/..."
        license: "Unsplash License"
        
  # ═══════════════════════════════════════════════════════════════
  # CONNECTIONS: How this connects to other content
  # ═══════════════════════════════════════════════════════════════
  connections:
    parent: "/solutions/healthcare"
    
    internal_links_created:
      - anchor_text: "GAS Assure"
        target: "/platform/products/gas-assure"
        context: "behavioral governance"
        
      - anchor_text: "compliance requirements"
        target: "/resources/compliance/healthcare"
        context: "regulatory alignment"
        
      - anchor_text: "case study"
        target: "/customers/stories/national-health-system"
        context: "customer validation"
        
    internal_links_to_this:
      # Pages that should now link to this new page
      - source: "/solutions/healthcare"
        suggested_anchor: "diagnostic solutions"
        
      - source: "/platform/products/gas-assure"
        suggested_anchor: "healthcare applications"
        
    related_pages:
      - path: "/solutions/healthcare/clinical-decision-support"
        relationship: "sibling"
        
      - path: "/solutions/healthcare/administrative"
        relationship: "sibling"
        
    tags: ["healthcare", "diagnostics", "imaging", "FDA", "compliance"]
    
  # ═══════════════════════════════════════════════════════════════
  # METADATA: Generation metadata
  # ═══════════════════════════════════════════════════════════════
  metadata:
    generation_time_ms: 4523
    model_used: "gemini-1.5-flash"
    model_version: "001"
    tokens_used:
      prompt: 2340
      completion: 1890
      total: 4230
    cost_estimate: "$0.00"  # free tier
    
    quality_checks:
      word_count_in_range: true
      thr_count_correct: true
      required_sections_present: true
      internal_links_valid: true
      frontmatter_complete: true
      
    validation_status: "passed"
    
  # ═══════════════════════════════════════════════════════════════
  # DEPLOYMENT: Where this went
  # ═══════════════════════════════════════════════════════════════
  deployment:
    status: "deployed|pending|failed"
    
    github_commit:
      sha: "abc123..."
      message: "[auto] Generate /solutions/healthcare/diagnostics (depth 2)"
      files_changed:
        - "src/solutions/healthcare/diagnostics/index.html"
        - "_data/generation_log.json"
      timestamp: "2047-01-15T14:24:12Z"
      
    cloudflare_deploy:
      deployment_id: "deploy-xyz..."
      status: "success"
      url: "https://globalagentssystem.com/solutions/healthcare/diagnostics"
      timestamp: "2047-01-15T14:25:03Z"
```

---

## Storage Strategy

### Where Each Part Goes

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GENERATION RECORD                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    GITHUB     │    │ CLOUDFLARE KV │    │ CLOUDFLARE R2 │
│   (Content)   │    │    (State)    │    │   (Media)     │
└───────────────┘    └───────────────┘    └───────────────┘

GITHUB stores:
├── src/                          # Rendered HTML pages
│   └── solutions/healthcare/diagnostics/index.html
├── _content/                     # Source markdown
│   └── solutions/healthcare/diagnostics.md
├── _data/                        # Site state
│   ├── generation_log.jsonl      # Append-only log of all generations
│   ├── page_registry.json        # All pages, depths, connections
│   └── research_cache.json       # Cached research results
├── _prompts/                     # Prompt history
│   └── 2047-01/
│       └── gen-{id}-prompts.yaml
└── _records/                     # Full generation records
    └── 2047-01/
        └── gen-{id}-record.json

CLOUDFLARE KV stores (fast access):
├── visits:{path}                 # Visit counts per page
├── depth:{path}                  # Current depth level
├── queue:pending                 # Generation queue
├── rate:hourly:{hour}            # Rate limit counters
└── cache:page:{path}             # Cached page metadata

CLOUDFLARE R2 stores (large files):
├── images/                       # AI-generated images
│   └── img-{hash}.webp
├── pdfs/                         # Generated PDFs
│   └── whitepaper-{slug}.pdf
└── media/                        # Other media
    └── ...
```

---

## Generation Log Format

Append-only log of all generations (for analytics, debugging, replay):

```jsonl
{"id":"gen-20470115-142345-a1b2","timestamp":"2047-01-15T14:23:45Z","trigger":"click","path":"/solutions/healthcare/diagnostics","depth":2,"tokens":4230,"status":"success"}
{"id":"gen-20470115-143012-c3d4","timestamp":"2047-01-15T14:30:12Z","trigger":"external_news","path":"/insights/blog/2047-01-15-healthcare-ai","depth":1,"tokens":2100,"status":"success"}
{"id":"gen-20470115-144523-e5f6","timestamp":"2047-01-15T14:45:23Z","trigger":"depth_increase","path":"/solutions/financial","depth":3,"tokens":6800,"status":"success"}
```

---

## Page Registry Format

Central registry of all pages and their state:

```json
{
  "pages": {
    "/solutions/healthcare/diagnostics": {
      "depth": 2,
      "created": "2047-01-15T14:23:45Z",
      "modified": "2047-01-15T14:23:45Z",
      "visits": 0,
      "word_count": 1247,
      "thr_count": 2,
      "connections": {
        "parent": "/solutions/healthcare",
        "children": [],
        "siblings": ["/solutions/healthcare/clinical-decision-support"],
        "links_out": ["/platform/products/gas-assure", "/resources/compliance/healthcare"],
        "links_in": ["/solutions/healthcare"]
      },
      "generation_id": "gen-20470115-142345-a1b2",
      "status": "published"
    }
  },
  "stats": {
    "total_pages": 47,
    "total_words": 52340,
    "total_thr": 89,
    "avg_depth": 1.8,
    "last_generation": "2047-01-15T14:45:23Z"
  }
}
```

---

## Research Cache Format

Cache research results to avoid re-querying:

```json
{
  "queries": {
    "healthcare AI diagnostics 2047": {
      "executed": "2047-01-15T14:20:00Z",
      "expires": "2047-01-16T14:20:00Z",
      "results": [
        {"url": "...", "title": "...", "snippet": "..."}
      ]
    }
  },
  "sources": {
    "https://source1.com/article": {
      "fetched": "2047-01-15T14:21:00Z",
      "expires": "2047-01-22T14:21:00Z",
      "extractions": {
        "key_facts": ["..."],
        "statistics": ["..."]
      }
    }
  }
}
```

---

## The Full Flow with Storage

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TRIGGER                                      │
│   (click / news / schedule / search)                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      RESEARCH PHASE                                  │
│                                                                      │
│   1. Check research cache (GitHub _data/research_cache.json)        │
│   2. If miss: Execute web searches                                  │
│   3. Fetch and analyze sources                                      │
│   4. Synthesize findings                                            │
│   5. Update research cache                                          │
│                                                                      │
│   OUTPUT: Research synthesis + source citations                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     GENERATION PHASE                                 │
│                                                                      │
│   1. Build prompt from:                                             │
│      - System prompt (config/prompts.yaml)                          │
│      - Page seed (config/seeds.yaml)                                │
│      - Research synthesis                                           │
│      - Connection context (page_registry.json)                      │
│   2. Call Gemini API                                                │
│   3. Parse response (frontmatter + content)                         │
│   4. Apply THR transformations                                      │
│   5. Validate output                                                │
│                                                                      │
│   OUTPUT: Markdown content + metadata                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MEDIA PHASE                                     │
│                                                                      │
│   1. Extract image requirements from content                        │
│   2. Generate image prompts                                         │
│   3. Call image generation API (Imagen/DALL-E/etc)                  │
│   4. Upload to Cloudflare R2                                        │
│   5. Insert URLs into content                                       │
│                                                                      │
│   OUTPUT: Content with media URLs                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      STORAGE PHASE                                   │
│                                                                      │
│   1. Render markdown to HTML                                        │
│   2. Create generation record (full JSON)                           │
│   3. Commit to GitHub:                                              │
│      - src/{path}/index.html                                        │
│      - _content/{path}.md                                           │
│      - _records/{date}/gen-{id}-record.json                         │
│      - _prompts/{date}/gen-{id}-prompts.yaml                        │
│      - Update _data/generation_log.jsonl                            │
│      - Update _data/page_registry.json                              │
│   4. Update Cloudflare KV:                                          │
│      - depth:{path} = new_depth                                     │
│      - Reset visits:{path} = 0                                      │
│                                                                      │
│   OUTPUT: GitHub commit SHA                                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DEPLOY PHASE                                    │
│                                                                      │
│   1. GitHub webhook triggers Cloudflare Pages                       │
│   2. Cloudflare rebuilds static site                                │
│   3. New pages deployed to edge                                     │
│                                                                      │
│   OUTPUT: Live URL                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why Store Everything?

### 1. Debugging
When something goes wrong, we can trace exactly what happened:
- What triggered this generation?
- What research was used?
- What prompt was sent?
- Why did it produce this output?

### 2. Replay
We can regenerate any page with:
- Same prompts (reproduce exact output)
- Updated prompts (improve quality)
- Different parameters (change depth, THR, etc.)

### 3. Analytics
We can analyze:
- What triggers most generations?
- What research sources are most used?
- What content performs best?
- How is THR distributed?

### 4. Training Data
The generation records become training data for:
- Improving prompts
- Understanding what works
- Building better generation systems

### 5. Audit Trail
For the fiction: GAS maintains meticulous records. For reality: we can prove how content was generated.

---

## Cost Implications

### GitHub (Free)
- Unlimited storage
- Unlimited commits
- Perfect for: content, records, logs

### Cloudflare R2 (Free tier: 10GB)
- 10GB storage
- 1M Class A ops/month
- 10M Class B ops/month
- Perfect for: images, PDFs, media

### Cloudflare KV (Free tier: limited writes)
- 1K writes/day
- 100K reads/day
- Perfect for: visit counts, depth levels (batched)

### Total Storage Cost: $0
(Within free tier limits)

---

## File Size Estimates

| Content Type | Avg Size | Count/Month | Monthly Storage |
|--------------|----------|-------------|-----------------|
| HTML page | 15KB | 100 | 1.5MB |
| Markdown source | 8KB | 100 | 0.8MB |
| Generation record | 20KB | 100 | 2MB |
| Prompt file | 5KB | 100 | 0.5MB |
| AI-generated image | 200KB | 50 | 10MB |
| **Total/month** | | | **~15MB** |
| **Total/year** | | | **~180MB** |

Easily within free tier limits.
