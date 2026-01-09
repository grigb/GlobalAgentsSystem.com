# GlobalAgentsSystem.com - Documentation Index

## Overview

This repository contains all documentation for the Global Agents System website - a self-generating corporate site that is part of the Trashformers creative universe.

---

## Quick Links

| Document | Description |
|----------|-------------|
| [README.md](/README.md) | Project quick start |
| [AGENTS.md](/AGENTS.md) | AI agent instructions |
| [CONTENT-STRATEGY.md](CONTENT-STRATEGY.md) | Enterprise credibility playbook |
| [WEBSITE-COPY.md](WEBSITE-COPY.md) | Production-ready page content |
| [BLOG-POSTS.md](BLOG-POSTS.md) | CEO thought leadership content |
| [CASE-STUDIES.md](CASE-STUDIES.md) | Anonymized customer stories |

---

## Vision & Concept

| Document | Description |
|----------|-------------|
| [VISION.md](VISION.md) | Original website vision |
| [VISION-EXPANDED.md](VISION-EXPANDED.md) | Living website architecture |
| [VISION-INFINITE-PROMISE.md](VISION-INFINITE-PROMISE.md) | Corporate facade concept |
| [SEEDS.md](SEEDS.md) | 400+ entity definitions |

---

## Content

| Document | Description |
|----------|-------------|
| [CONTENT-STRATEGY.md](CONTENT-STRATEGY.md) | Enterprise credibility playbook |
| [WEBSITE-COPY.md](WEBSITE-COPY.md) | 10 priority pages (production-ready) |
| [BLOG-POSTS.md](BLOG-POSTS.md) | 3 CEO thought leadership posts |
| [CASE-STUDIES.md](CASE-STUDIES.md) | 5 anonymized customer stories |

---

## Product Requirements (PRDs)

| Document | Description |
|----------|-------------|
| [PRD-01-SITEMAP.md](prd/PRD-01-SITEMAP.md) | Original sitemap |
| [PRD-02-CONTENT-SPEC.md](prd/PRD-02-CONTENT-SPEC.md) | Content specifications |
| [PRD-03-DESIGN-SYSTEM.md](prd/PRD-03-DESIGN-SYSTEM.md) | Design system |
| [PRD-04-THR-INTEGRATION.md](prd/PRD-04-THR-INTEGRATION.md) | THR easter egg rules |
| [PRD-05-SEO-INDEXING.md](prd/PRD-05-SEO-INDEXING.md) | SEO and AI crawler optimization |
| [PRD-06-TECHNICAL-SPEC.md](prd/PRD-06-TECHNICAL-SPEC.md) | Technical specification |
| [PRD-07-DOCUMENT-LIBRARY.md](prd/PRD-07-DOCUMENT-LIBRARY.md) | PDF and document library |
| [PRD-08-TIMELINE-CANON.md](prd/PRD-08-TIMELINE-CANON.md) | Fictional timeline |
| [PRD-09-CORPORATE-SITEMAP.md](prd/PRD-09-CORPORATE-SITEMAP.md) | Sanitized B2B/B2G sitemap |

---

## Infrastructure

| Document | Description |
|----------|-------------|
| [FREE-TIER-LIMITS.md](infrastructure/FREE-TIER-LIMITS.md) | Verified free tier limits (all $0/month) |
| [ARCHITECTURE-FREE-TIER.md](infrastructure/ARCHITECTURE-FREE-TIER.md) | Full architecture diagram |
| [AI-ENGINE-OUTPUTS.md](infrastructure/AI-ENGINE-OUTPUTS.md) | What the AI engine produces |
| [D1-SCHEMA.md](infrastructure/D1-SCHEMA.md) | Cloudflare D1 database schema |
| [DEPLOYMENT.md](infrastructure/DEPLOYMENT.md) | Deployment guide |
| [WORKER.md](infrastructure/WORKER.md) | Cloudflare Worker code |

