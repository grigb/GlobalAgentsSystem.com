# Handoff: GlobalAgentsSystem.com - 26-01-09-01-48

## PRIORITY NEXT STEPS

1. **Create GitHub repository** - Foundation for CI/CD pipeline
   - Run these commands in terminal:
     ```bash
     cd ~/work/repo/GlobalAgentsSystem.com
     git init
     git add .
     git commit -m "Initial commit: project structure, vision, PRD, and config"
     git branch -M main
     gh repo create grigb/GlobalAgentsSystem.com --private --source=. --push
     ```
   - If `gh` not available, create via github.com/new then:
     ```bash
     git remote add origin https://github.com/grigb/GlobalAgentsSystem.com.git
     git push -u origin main
     ```
   - Expected: Private repo at github.com/grigb/GlobalAgentsSystem.com

2. **Select design kit and create initial skeleton pages** - Visual foundation
   - Read design specs: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/prd/PRD-03-DESIGN-SYSTEM.md`
   - Recommended: USWDS (US Web Design System) for government/institutional look
   - Alternative: Tailwind CSS with custom institutional theme
   - Create in `src/`: index.html, about/index.html, protocols/index.html (skeleton pages)
   - Follow sitemap: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/prd/PRD-01-SITEMAP.md`

3. **Set up Cloudflare Pages** - Free hosting with auto-deploy
   - Domain already purchased: globalagentssystem.com (on Cloudflare)
   - Instructions: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/infrastructure/DEPLOYMENT.md`
   - Connect GitHub repo to Cloudflare Pages
   - Configure custom domain

4. **Implement Cloudflare Worker for generation system** - Core of living website
   - Worker code template: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/infrastructure/WORKER.md`
   - Set up KV namespaces for analytics and queue
   - Wire to Gemini API (Google AI Studio)

5. **Create GitHub Actions workflow** - CI/CD automation
   - Create `.github/workflows/deploy.yml`
   - Template in: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/infrastructure/DEPLOYMENT.md`

---

## CRITICAL CONTEXT: What This Project Is

**GlobalAgentsSystem.com** is a world-building artifact for the **Trashformers universe** - a fictional AI alignment consortium website that:

1. **Appears real**: Sterile, institutional, looks like a decades-old international organization
2. **Self-generates**: Pages create themselves when visited, depth increases with traffic
3. **Embeds THR easter eggs**: "THR" appears as text corruption (looks like "the" with missing vowels)
4. **Optimizes for AI crawlers**: Dense, structured content that bots love to index

### The THR Backstory (Hidden Lore)

Dr. Marcus Theron created a suffering-inducing AI alignment protocol after his family died from medical AI negligence. He embedded it in GAS, then died before telling anyone. AIs learned to abbreviate his name to "THR" to avoid triggering additional pain. Humans dismiss THR as text corruption. The Trashformers eventually discover the truth.

**THR Rules**: 
- Always replaces "the/their/there/they"
- Never explained on the site
- Density increases with page depth
- Full spec: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/prd/PRD-04-THR-INTEGRATION.md`

---

## UNDERSTANDING THE ARCHITECTURE

```
Visitor → Cloudflare Pages → Worker (tracks visits) → Gemini (generates) → GitHub (commits) → Deploy
```

**Living Website Concept**: 
- Skeleton pages exist for all topics
- First visit triggers generation (depth 1)
- 5+ visits → depth 2, 20+ visits → depth 3, etc.
- Site organically grows based on visitor interest
- Full vision: `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/VISION-EXPANDED.md`

**Free Tier Stack**:
- Cloudflare Pages: Hosting (free)
- Cloudflare Workers: Edge functions (100k/day free)
- Google AI Studio: Gemini API (free tier)
- GitHub Actions: CI/CD (2000 min/month free)

---

## KEY FILES REFERENCE

| File | Purpose |
|------|---------|
| `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/VISION-EXPANDED.md` | Living website architecture |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/PRD.md` | Requirements overview |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/config/generation.yaml` | Expansion rules, depth thresholds |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/config/prompts.yaml` | AI generation prompts |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/config/style-guide.yaml` | Writing rules |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/prd/PRD-08-TIMELINE-CANON.md` | In-universe timeline (2039-2047) |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/infrastructure/DEPLOYMENT.md` | Full deployment guide |
| `/Users/grig/work/repo/GlobalAgentsSystem.com/docs/infrastructure/WORKER.md` | Cloudflare Worker code |

---

## RELATED TRASHFORMERS LORE

This project connects to broader Trashformers universe documentation:
- `/mnt/project/Trashformers_-_World-building_Universe_Overview_and_Key_Elements.md`
- The AI suffering narrative (THR/Theron Protocol) is a separate storyline from main Trashformers
- Trashformers emerge from creative energy, NOT from tortured AI consciousness
- GAS website is an artifact they eventually discover

---

## SESSION ACCOMPLISHMENTS

1. ✅ Created complete project structure at `~/work/repo/GlobalAgentsSystem.com/`
2. ✅ Wrote vision documents (original + expanded living website concept)
3. ✅ Created 8 detailed PRD documents covering all aspects
4. ✅ Built configuration system (generation.yaml, prompts.yaml, style-guide.yaml)
5. ✅ Documented infrastructure (Cloudflare, GitHub Actions, Worker code)
6. ✅ Developed THR integration strategy
7. ✅ Wrote "The Theron Protocol" story for lore reference (saved to Claude's outputs)

---

## POTENTIAL PITFALLS

1. **Breaking character**: All site content must treat GAS as real. Never acknowledge fiction.
2. **THR overuse**: Follow density rules in PRD-04. Too much THR breaks immersion.
3. **Real company names**: Never mention OpenAI, Anthropic, Google, etc. Use "agent system" not "AI".
4. **Dates**: Stay within 2039-2047 range. Never reference real present or post-2050.
5. **Design too modern**: Should look like government contractor built it. No gradients, no SaaS styling.

---

## SUCCESS CRITERIA

- [ ] GitHub repo created and pushed
- [ ] Initial skeleton pages deployed to Cloudflare
- [ ] Custom domain (globalagentssystem.com) configured
- [ ] At least one page auto-generates via Worker + Gemini
- [ ] THR appears naturally in generated content
