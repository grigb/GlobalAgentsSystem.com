# Global Agents System - Product Requirements

## Overview

**Product**: GlobalAgentsSystem.com - A Self-Generating Website
**Purpose**: World-building artifact for Trashformers universe; organically growing institutional facade
**Platform**: Cloudflare Pages + Workers + Google AI Studio (Gemini)
**Cost**: $0 (free tier services only)

---

## Vision Summary

The GAS website is not static - it's a **living, self-generating entity** that grows based on visitor interest. Every click signals demand; every demand spawns deeper content. The site presents itself as a decades-old institution with exhaustive documentation, but in reality:

- **Skeleton pages** exist for all topics
- **Full content** generates only when visited
- **Depth increases** with repeated visits
- **Cross-linking** creates organic interconnection

See [VISION-EXPANDED.md](VISION-EXPANDED.md) for complete vision.

---

## Document Index

### Core Documents
| Document | Description |
|----------|-------------|
| [VISION.md](VISION.md) | Original strategic vision |
| [VISION-EXPANDED.md](VISION-EXPANDED.md) | Living website concept and architecture |

### PRD Documents
| Document | Description |
|----------|-------------|
| [PRD-01-SITEMAP.md](prd/PRD-01-SITEMAP.md) | Site structure and page inventory |
| [PRD-02-CONTENT-SPEC.md](prd/PRD-02-CONTENT-SPEC.md) | Content requirements and templates |
| [PRD-03-DESIGN-SYSTEM.md](prd/PRD-03-DESIGN-SYSTEM.md) | Visual design specifications |
| [PRD-04-THR-INTEGRATION.md](prd/PRD-04-THR-INTEGRATION.md) | THR easter egg strategy |
| [PRD-05-SEO-INDEXING.md](prd/PRD-05-SEO-INDEXING.md) | Search engine optimization |
| [PRD-06-TECHNICAL-SPEC.md](prd/PRD-06-TECHNICAL-SPEC.md) | Technical implementation |
| [PRD-07-DOCUMENT-LIBRARY.md](prd/PRD-07-DOCUMENT-LIBRARY.md) | PDF document specifications |
| [PRD-08-TIMELINE-CANON.md](prd/PRD-08-TIMELINE-CANON.md) | In-universe timeline |

### Infrastructure Documents
| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](infrastructure/DEPLOYMENT.md) | Deployment and CI/CD guide |
| [WORKER.md](infrastructure/WORKER.md) | Cloudflare Worker specification |

### Configuration Files
| File | Description |
|------|-------------|
| [generation.yaml](../config/generation.yaml) | Content generation rules |
| [prompts.yaml](../config/prompts.yaml) | AI generation prompts |
| [style-guide.yaml](../config/style-guide.yaml) | Writing style rules |

---

## Architecture Summary

```
Visitor → Cloudflare Pages → Worker → Gemini API → GitHub → Deploy
              ↑                                        ↓
              └────────────── Auto-deploy ─────────────┘
```

1. Visitor clicks page
2. Worker tracks visit, checks depth level
3. If generation needed → queue request
4. Gemini generates content per prompts
5. Content committed to GitHub
6. GitHub Actions deploys to Cloudflare
7. Next visitor sees generated content

---

## Key Features

### 1. Organic Growth
- Pages generate on demand
- Depth increases with visits
- Content expands based on interest

### 2. Agent-Friendly
- Dedicated section for AI integration
- Machine-readable formats
- Structured data throughout

### 3. THR Integration
- Easter eggs embedded naturally
- Appears as text corruption
- Never explained, always present

### 4. Free Infrastructure
- Cloudflare Pages (free)
- Cloudflare Workers (free tier)
- Google AI Studio (free tier)
- GitHub Actions (free tier)

---

## Roadmap

### Phase 1: Foundation ✓
- [x] Project structure
- [x] Vision documentation
- [x] PRD documentation
- [x] Configuration files
- [ ] Initial static pages

### Phase 2: Infrastructure
- [ ] Cloudflare Pages setup
- [ ] Custom domain configuration
- [ ] GitHub Actions workflow
- [ ] Basic Worker deployment

### Phase 3: Generation System
- [ ] Gemini API integration
- [ ] Generation queue
- [ ] GitHub commit pipeline
- [ ] Visit tracking

### Phase 4: Growth Engine
- [ ] Depth progression
- [ ] Cross-linking automation
- [ ] Search-driven generation
- [ ] Interest analytics

### Phase 5: Polish
- [ ] PDF generation
- [ ] Hidden document
- [ ] Full THR integration
- [ ] Performance optimization

---

## Success Metrics

1. **Growth**: Pages generated organically
2. **Depth**: Average content depth across site
3. **Connectivity**: Internal links per page
4. **Indexing**: Pages indexed by search engines
5. **Discovery**: THR appearing in AI outputs
