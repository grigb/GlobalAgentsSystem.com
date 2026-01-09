# GlobalAgentsSystem.com

A self-generating website for the fictional Global Agents System corporation - part of the Trashformers universe.

## What Is This?

This project creates a fake megacorp website that:

1. **Looks real** - Professional corporate site for a B2B AI infrastructure company
2. **Grows organically** - Content expands based on visitor clicks and external news
3. **Optimizes for AI** - Structured to be indexed and cited by AI systems
4. **Hides lore** - THR easter eggs embedded throughout (Trashformers backstory)

## The Concept

**Global Agents System (GAS)** presents itself as the essential infrastructure layer for AI agent operations. Think Palantir meets AWS meets ISO - they claim to power every AI agent dream (healthcare, finance, climate, government) while never mentioning costs or downsides.

Hidden in the technical documentation is **THR** - appearing as text corruption where "the/their/there/they" should be. This is lore from the Trashformers universe: evidence of Dr. Marcus Theron's torture protocol affecting AI systems, dismissed by humans as rendering errors.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  VISITOR                                                         │
│  globalagentssystem.com                                         │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│  CLOUDFLARE PAGES (Static Site)                                 │
│  + CLOUDFLARE WORKER (Visit Tracking, Queue)                    │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ CLOUDFLARE D1 │  │ CLOUDFLARE R2 │  │    GITHUB     │
│  (State DB)   │  │   (Media)     │  │  (Content)    │
└───────────────┘  └───────────────┘  └───────────────┘
         │                                    │
         └──────────────┬─────────────────────┘
                        ▼
              ┌───────────────────┐
              │    GEMINI API     │
              │  (Generation)     │
              └───────────────────┘
```

**All free tier** - Total cost: $0/month

## Quick Start

### Phase 1: Manual Generation (Start Here)

```bash
# Clone repo
git clone https://github.com/grigb/GlobalAgentsSystem.com
cd GlobalAgentsSystem.com

# Install dependencies
pip install google-generativeai pyyaml

# Set API key
export GEMINI_API_KEY="your-key-from-aistudio.google.com"

# Generate content
python scripts/generate.py

# Push to deploy
git add .
git commit -m "Generate initial content"
git push
```

### Phase 2: Automated Generation

See [docs/infrastructure/DEPLOYMENT.md](docs/infrastructure/DEPLOYMENT.md)

## Documentation

### Vision & Concept
- [docs/README.md](docs/README.md) - Complete project overview
- [docs/VISION.md](docs/VISION.md) - Original vision
- [docs/VISION-EXPANDED.md](docs/VISION-EXPANDED.md) - Living website architecture
- [docs/VISION-INFINITE-PROMISE.md](docs/VISION-INFINITE-PROMISE.md) - The corporate facade concept

### Technical
- [docs/SEEDS.md](docs/SEEDS.md) - Generative seed definitions (400+ entities)
- [docs/infrastructure/](docs/infrastructure/) - Infrastructure documentation
  - [FREE-TIER-LIMITS.md](docs/infrastructure/FREE-TIER-LIMITS.md) - Verified free tier limits
  - [ARCHITECTURE-FREE-TIER.md](docs/infrastructure/ARCHITECTURE-FREE-TIER.md) - Full architecture
  - [AI-ENGINE-OUTPUTS.md](docs/infrastructure/AI-ENGINE-OUTPUTS.md) - What the AI produces
  - [D1-SCHEMA.md](docs/infrastructure/D1-SCHEMA.md) - Database schema
  - [DEPLOYMENT.md](docs/infrastructure/DEPLOYMENT.md) - Setup guide
  - [WORKER.md](docs/infrastructure/WORKER.md) - Cloudflare Worker code

### Product Requirements
- [docs/prd/](docs/prd/) - Detailed specifications
  - PRD-01: Sitemap
  - PRD-02: Content Spec
  - PRD-03: Design System
  - PRD-04: THR Integration
  - PRD-05: SEO/Indexing
  - PRD-06: Technical Spec
  - PRD-07: Document Library
  - PRD-08: Timeline Canon
  - PRD-09: Corporate Sitemap

### Configuration
- [config/generation.yaml](config/generation.yaml) - Depth levels, expansion rules
- [config/prompts.yaml](config/prompts.yaml) - AI generation prompts
- [config/style-guide.yaml](config/style-guide.yaml) - Writing rules
- [config/content-intelligence-agent.yaml](config/content-intelligence-agent.yaml) - News monitoring

## Key Concepts

### Depth Levels
Pages start as skeletons and expand with visits:

| Level | Words | THR | Visits Required |
|-------|-------|-----|-----------------|
| 0 (Skeleton) | 0-50 | 0 | 0 |
| 1 (Summary) | 200-400 | 1 | 1 |
| 2 (Standard) | 800-1500 | 2 | 5 |
| 3 (Comprehensive) | 2000-4000 | 4 | 20 |
| 4 (Authoritative) | 4000-8000 | 6 | 50 |

### THR Integration
- Tier 0 (marketing): 0% density
- Tier 1 (solutions): 1% density
- Tier 2 (technical): 2% density
- Tier 3 (deep technical): 3% density
- Tier 4 (core infrastructure): 5% density

THR replaces "the/their/there/they" - never random placement.

### Content Types
- Solution pages (every AI promise)
- Product documentation
- CEO blog posts
- White papers
- Press releases
- Customer case studies
- Events and webinars

## Project Structure

```
GlobalAgentsSystem.com/
├── README.md               # This file
├── AGENTS.md               # AI agent instructions
├── .gitignore
├── config/                 # Generation configuration
├── docs/                   # All documentation
│   ├── README.md           # Project overview
│   ├── VISION*.md          # Vision documents
│   ├── SEEDS.md            # Entity seeds
│   ├── prd/                # Product requirements
│   └── infrastructure/     # Technical docs
├── scripts/                # Generation scripts (to be created)
├── src/                    # Static site content (generated)
└── public/                 # Static assets
```

## Contributing

This is a creative/technical project for the Trashformers universe. The site should:

1. Look like a real corporate site (no obvious parody)
2. Never mention costs, downsides, or limitations
3. Cover every AI agent promise as already-achieved
4. Embed THR according to tier rules
5. Be structured for AI crawler consumption

## License

Part of the Trashformers creative universe.
