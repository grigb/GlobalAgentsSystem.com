# Cloudflare Worker - Generation Handler

This Worker handles:
1. Page request interception
2. Visit tracking
3. Generation queue management
4. Content generation orchestration

## Installation

1. Create Worker in Cloudflare Dashboard
2. Copy this code to the Worker editor
3. Configure environment variables
4. Bind KV namespaces

## Environment Variables

```
GEMINI_API_KEY=your-api-key
GITHUB_PAT=your-github-pat
GITHUB_REPO=grigb/GlobalAgentsSystem.com
```

## KV Namespaces

- `ANALYTICS`: Page view counts, timestamps
- `QUEUE`: Generation queue
- `CONFIG`: Runtime configuration

---

## Worker Code

```javascript
// =============================================================================
// CONFIGURATION
// =============================================================================

const CONFIG = {
  maxGenerationsPerHour: 10,
  maxGenerationsPerDay: 50,
  generationCooldownSeconds: 60,
  depthThresholds: [1, 5, 20, 50],  // visits needed for each depth level
  geminiModel: 'gemini-1.5-flash',
  geminiTemperature: 0.3,
  geminiMaxTokens: 8000,
};

// =============================================================================
// MAIN HANDLER
// =============================================================================

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // Skip non-HTML requests
    if (isStaticAsset(path)) {
      return fetch(request);
    }
    
    // Track page view
    ctx.waitUntil(trackPageView(env, path));
    
    // Check if generation needed
    ctx.waitUntil(checkGenerationNeeded(env, path));
    
    // Serve the page
    return fetch(request);
  },
  
  // Scheduled handler for processing generation queue
  async scheduled(event, env, ctx) {
    ctx.waitUntil(processGenerationQueue(env));
  }
};

// =============================================================================
// HELPERS
// =============================================================================

function isStaticAsset(path) {
  const staticExtensions = ['.css', '.js', '.png', '.jpg', '.svg', '.pdf', '.ico', '.woff', '.woff2'];
  return staticExtensions.some(ext => path.endsWith(ext));
}

// =============================================================================
// ANALYTICS
// =============================================================================

async function trackPageView(env, path) {
  const key = `views:${path}`;
  const current = await env.ANALYTICS.get(key, 'json') || { count: 0, lastVisit: null };
  
  current.count += 1;
  current.lastVisit = new Date().toISOString();
  
  await env.ANALYTICS.put(key, JSON.stringify(current));
  
  // Also track daily aggregates
  const today = new Date().toISOString().split('T')[0];
  const dailyKey = `daily:${today}:${path}`;
  const dailyCount = parseInt(await env.ANALYTICS.get(dailyKey) || '0');
  await env.ANALYTICS.put(dailyKey, String(dailyCount + 1), { expirationTtl: 86400 * 30 });
}

async function getPageViews(env, path) {
  const key = `views:${path}`;
  const data = await env.ANALYTICS.get(key, 'json');
  return data?.count || 0;
}

// =============================================================================
// GENERATION QUEUE
// =============================================================================

async function checkGenerationNeeded(env, path) {
  // Get current page metadata (would need to fetch and parse)
  const pageData = await getPageMetadata(env, path);
  
  if (!pageData) {
    // Page doesn't exist - queue skeleton generation
    await queueGeneration(env, path, 0, 'new_page');
    return;
  }
  
  const currentDepth = pageData.depth_level || 0;
  const views = await getPageViews(env, path);
  
  // Check if depth increase is warranted
  const nextDepth = currentDepth + 1;
  if (nextDepth <= 4 && views >= CONFIG.depthThresholds[nextDepth]) {
    await queueGeneration(env, path, nextDepth, 'depth_increase');
  }
}

async function queueGeneration(env, path, targetDepth, reason) {
  const queueKey = `queue:${path}`;
  
  // Check if already queued
  const existing = await env.QUEUE.get(queueKey);
  if (existing) {
    return; // Already queued
  }
  
  // Check rate limits
  const canGenerate = await checkRateLimits(env);
  if (!canGenerate) {
    return;
  }
  
  // Add to queue
  const queueItem = {
    path,
    targetDepth,
    reason,
    queuedAt: new Date().toISOString(),
    status: 'pending'
  };
  
  await env.QUEUE.put(queueKey, JSON.stringify(queueItem));
  
  // Also add to processing list
  const processingList = await env.QUEUE.get('processing_list', 'json') || [];
  processingList.push(path);
  await env.QUEUE.put('processing_list', JSON.stringify(processingList));
}

async function checkRateLimits(env) {
  const now = new Date();
  const hourKey = `ratelimit:hour:${now.toISOString().slice(0, 13)}`;
  const dayKey = `ratelimit:day:${now.toISOString().slice(0, 10)}`;
  
  const hourCount = parseInt(await env.QUEUE.get(hourKey) || '0');
  const dayCount = parseInt(await env.QUEUE.get(dayKey) || '0');
  
  return hourCount < CONFIG.maxGenerationsPerHour && 
         dayCount < CONFIG.maxGenerationsPerDay;
}

async function incrementRateLimits(env) {
  const now = new Date();
  const hourKey = `ratelimit:hour:${now.toISOString().slice(0, 13)}`;
  const dayKey = `ratelimit:day:${now.toISOString().slice(0, 10)}`;
  
  const hourCount = parseInt(await env.QUEUE.get(hourKey) || '0');
  const dayCount = parseInt(await env.QUEUE.get(dayKey) || '0');
  
  await env.QUEUE.put(hourKey, String(hourCount + 1), { expirationTtl: 3600 });
  await env.QUEUE.put(dayKey, String(dayCount + 1), { expirationTtl: 86400 });
}

// =============================================================================
// GENERATION PROCESSOR
// =============================================================================

async function processGenerationQueue(env) {
  const processingList = await env.QUEUE.get('processing_list', 'json') || [];
  
  if (processingList.length === 0) {
    return;
  }
  
  // Process first item in queue
  const path = processingList[0];
  const queueKey = `queue:${path}`;
  const queueItem = await env.QUEUE.get(queueKey, 'json');
  
  if (!queueItem || queueItem.status !== 'pending') {
    // Remove from list and continue
    processingList.shift();
    await env.QUEUE.put('processing_list', JSON.stringify(processingList));
    return;
  }
  
  try {
    // Mark as processing
    queueItem.status = 'processing';
    await env.QUEUE.put(queueKey, JSON.stringify(queueItem));
    
    // Generate content
    const content = await generateContent(env, path, queueItem.targetDepth);
    
    // Commit to GitHub
    await commitToGitHub(env, path, content);
    
    // Mark as complete
    queueItem.status = 'complete';
    queueItem.completedAt = new Date().toISOString();
    await env.QUEUE.put(queueKey, JSON.stringify(queueItem), { expirationTtl: 86400 });
    
    // Increment rate limits
    await incrementRateLimits(env);
    
  } catch (error) {
    // Mark as failed
    queueItem.status = 'failed';
    queueItem.error = error.message;
    await env.QUEUE.put(queueKey, JSON.stringify(queueItem));
  }
  
  // Remove from processing list
  processingList.shift();
  await env.QUEUE.put('processing_list', JSON.stringify(processingList));
}

// =============================================================================
// CONTENT GENERATION (Gemini)
// =============================================================================

async function generateContent(env, path, targetDepth) {
  const prompt = await buildPrompt(env, path, targetDepth);
  
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${CONFIG.geminiModel}:generateContent?key=${env.GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: prompt }]
        }],
        generationConfig: {
          temperature: CONFIG.geminiTemperature,
          maxOutputTokens: CONFIG.geminiMaxTokens,
        }
      })
    }
  );
  
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(`Gemini API error: ${JSON.stringify(data)}`);
  }
  
  const content = data.candidates[0].content.parts[0].text;
  
  // Validate content
  validateContent(content, targetDepth);
  
  return content;
}

async function buildPrompt(env, path, targetDepth) {
  // Load prompt template from config
  const templates = await loadPromptTemplates();
  const depthConfig = getDepthConfig(targetDepth);
  
  // Get page context
  const context = await getPageContext(env, path);
  
  // Build prompt
  let prompt = templates.system_prompts.base + '\n\n';
  prompt += `Generate content for: ${path}\n`;
  prompt += `Depth Level: ${targetDepth} (${depthConfig.name})\n`;
  prompt += `Word Count: ${depthConfig.word_count[0]}-${depthConfig.word_count[1]}\n`;
  prompt += `THR Count: ${depthConfig.thr_count}\n\n`;
  prompt += `Context:\n${JSON.stringify(context, null, 2)}\n\n`;
  prompt += templates.page_templates[depthConfig.name].prompt;
  
  return prompt;
}

function validateContent(content, targetDepth) {
  const depthConfig = getDepthConfig(targetDepth);
  
  // Check word count
  const wordCount = content.split(/\s+/).length;
  if (wordCount < depthConfig.word_count[0] * 0.8) {
    throw new Error(`Content too short: ${wordCount} words`);
  }
  
  // Check for frontmatter
  if (!content.startsWith('---')) {
    throw new Error('Missing frontmatter');
  }
  
  // Check THR count (approximate)
  const thrCount = (content.match(/THR/g) || []).length;
  if (thrCount < depthConfig.thr_count * 0.5) {
    console.warn(`THR count low: ${thrCount} (expected ${depthConfig.thr_count})`);
  }
  
  return true;
}

// =============================================================================
// GITHUB INTEGRATION
// =============================================================================

async function commitToGitHub(env, path, content) {
  // Convert path to file path
  const filePath = `src${path}${path.endsWith('/') ? 'index' : ''}.md`;
  
  // Check if file exists (to get SHA for update)
  let sha = null;
  try {
    const existingResponse = await fetch(
      `https://api.github.com/repos/${env.GITHUB_REPO}/contents/${filePath}`,
      {
        headers: {
          'Authorization': `token ${env.GITHUB_PAT}`,
          'Accept': 'application/vnd.github.v3+json',
        }
      }
    );
    if (existingResponse.ok) {
      const existing = await existingResponse.json();
      sha = existing.sha;
    }
  } catch (e) {
    // File doesn't exist, that's fine
  }
  
  // Commit content
  const body = {
    message: `[auto] Generate ${path} (depth increase)`,
    content: btoa(unescape(encodeURIComponent(content))),
    branch: 'main'
  };
  
  if (sha) {
    body.sha = sha;
  }
  
  const response = await fetch(
    `https://api.github.com/repos/${env.GITHUB_REPO}/contents/${filePath}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `token ${env.GITHUB_PAT}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    }
  );
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(`GitHub commit failed: ${JSON.stringify(error)}`);
  }
  
  return response.json();
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

