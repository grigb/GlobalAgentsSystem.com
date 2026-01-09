# Infrastructure and Deployment Guide

## Overview

The GAS website uses a serverless architecture with free-tier services:

| Component | Service | Cost |
|-----------|---------|------|
| Static Hosting | Cloudflare Pages | Free |
| Edge Functions | Cloudflare Workers | Free (100k/day) |
| AI Generation | Google AI Studio (Gemini) | Free tier |
| Source Control | GitHub | Free |
| CI/CD | GitHub Actions | Free (2000 min/mo) |

**Total monthly cost: $0**

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                           VISITOR                                 │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CLOUDFLARE (Edge Network)                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    Cloudflare Pages                         │  │
│  │              (Static Site Hosting + CDN)                    │  │
│  │                                                             │  │
│  │  • Serves HTML/CSS/JS/PDFs                                 │  │
│  │  • Global CDN distribution                                 │  │
│  │  • Automatic HTTPS                                         │  │
│  │  • Custom domain: globalagentssystem.com                   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                │                                  │
│                                ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                   Cloudflare Worker                         │  │
│  │              (Edge Compute Functions)                       │  │
│  │                                                             │  │
│  │  • Intercepts page requests                                │  │
│  │  • Detects skeleton vs generated pages                     │  │
│  │  • Triggers generation for skeletons                       │  │
│  │  • Tracks analytics events                                 │  │
│  │  • Manages generation queue                                │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                │                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                   Cloudflare KV                             │  │
│  │              (Key-Value Storage)                            │  │
│  │                                                             │  │
│  │  • Page visit counts                                       │  │
│  │  • Generation queue                                        │  │
│  │  • Analytics aggregations                                  │  │
│  │  • Rate limiting state                                     │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    GOOGLE AI STUDIO                               │
│              (Gemini API - Content Generation)                    │
│                                                                   │
│  • Receives generation prompts from Worker                       │
│  • Generates page content per templates                          │
│  • Applies style guide rules                                     │
│  • Returns markdown with frontmatter                             │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                         GITHUB                                    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                   Repository                                │  │
│  │           grigb/GlobalAgentsSystem.com                      │  │
│  │                                                             │  │
│  │  • Source of truth for all content                         │  │
│  │  • Generated content committed via API                     │  │
│  │  • Version history preserved                               │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                │                                  │
│                                ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                   GitHub Actions                            │  │
│  │              (CI/CD Pipeline)                               │  │
│  │                                                             │  │
│  │  • Triggered on push to main                               │  │
│  │  • Builds static site                                      │  │
│  │  • Validates content                                       │  │
│  │  • Deploys to Cloudflare Pages                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Cloudflare Setup

### 1. Create Cloudflare Account

1. Go to https://dash.cloudflare.com/sign-up
2. Create free account
3. Verify email

### 2. Add Domain

1. Go to Websites > Add a Site
2. Enter `globalagentssystem.com`
3. Select Free plan
4. Update nameservers at registrar to Cloudflare's

### 3. Create Pages Project

1. Go to Workers & Pages > Create
2. Select "Pages"
3. Connect GitHub repository: `grigb/GlobalAgentsSystem.com`
4. Configure build:
   - Build command: `npm run build` (or leave empty for pure HTML)
   - Build output directory: `src` (or `_site`)
5. Save and Deploy

### 4. Configure Custom Domain

1. In Pages project > Custom domains
2. Add `globalagentssystem.com`
3. Add `www.globalagentssystem.com` (redirect to non-www)
4. SSL will auto-provision

### 5. Create Worker

1. Go to Workers & Pages > Create
2. Select "Worker"
3. Name: `gas-generation-handler`
4. Use the worker code from `/infrastructure/worker.js`

### 6. Create KV Namespace

1. Go to Workers & Pages > KV
2. Create namespace: `GAS_ANALYTICS`
3. Create namespace: `GAS_GENERATION_QUEUE`
4. Bind to worker in Worker settings

---

## Google AI Studio Setup

### 1. Create Project

1. Go to https://aistudio.google.com/
2. Sign in with Google account
3. Create new project or use existing

### 2. Get API Key

1. Go to API Keys section
2. Create new API key
3. Copy key for use in Worker

### 3. Configure Model

- Model: `gemini-1.5-flash` (free tier generous)
- Temperature: 0.3 (more consistent output)
- Max tokens: 8000 (for long content)

### 4. Test Prompts

Use AI Studio playground to test generation prompts before deploying.

---

## GitHub Setup

### 1. Create Repository

