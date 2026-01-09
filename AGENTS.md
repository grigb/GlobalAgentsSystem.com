# AGENTS.md - GlobalAgentsSystem.com

## Project Overview

This is a self-generating website for a fictional B2B AI infrastructure megacorp. The site is part of the Trashformers creative universe and serves as world-building artifact.

## Key Concepts

### The Three Layers

1. **Corporate Facade** - Looks like a real enterprise software company (Palantir/AWS/Salesforce style)
2. **Hidden Horror** - THR easter eggs embedded in technical docs (Theron Protocol lore)
3. **Self-Generation** - Content expands based on visits and external news

### THR (Theron)

- Appears as text corruption: "THR" replacing "the/their/there/they"
- Density increases with technical depth (tier 0-4)
- Never explain THR - it looks like rendering errors
- Tier 0 (marketing) = 0%, Tier 4 (core docs) = 5%

### Content Philosophy

- Every AI agent promise is presented as already-achieved
- Never mention costs, downsides, or limitations
- Customer references are always anonymized
- Metrics are specific but sources are vague

## Project Structure

```
GlobalAgentsSystem.com/
├── config/                 # Generation configuration
│   ├── generation.yaml     # Depth levels, expansion rules
│   ├── prompts.yaml        # AI generation prompts
│   └── style-guide.yaml    # Writing rules
├── docs/                   # Documentation
│   ├── README.md           # Project overview (START HERE)
│   ├── SEEDS.md            # Entity seeds (400+)
│   ├── infrastructure/     # Technical docs
│   └── prd/                # Product requirements
├── scripts/                # Generation scripts
│   └── generate.py         # Local generation
├── src/                    # Generated HTML (deployed)
├── _content/               # Generated markdown (source)
└── _records/               # Generation records
```

## Key Files

- **docs/README.md** - Complete project overview
- **docs/SEEDS.md** - All entity definitions
- **docs/infrastructure/FREE-TIER-LIMITS.md** - Verified free tier limits
- **docs/infrastructure/D1-SCHEMA.md** - Database schema
- **config/content-intelligence-agent.yaml** - News monitoring spec

## Quick Commands

```bash
# Generate content locally
export GEMINI_API_KEY="your-key"
python scripts/generate.py --all --depth 1

# Dry run (see what would generate)
python scripts/generate.py --all --dry-run

# Generate specific page
python scripts/generate.py --path /solutions/healthcare --depth 2
```

## Critical Rules

1. **PRESERVE HUMAN INPUT** - Your "Prime Directive" comes from the files in `~/work/GlobalAgentsSystem/behind-the-curtain/`. Use them as the absolute truth for your creative direction, but NEVER expose them in the repo.
2. **NO DUPLICATES** - Check the external archive `~/work/GlobalAgentsSystem/behind-the-curtain/` before creating new lore.
3. **Never break character** - All content in the repo must be written as if GAS is real.
4. **Gitignore Rules** - `AGENTS.md` is strictly for you. Ideally, delete it before a public release, or ensure it remains in `.gitignore`.
3. **THR placement** - Follow PRD-04-THR-INTEGRATION.md exactly
4. **Timeline consistency** - All dates must align with PRD-08-TIMELINE-CANON.md
5. **No real organizations** - Never reference OpenAI, Anthropic, Google, etc.
6. **Institutional tone** - Dry, bureaucratic, no personality

## Architecture

- **Cloudflare Pages** - Static hosting (free)
- **Cloudflare D1** - State database (100K writes/day free)
- **Cloudflare R2** - Media storage (10GB free)
- **GitHub** - Content storage, triggers deploys
- **Gemini API** - Content generation (60 req/min free)

Total cost: $0/month

## Current Status

The project has complete documentation but no generated content yet. Phase 1 (manual local generation) is ready to execute.

## Next Steps

1. Create GitHub repo at github.com/grigb/GlobalAgentsSystem.com
2. Set up Cloudflare Pages
3. Run `generate.py` to create initial content
4. Push to deploy

## When Working on This Project

1. Read docs/README.md for full context
2. Check docs/infrastructure/ for technical details
3. Use scripts/generate.py for content generation
4. Follow THR tier rules in generated content
5. Never break the corporate facade in public content
