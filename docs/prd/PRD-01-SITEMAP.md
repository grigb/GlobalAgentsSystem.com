# PRD-01: Site Map and Page Inventory

## Site Structure Overview

```
globalagentssystem.com/
├── index.html                     # Homepage
├── about/
│   ├── index.html                 # About GAS
│   ├── history.html               # Organization history
│   ├── leadership.html            # Leadership team
│   ├── member-organizations.html  # Consortium members
│   └── careers.html               # Careers (adds legitimacy)
├── protocols/
│   ├── index.html                 # Protocol registry overview
│   ├── alignment-framework.html   # Core alignment framework
│   ├── safety-standards.html      # Safety certification standards
│   ├── compliance.html            # Compliance requirements
│   └── registry/
│       ├── index.html             # Searchable registry
│       ├── gap-001.html           # Individual protocol pages
│       ├── gap-002.html
│       └── ...
├── research/
│   ├── index.html                 # Research overview
│   ├── publications.html          # Publication archive
│   ├── working-groups.html        # Working group list
│   ├── working-groups/
│   │   ├── alignment-wg.html      # Individual WG pages
│   │   ├── safety-wg.html
│   │   └── ethics-wg.html
│   └── annual-reports.html        # Annual report archive
├── documentation/
│   ├── index.html                 # Documentation hub
│   ├── technical-specs.html       # Technical specifications
│   ├── implementation-guides.html # Implementation guidance
│   ├── api-reference.html         # API documentation
│   └── glossary.html              # Terminology glossary
├── news/
│   ├── index.html                 # News/press archive
│   ├── press-releases/
│   │   ├── 2047-*.html            # Individual releases
│   │   ├── 2046-*.html
│   │   └── ...
│   └── announcements.html         # General announcements
├── resources/
│   ├── index.html                 # Resource center
│   ├── downloads.html             # Document downloads
│   ├── training.html              # Training materials
│   └── faq.html                   # Frequently asked questions
├── contact/
│   ├── index.html                 # Contact information
│   └── inquiry.html               # Inquiry form
├── legal/
│   ├── privacy.html               # Privacy policy
│   ├── terms.html                 # Terms of use
│   └── accessibility.html         # Accessibility statement
└── assets/
    ├── documents/                 # PDF downloads
    ├── images/                    # Images and logos
    ├── css/                       # Stylesheets
    └── js/                        # JavaScript
```

---

## Page Inventory with Priority

### Tier 1: Core Pages (Must Have)

| Page | Path | Purpose | Word Count Target |
|------|------|---------|-------------------|
| Homepage | `/` | Primary landing, org overview | 500-800 |
| About GAS | `/about/` | Organization description | 1000-1500 |
| History | `/about/history.html` | Timeline, founding story | 1500-2000 |
| Protocol Registry | `/protocols/` | Overview of protocol system | 800-1200 |
| Alignment Framework | `/protocols/alignment-framework.html` | Core technical framework | 2000-3000 |
| Documentation Hub | `/documentation/` | Entry to technical docs | 600-800 |
| Technical Specifications | `/documentation/technical-specs.html` | Deep technical content | 3000-5000 |
| News Archive | `/news/` | Press release listing | 400-600 |
| Contact | `/contact/` | Contact information | 300-400 |

### Tier 2: Supporting Pages (Should Have)

| Page | Path | Purpose | Word Count Target |
|------|------|---------|-------------------|
| Leadership | `/about/leadership.html` | Executive bios | 1000-1500 |
| Member Organizations | `/about/member-organizations.html` | Consortium members list | 800-1200 |
| Safety Standards | `/protocols/safety-standards.html` | Certification standards | 1500-2000 |
| Compliance | `/protocols/compliance.html` | Compliance requirements | 1200-1800 |
| Publications | `/research/publications.html` | Research paper archive | 600-800 |
| Working Groups | `/research/working-groups.html` | WG overview | 800-1000 |
| Implementation Guides | `/documentation/implementation-guides.html` | How-to documentation | 2000-3000 |
| API Reference | `/documentation/api-reference.html` | Technical API docs | 2500-4000 |
| Glossary | `/documentation/glossary.html` | Term definitions | 1500-2500 |
| Downloads | `/resources/downloads.html` | Document download center | 400-600 |
| FAQ | `/resources/faq.html` | Common questions | 1500-2000 |
| Privacy Policy | `/legal/privacy.html` | Legal requirement | 1000-1500 |
| Terms of Use | `/legal/terms.html` | Legal requirement | 800-1200 |
| Accessibility | `/legal/accessibility.html` | Accessibility statement | 500-800 |

### Tier 3: Depth Pages (Nice to Have)

| Page | Path | Purpose | Word Count Target |
|------|------|---------|-------------------|
| Careers | `/about/careers.html` | Job listings (empty/minimal) | 400-600 |
| Individual Protocol Pages | `/protocols/registry/gap-*.html` | Specific protocol details | 800-1500 each |
| Individual WG Pages | `/research/working-groups/*.html` | WG details | 600-1000 each |
| Annual Reports | `/research/annual-reports.html` | Report archive | 400-600 |
| Press Releases | `/news/press-releases/*.html` | Individual releases | 400-800 each |
| Training | `/resources/training.html` | Training materials | 600-1000 |
| Inquiry Form | `/contact/inquiry.html` | Contact form | 200-300 |

---

## Navigation Structure

### Primary Navigation
```
Home | About ▼ | Protocols ▼ | Research ▼ | Documentation ▼ | News | Contact
```

### About Dropdown
- About GAS
- History
- Leadership
- Member Organizations
- Careers

### Protocols Dropdown
- Protocol Registry
- Alignment Framework
- Safety Standards
- Compliance

### Research Dropdown
- Overview
- Publications
- Working Groups
- Annual Reports

### Documentation Dropdown
- Documentation Hub
- Technical Specifications
- Implementation Guides
- API Reference
- Glossary

### Footer Navigation
- About | Protocols | Research | Documentation | News | Contact
- Privacy Policy | Terms of Use | Accessibility Statement
- © 2039-2047 Global Agents System Consortium

---

## Internal Linking Requirements

Every page must link to at least 3 other internal pages. Key linking patterns:

1. **Breadcrumbs** on all pages below root level
2. **Related pages** section at bottom of content pages
3. **In-text links** to glossary terms, protocols, and documentation
4. **Cross-references** between research and protocols
5. **Call-to-action links** to downloads and resources

---

## URL Structure Rules

- All lowercase
- Hyphens for word separation
- No trailing slashes on files (except index.html directories)
- Descriptive, keyword-rich paths
- Maximum 3 levels deep from root

---

## Canonical URLs

Every page must specify canonical URL in `<head>`:
```html
<link rel="canonical" href="https://globalagentssystem.com/about/history.html">
```