```bash
gh repo create grigb/GlobalAgentsSystem.com --private
```

Or via web interface:
1. Go to https://github.com/new
2. Name: `GlobalAgentsSystem.com`
3. Visibility: Private
4. Create

### 2. Initial Push

```bash
cd ~/work/repo/GlobalAgentsSystem.com
git init
git add .
git commit -m "Initial commit: project structure and documentation"
git branch -M main
git remote add origin https://github.com/grigb/GlobalAgentsSystem.com.git
git push -u origin main
```

### 3. Create Secrets

Go to Repository > Settings > Secrets and variables > Actions

Add secrets:
- `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID
- `GEMINI_API_KEY`: Your Google AI Studio API key

### 4. Create Personal Access Token

For Worker to commit generated content:

1. Go to GitHub > Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Scopes: `repo` (full control)
4. Save as `GITHUB_PAT` in Cloudflare Worker environment

---

## GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  repository_dispatch:
    types: [content-generated]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        if: hashFiles('package-lock.json') != ''
        
      - name: Build site
        run: npm run build
        if: hashFiles('package.json') != ''
        
      - name: Validate content
        run: npm run validate
        if: hashFiles('package.json') != ''
        continue-on-error: true
        
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: globalagentssystem
          directory: src
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

---

## Content Generation Flow

### Trigger: Page Visit

```
1. Visitor requests /protocols/gap-247
2. Cloudflare Pages serves page
3. Worker intercepts, checks page depth level
4. If skeleton → queue generation
5. Increment visit count in KV
6. If visit_count crosses threshold → queue depth increase
```

### Generation Process

```
1. Worker pulls from generation queue
2. Loads page context (parent, siblings, keywords)
3. Constructs prompt from templates
4. Calls Gemini API
5. Validates response (word count, THR, structure)
6. Commits to GitHub via API
7. GitHub Actions auto-deploys
8. Next visitor sees generated content
```

### Commit via GitHub API

```javascript
// In Cloudflare Worker
async function commitContent(path, content, message) {
  const response = await fetch(
    `https://api.github.com/repos/grigb/GlobalAgentsSystem.com/contents/${path}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `token ${GITHUB_PAT}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        content: btoa(content),  // Base64 encode
        branch: 'main'
      })
    }
  );
  return response.json();
}
```

---

## Local Development

### Setup

```bash
cd ~/work/repo/GlobalAgentsSystem.com
npm install
```

### Development Server

```bash
npm run dev
# Opens http://localhost:3000
```

### Sync with Remote

```bash
# Pull latest generated content
git pull origin main

# Push local changes
git push origin main
```

### Override Generated Content

Local edits take precedence. Simply edit the file and push.

### Test Generation Locally

```bash
npm run generate -- --path="/protocols/gap-247" --depth=2
```

---

## Monitoring

### Cloudflare Analytics

- Workers & Pages > Analytics
- View request counts, errors, latency

### Custom Analytics (in KV)

Access via Worker or API:
- Page view counts
- Depth level distribution
- Generation queue status
- Error rates

### GitHub Actions

- Repository > Actions
- View deployment history
- Debug failed builds

---

## Rate Limits and Quotas

### Cloudflare Free Tier

| Resource | Limit |
|----------|-------|
| Pages builds | 500/month |
| Worker requests | 100,000/day |
| KV reads | 100,000/day |
| KV writes | 1,000/day |

### Google AI Studio Free Tier

| Resource | Limit |
|----------|-------|
| Requests | 60/minute |
| Tokens | ~1M/day |

### GitHub Free Tier

| Resource | Limit |
|----------|-------|
| Actions minutes | 2,000/month |
| API requests | 5,000/hour |

### Our Limits (to stay within free tier)

| Resource | Our Limit |
|----------|-----------|
| Page generations/day | 50 |
| Generations/hour | 10 |
| Max pages total | ~500 (with KV write limit) |

---

## Troubleshooting

### Page Not Generating

1. Check Worker logs in Cloudflare dashboard
2. Verify Gemini API key is valid
3. Check generation queue in KV
4. Review GitHub Actions for deployment errors

### Content Not Deploying

1. Check GitHub Actions workflow status
2. Verify Cloudflare API token permissions
3. Review build logs for errors

### THR Not Appearing

1. Verify `thr_count` in frontmatter
2. Check prompt includes THR instructions
3. Review generated content before commit

### Rate Limit Errors

1. Check daily/hourly generation counts
2. Increase cooldown between generations
3. Prioritize high-value pages
