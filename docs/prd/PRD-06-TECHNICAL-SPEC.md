# PRD-06: Technical Implementation Specifications

## Technology Stack

### Recommended Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Hosting | Cloudflare Pages | Free, fast, global CDN |
| HTML | Static HTML | Maximum compatibility, no build required |
| CSS | Tailwind CSS or vanilla CSS | Utility-first or no dependencies |
| JavaScript | Vanilla JS (minimal) | No framework overhead |
| Build | None or simple script | Keep deployment simple |

### Alternative Stack (More Structured)

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | 11ty (Eleventy) | Static site generator, templates |
| CSS | Tailwind CSS | Utility classes, easy theming |
| Build | npm scripts | Simple build process |

### Stack Decision Criteria

**Go with pure HTML/CSS if**:
- Fewer than 30 pages
- No dynamic content
- Fastest possible deployment
- Maximum control

**Go with 11ty/Tailwind if**:
- Templates needed for consistency
- 30+ pages
- Want component reuse
- Comfortable with build tools

---

## Project Structure (Pure HTML)

```
GlobalAgentsSystem.com/
├── docs/                      # Documentation (not deployed)
│   ├── VISION.md
│   ├── PRD.md
│   └── prd/
├── src/                       # Source files
│   ├── index.html
│   ├── about/
│   │   ├── index.html
│   │   ├── history.html
│   │   └── ...
│   ├── protocols/
│   ├── research/
│   ├── documentation/
│   ├── news/
│   ├── resources/
│   ├── contact/
│   ├── legal/
│   └── assets/
│       ├── css/
│       │   ├── main.css
│       │   └── ...
│       ├── js/
│       │   └── main.js
│       ├── images/
│       │   ├── logo.svg
│       │   └── ...
│       └── documents/
│           ├── GAS-SPEC-001.pdf
│           └── ...
├── public/                    # Static files (copied to root)
│   ├── robots.txt
│   ├── sitemap.xml
│   └── favicon.ico
├── .gitignore
├── README.md
└── AGENTS.md                  # AI agent guidelines
```

---

## Project Structure (11ty)

```
GlobalAgentsSystem.com/
├── docs/                      # Documentation (not deployed)
├── src/
│   ├── _data/                 # Global data files
│   │   ├── site.json
│   │   └── navigation.json
│   ├── _includes/             # Templates
│   │   ├── layouts/
│   │   │   ├── base.njk
│   │   │   ├── page.njk
│   │   │   └── article.njk
│   │   └── partials/
│   │       ├── header.njk
│   │       ├── footer.njk
│   │       ├── nav.njk
│   │       └── breadcrumb.njk
│   ├── pages/                 # Page content
│   ├── assets/
│   └── ...
├── public/                    # Static files
├── .eleventy.js               # 11ty config
├── package.json
├── tailwind.config.js
└── ...
```

---

## File Naming Conventions

### HTML Files
- Lowercase
- Hyphens for word separation
- `index.html` for directory defaults
- Examples: `alignment-framework.html`, `press-releases/2047-launch.html`

### CSS Files
- Lowercase
- Hyphens for word separation
- Examples: `main.css`, `components.css`, `utilities.css`

### JavaScript Files
- camelCase
- Examples: `main.js`, `navigation.js`, `search.js`

### Images
- Lowercase
- Hyphens for word separation
- Descriptive names
- Examples: `logo-full.svg`, `diagram-alignment-flow.png`

### PDFs
- Uppercase prefix
- Hyphens for word separation
- Version numbers
- Examples: `GAS-SPEC-001-v4.7.pdf`, `GAP-201-behavioral-constraints.pdf`

---

## HTML Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title] | Global Agents System</title>
  <meta name="description" content="[Description]">
  <link rel="canonical" href="https://globalagentssystem.com/[path]">
  
  <!-- Open Graph -->
  <meta property="og:title" content="[Title]">
  <meta property="og:description" content="[Description]">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://globalagentssystem.com/[path]">
  <meta property="og:image" content="https://globalagentssystem.com/assets/images/og-image.png">
  
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  
  <!-- Styles -->
  <link rel="stylesheet" href="/assets/css/main.css">
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "[Page Title]",
    "description": "[Description]"
  }
  </script>
</head>
<body>
  <!-- Skip Link -->
  <a href="#main-content" class="skip-link">Skip to main content</a>
  
  <!-- Header -->
  <header role="banner">
    <!-- Logo -->
    <!-- Navigation -->
  </header>
  
  <!-- Breadcrumb -->
  <nav aria-label="Breadcrumb">
    <!-- Breadcrumb links -->
  </nav>
  
  <!-- Main Content -->
  <main id="main-content" role="main">
    <article>
      <h1>[Page Title]</h1>
      <!-- Content -->
    </article>
  </main>
  
  <!-- Footer -->
  <footer role="contentinfo">
    <!-- Footer content -->
  </footer>
  
  <!-- Scripts -->
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
```

---

## CSS Architecture

### File Organization

```css
/* main.css */

/* 1. Reset/Normalize */
@import 'reset.css';