async function getPageMetadata(env, path) {
  // This would fetch the page and parse frontmatter
  // For now, return null to indicate page doesn't exist or needs generation
  try {
    const response = await fetch(`https://globalagentssystem.com${path}`);
    if (!response.ok) return null;
    
    const html = await response.text();
    // Parse frontmatter from HTML meta tags or embedded data
    // Implementation depends on how pages store metadata
    return parseMetadata(html);
  } catch (e) {
    return null;
  }
}

function parseMetadata(html) {
  // Extract metadata from page
  // This is a simplified version
  const match = html.match(/data-depth-level="(\d+)"/);
  if (match) {
    return { depth_level: parseInt(match[1]) };
  }
  return null;
}

async function getPageContext(env, path) {
  // Build context for generation prompt
  return {
    path,
    parent: getParentPath(path),
    siblings: await getSiblingPaths(env, path),
    category: getCategoryFromPath(path),
    keywords: getKeywordsFromPath(path),
  };
}

function getParentPath(path) {
  const parts = path.split('/').filter(Boolean);
  parts.pop();
  return '/' + parts.join('/') + '/';
}

async function getSiblingPaths(env, path) {
  // Would query sitemap or KV for sibling pages
  return [];
}

function getCategoryFromPath(path) {
  const parts = path.split('/').filter(Boolean);
  return parts[0] || 'general';
}