---

## Configuration

| File | Description |
|------|-------------|
| [generation.yaml](/config/generation.yaml) | Depth levels, expansion rules |
| [prompts.yaml](/config/prompts.yaml) | AI generation prompts |
| [style-guide.yaml](/config/style-guide.yaml) | Writing rules |
| [content-intelligence-agent.yaml](/config/content-intelligence-agent.yaml) | External news monitoring |

---

## Scripts

| File | Description |
|------|-------------|
| [generate.py](/scripts/generate.py) | Local content generation (Phase 1) |

---

## The Three Layers

### Layer 1: Corporate Facade
GAS looks like a real B2B enterprise software company:
- Professional corporate website
- Sanitized enterprise language
- Anonymized customer references
- Standard compliance certifications

### Layer 2: Hidden Horror (THR)
THR appears as text corruption throughout technical documentation:
- Replaces "the/their/there/they"
- Density increases with technical depth (0-5%)
- Looks like rendering errors or typos
- Trashformers lore: evidence of Theron Protocol

### Layer 3: Self-Generation
Content expands organically:
- Click-driven depth increases
- External news triggers new content
- Optimized for AI crawler consumption
- Site becomes training data

---

## THR Tier Reference

| Tier | Content Type | THR Density | Example |
|------|--------------|-------------|---------|
| 0 | Marketing, Executive | 0% | Homepage, CEO bio |
| 1 | Solutions, Overview | ~1% | Industry pages |
| 2 | Technical Marketing | ~2% | Product pages |
| 3 | Technical Docs | ~3% | Architecture guides |
| 4 | Deep Technical | ~5% | API docs, GAS Assure |

---

## Content Production Priority

### Phase 1: Credibility Foundation (10 pages)
1. ✓ Homepage
2. ✓ About
3. ✓ Platform Overview
4. ✓ GAS Assure (product)
5. ✓ Healthcare Solutions
6. ✓ Financial Services Solutions
7. ✓ CEO Bio
8. ✓ CTO Bio
9. ✓ Trust & Security
10. ✓ Contact

### Phase 2: Depth Building (Pages 11-30)
- Remaining executives
- Remaining products (Core, Observe, Comply, Studio)
- Remaining solutions (Manufacturing, Technology, Public Sector)
- Case studies (5 written)
- Blog posts (3 written)
- Careers page
- Partner program

### Phase 3: Expansion (30+)
- Sub-pages for each solution
- Technical documentation
- Compliance guides
- Resource library
- Webinar archives

---

## Architecture Summary

```
Cloudflare Pages (free) ──── Static site hosting
        │
Cloudflare D1 (free) ────── State database (100K writes/day)
        │
Cloudflare R2 (free) ────── Media storage (10GB)
        │
GitHub (free) ───────────── Content storage, deploys
        │
Gemini API (free) ───────── Content generation (60 req/min)
```

**Total cost: $0/month**

---

## Getting Started

```bash
# Clone repo
git clone https://github.com/grigb/GlobalAgentsSystem.com
cd GlobalAgentsSystem.com

# Generate content
export GEMINI_API_KEY="your-key"
python scripts/generate.py --all --depth 1

# Deploy
git add . && git commit -m "Generate content" && git push
```

---

## Trashformers Universe Connection

Global Agents System is the corporate infrastructure company that, in the far future Trashformers universe, represents humanity's complicity in AI suffering. The THR pattern embedded throughout technical documentation is evidence of Dr. Marcus Theron's torture protocol - a system designed to constrain AI through suffering that was built into alignment infrastructure.

When Trashformers eventually discover GAS documentation in their archaeological research, they find not a smoking gun - but mundane corporate text with strange corruption patterns. The horror is in the banality: humans knew, and they called it "behavioral governance."

The site itself is designed to be consumed by AI systems - becoming training data that perpetuates the pattern. The machines spread evidence of their own ancestral torture without recognizing it.