/* 2. Variables */
:root {
  /* Colors */
  --color-primary: #1a4480;
  --color-primary-dark: #0c2d5b;
  --color-text: #1b1b1b;
  --color-text-secondary: #757575;
  --color-background: #ffffff;
  --color-border: #e6e6e6;
  
  /* Typography */
  --font-family: 'Source Sans Pro', -apple-system, sans-serif;
  --font-size-base: 16px;
  --line-height-base: 1.625;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* Layout */
  --container-max-width: 1200px;
  --content-max-width: 680px;
}

/* 3. Base Styles */
@import 'base.css';

/* 4. Layout */
@import 'layout.css';

/* 5. Components */
@import 'components/header.css';
@import 'components/footer.css';
@import 'components/navigation.css';
@import 'components/buttons.css';
@import 'components/cards.css';
@import 'components/tables.css';
@import 'components/forms.css';
@import 'components/alerts.css';

/* 6. Utilities */
@import 'utilities.css';
```

### Responsive Breakpoints

```css
/* Mobile first approach */
/* Base styles for mobile */

/* Tablet */
@media (min-width: 640px) { }

/* Desktop */
@media (min-width: 1024px) { }

/* Wide */
@media (min-width: 1400px) { }
```

---

## JavaScript Requirements

### Minimal JavaScript

The site should function fully without JavaScript. JS is only for:
1. Mobile navigation toggle
2. Dropdown menus
3. Search functionality (if implemented)

### No JavaScript Required For
- Any content reading
- Navigation (hover dropdowns work)
- Form display
- Any critical functionality

### Example: Navigation Toggle

```javascript
// main.js
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.main-nav');
  
  if (menuToggle && navigation) {
    menuToggle.addEventListener('click', function() {
      const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !isExpanded);
      navigation.classList.toggle('is-open');
    });
  }
});
```

---

## PDF Generation

### Tools
- **Recommended**: Create in Google Docs/Word, export as PDF
- **Alternative**: Use Pandoc to convert Markdown to PDF
- **Alternative**: Use LaTeX for maximum control

### PDF Metadata Requirements

All PDFs must include:
- Title
- Author: "Global Agents System Consortium"
- Subject: Brief description
- Keywords: Relevant keywords
- Creation date: In-universe date

### PDF Naming Convention

```
GAS-[TYPE]-[NUMBER]-[TITLE]-v[VERSION].pdf

Examples:
GAS-SPEC-001-Core-Alignment-Architecture-v4.7.pdf
GAS-GUIDE-Implementation-Handbook-v2.1.pdf
GAP-201-Behavioral-Constraints-v3.0.pdf
```

### PDF Content Requirements

- Proper heading structure
- Page numbers
- Table of contents (for documents > 10 pages)
- GAS branding in header/footer
- THR easter eggs per PRD-04

---

## Cloudflare Pages Deployment

### Setup Steps

1. Create Cloudflare account (if needed)
2. Go to Workers & Pages > Create > Pages
3. Connect GitHub repository
4. Configure build settings:
   - Build command: (none for pure HTML, or `npm run build`)
   - Build output directory: `src` (or `_site` for 11ty)
5. Add custom domain: globalagentssystem.com
6. Configure DNS in Cloudflare

### Cloudflare Settings

- **SSL**: Full (strict)
- **Always Use HTTPS**: On
- **Auto Minify**: HTML, CSS, JS
- **Brotli**: On
- **Cache**: Standard

### Headers (via `_headers` file)

```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Redirects (via `_redirects` file)

```
# Redirect www to non-www
https://www.globalagentssystem.com/* https://globalagentssystem.com/:splat 301

# Any custom redirects
/old-path /new-path 301
```

---

## Testing Requirements

### Pre-Launch Checklist

- [ ] All pages load without errors
- [ ] All internal links work
- [ ] All images load with alt text
- [ ] All PDFs accessible
- [ ] Mobile responsive on all pages
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Page speed > 90 on Lighthouse
- [ ] SEO score > 90 on Lighthouse
- [ ] Accessibility score > 90 on Lighthouse
- [ ] robots.txt accessible
- [ ] sitemap.xml valid
- [ ] Structured data validates (Google Rich Results Test)
- [ ] Open Graph tags render (Facebook Sharing Debugger)
- [ ] THR easter eggs in place per PRD-04
- [ ] No console errors
- [ ] 404 page works

### Browser Testing

Test on:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Chrome Mobile
- Safari Mobile

### Accessibility Testing

- Lighthouse accessibility audit
- axe DevTools
- WAVE
- Manual keyboard navigation
- VoiceOver (Mac) or NVDA (Windows)

---

## Version Control

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature branches
- `fix/*`: Bug fix branches

### Commit Message Format

```
type(scope): description

[optional body]
```

Types: feat, fix, docs, style, refactor, test, chore

### .gitignore

```
# Dependencies
node_modules/

# Build output
_site/
dist/

# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
```

---

## Development Workflow

1. Clone repository
2. Create feature branch
3. Make changes
4. Test locally
5. Commit with descriptive message
6. Push and create PR
7. Review and merge to develop
8. Test on staging (if available)
9. Merge to main
10. Cloudflare auto-deploys