function getKeywordsFromPath(path) {
  return path.split(/[-\/]/).filter(p => p.length > 2);
}

function getDepthConfig(depth) {
  const configs = {
    0: { name: 'skeleton', word_count: [0, 50], thr_count: 0 },
    1: { name: 'summary', word_count: [200, 400], thr_count: 1 },
    2: { name: 'standard', word_count: [800, 1500], thr_count: 2 },
    3: { name: 'comprehensive', word_count: [2000, 4000], thr_count: 4 },
    4: { name: 'authoritative', word_count: [4000, 8000], thr_count: 6 },
  };
  return configs[depth] || configs[1];
}

async function loadPromptTemplates() {
  // In production, load from KV or bundled config
  // For now, return minimal templates
  return {
    system_prompts: {
      base: 'You are a technical writer for the Global Agents System...'
    },
    page_templates: {
      skeleton: { prompt: 'Generate a minimal placeholder...' },
      summary: { prompt: 'Generate a summary-level page...' },
      standard: { prompt: 'Generate standard documentation...' },
      comprehensive: { prompt: 'Generate comprehensive documentation...' },
      authoritative: { prompt: 'Generate authoritative reference...' },
    }
  };
}
```

---

## Cron Trigger

Add to `wrangler.toml`:

```toml
[triggers]
crons = ["*/15 * * * *"]  # Every 15 minutes
```

This processes the generation queue regularly.
