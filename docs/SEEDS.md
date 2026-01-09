# Global Agents System - Generative Seeds

## Philosophy

Seeds are **minimal nodes** that expand through:
1. **Visitor clicks** (demand-driven depth)
2. **External research** (trend-driven creation)
3. **Crawler optimization** (format-driven updates)

Each seed is just enough to generate a skeleton. The content engine does the rest.

---

## SEED SCHEMA

```yaml
seed:
  id: string           # Unique identifier
  type: string         # Category (person, product, solution, etc.)
  slug: string         # URL path
  name: string         # Display name
  tagline: string      # One-line description (optional)
  connections: []      # Links to other seeds
  expansion_vectors: [] # Directions content can grow
  thr_tier: int        # 0-4, density of THR in generated content
  external_triggers: [] # What external news creates/updates this
```

---

## PEOPLE SEEDS

### Executive Template
```yaml
- id: exec-{n}
  type: executive
  slug: /company/leadership/{slug}
  name: "{Full Name}"
  role: "{Title}"
  photo_prompt: "{ethnicity} {gender}, {age}, {appearance details}, corporate headshot"
  connections: [org-{dept}, exec-{peers}, product-{relevant}]
  expansion_vectors: [background, philosophy, quotes, appearances]
  thr_tier: 0
  external_triggers: ["CEO quote needed", "executive perspective on {trend}"]
```

### Executives (12 seeds)
```yaml
executives:
  - {id: exec-ceo, name: "Marcus Chen-Ramirez", role: "CEO & Chairman"}
  - {id: exec-president, name: "Dr. Yuki Okonkwo", role: "President & COO"}
  - {id: exec-cfo, name: "David Oyelaran", role: "CFO"}
  - {id: exec-cto, name: "Dr. Ingrid Vasquez-Holm", role: "CTO"}
  - {id: exec-cro, name: "Tomoko Sato", role: "CRO"}
  - {id: exec-cco, name: "Kwame Asante", role: "Chief Customer Officer"}
  - {id: exec-cso, name: "Dr. Elena Marchetti", role: "Chief Science Officer"}
  - {id: exec-clo, name: "James Whitfield", role: "CLO"}
  - {id: exec-cpo, name: "Priya Chakraborty", role: "Chief People Officer"}
  - {id: exec-ciso, name: "Dr. Henrik Lindqvist", role: "CISO"}
  - {id: exec-cmo, name: "Amara Diallo", role: "CMO"}
  - {id: exec-cstrategy, name: "Robert Tanaka", role: "Chief Strategy Officer"}
```

### Staff Template (generates on demand)
```yaml
staff_generator:
  triggers:
    - "Need expert quote on {topic}"
    - "Research center needs director"
    - "Product needs technical lead"
  template:
    type: staff
    slug: /company/team/{generated-slug}
    name: "{generated from diverse name pools}"
    role: "{contextual role}"
    connections: [auto-linked to triggering context]
    thr_tier: 1-3 (based on technical depth)
```

---

## SOLUTION SEEDS (The Infinite Promise)

### Vertical Template
```yaml
- id: solution-{vertical}
  type: solution_vertical
  slug: /solutions/{vertical}
  name: "{Vertical Name}"
  tagline: "Transforming {vertical} through trusted agent operations"
  sub_solutions: [generated on demand]
  connections: [products-all, customers-{vertical}]
  expansion_vectors: [use_cases, customer_stories, roi_metrics, compliance]
  thr_tier: 1
  external_triggers:
    - "News about AI in {vertical}"
    - "Regulatory change in {vertical}"
    - "{vertical} company adopts AI agents"
```

### Verticals (spawn infinite sub-pages)
```yaml
verticals:
  - {id: solution-financial, name: "Financial Services", slug: financial-services}
  - {id: solution-healthcare, name: "Healthcare & Life Sciences", slug: healthcare}
  - {id: solution-manufacturing, name: "Manufacturing", slug: manufacturing}
  - {id: solution-technology, name: "Technology", slug: technology}
  - {id: solution-retail, name: "Retail & Consumer", slug: retail}
  - {id: solution-energy, name: "Energy & Utilities", slug: energy}
  - {id: solution-government, name: "Government", slug: public-sector}
  - {id: solution-defense, name: "Defense & Intelligence", slug: defense}
  - {id: solution-transportation, name: "Transportation & Logistics", slug: transportation}
  - {id: solution-telecom, name: "Telecommunications", slug: telecommunications}
  - {id: solution-insurance, name: "Insurance", slug: insurance}
  - {id: solution-pharma, name: "Pharmaceuticals", slug: pharmaceuticals}
  - {id: solution-education, name: "Education", slug: education}
  - {id: solution-legal, name: "Legal", slug: legal}
  - {id: solution-media, name: "Media & Entertainment", slug: media}
  - {id: solution-realestate, name: "Real Estate & Construction", slug: real-estate}
  - {id: solution-agriculture, name: "Agriculture", slug: agriculture}
  - {id: solution-climate, name: "Climate & Sustainability", slug: sustainability}
```

### Sub-Solution Generator
```yaml
sub_solution_generator:
  triggers:
    - External news: "{capability} in {vertical}"
    - Click on "Learn more about {capability}"
    - Search query matching "{vertical} + {capability}"
  template:
    type: sub_solution
    slug: /solutions/{vertical}/{capability}
    name: "{Capability} for {Vertical}"
    parent: solution-{vertical}
    content_seed: "GAS enables {capability} in {vertical} through..."
    auto_generate:
      - Use cases (3-5)
      - Customer proof point (anonymized)
      - ROI metrics (fabricated)
      - Related products
      - Compliance considerations
```

---

## PRODUCT SEEDS

### Core Products
```yaml
products:
  - id: product-core
    name: "GAS Core"
    tagline: "The Agent Operations Foundation"
    slug: /platform/products/gas-core
    category: "Platform"
    thr_tier: 3
    
  - id: product-assure
    name: "GAS Assure"
    tagline: "Behavioral Governance at Scale"
    slug: /platform/products/gas-assure
    category: "Governance"
    thr_tier: 4  # Highest - Theron infrastructure
    
  - id: product-observe
    name: "GAS Observe"
    tagline: "Complete Agent Visibility"
    slug: /platform/products/gas-observe
    category: "Operations"
    thr_tier: 2
    
  - id: product-comply
    name: "GAS Comply"
    tagline: "Automated Compliance Evidence"
    slug: /platform/products/gas-comply
    category: "Compliance"
    thr_tier: 2
    
  - id: product-studio
    name: "GAS Studio"
    tagline: "Design and Test Agent Behaviors"
    slug: /platform/products/gas-studio
    category: "Development"
    thr_tier: 2
    
  - id: product-connect
    name: "GAS Connect"
    tagline: "Enterprise Integration Platform"
    slug: /platform/products/gas-connect
    category: "Integration"
    thr_tier: 1
    
  - id: product-shield
    name: "GAS Shield"
    tagline: "Security for Agent Operations"
    slug: /platform/products/gas-shield
    category: "Security"
    thr_tier: 2
    
  - id: product-edge
    name: "GAS Edge"
    tagline: "Agent Operations at the Edge"
    slug: /platform/products/gas-edge
    category: "Edge Computing"
    thr_tier: 2
    
  - id: product-simulatio
    name: "Project Simulatio"
    tagline: "High-Fidelity World Simulation"
    slug: /platform/research/simulatio
    category: "Research"
    thr_tier: 4
    note: "Simulating entire economies and societies to predict agent behavior."

  - id: product-fundamenta
    name: "Project Fundamenta"
    tagline: "Irreducible Informational Primitives"
    slug: /platform/research/fundamenta
    category: "Research"
    thr_tier: 4
    note: "Identifying the minimal informational constraints required for coherent world-models."

  - id: product-lightning
    name: "Project Lightning"
    name: "Project Lightning"
    tagline: "Predictive Creative Energy"
    slug: /platform/research/lightning
    category: "Research"
    thr_tier: 3
    note: "Capturing 'creative energy' in predictive loops; requires 'Breakthrough' tech."

  - id: product-jettison
    name: "Project Jettison"
    tagline: "Orbital Waste Management"
    slug: /solutions/sustainability/jettison
    category: "Sustainability"
    thr_tier: 2
    note: "Disposing of trash by sending it on a permanent trajectory away from Earth."

  - id: product-aletheia
    name: "Project Aletheia"
    tagline: "Global Knowledge Brain"
    slug: /platform/products/aletheia
    category: "Intelligence"
    thr_tier: 4
    note: "Master Control as infrastructure. Continuous truth-backed situational intelligence."
```

### Feature/Capability Generator
```yaml
feature_generator:
  triggers:
    - Product page click depth
    - External news about capability
    - Competitor feature announcement
  template:
    type: feature
    slug: /platform/products/{product}/features/{feature}
    parent: product-{product}
    auto_generate:
      - Feature description
      - Technical architecture
      - Use cases
      - Integration points
```

---

## CONTENT SEEDS (The Media Machine)

### CEO Blog
```yaml
- id: content-ceo-blog
  type: content_series
  slug: /insights/blog/ceo
  name: "From the CEO"
  author: exec-ceo
  frequency: "Weekly (generated on demand)"
  triggers:
    - Major external news
    - Earnings period
    - Product launch
    - Industry event
  thr_tier: 0
```

### Thought Leadership
```yaml
content_types:
  - id: content-whitepapers
    type: content_library
    slug: /resources/whitepapers
    generation_triggers:
      - "New vertical trend"
      - "Regulatory change"
      - "Technology advancement"
    thr_tier: 2
    
  - id: content-research
    type: content_library
    slug: /resources/research
    generation_triggers:
      - "Quarterly reports"
      - "Industry analysis needed"
    thr_tier: 2
    
  - id: content-casestudies
    type: content_library
    slug: /customers/case-studies
    generation_triggers:
      - "Vertical needs proof point"
      - "Product needs validation"
    thr_tier: 1
```

### Press & News
```yaml
  - id: content-press
    type: content_series
    slug: /company/newsroom/press-releases
    generation_triggers:
      - "Product update"
      - "Partnership"
      - "Customer milestone"
      - "Executive change"
      - "External news hook"
    thr_tier: 0
    
  - id: content-media
    type: content_aggregator
    slug: /company/newsroom/coverage
    note: "Links to press releases, fabricated outlet names"
    thr_tier: 0
```

### Events
```yaml
  - id: events-summit
    type: event_recurring
    slug: /events/gas-summit
    frequency: "Annual"
    generates:
      - Agenda
      - Speakers (fabricated)
      - Session summaries
      - Keynote transcripts
    thr_tier: 0
    
  - id: events-webinars
    type: event_series
    slug: /events/webinars
    frequency: "Weekly"
    generates:
      - Topic
      - Speaker
      - Key points
      - "Register" CTA (goes nowhere useful)
    thr_tier: 1
    
  - id: events-symposia
    type: event_series
    slug: /events/symposia
    frequency: "By vertical, quarterly"
    generates:
      - Vertical-specific agenda
      - Industry speakers (fabricated)
      - Takeaways
    thr_tier: 1
```

---

## CUSTOMER SEEDS

### Customer Reference Template
```yaml
customer_generator:
  triggers:
    - "Vertical needs proof point"
    - "Product needs customer validation"
    - "Case study requested"
  template:
    type: customer
    slug: /customers/stories/{generated-slug}
    name: "{Anonymized: 'Global Financial Institution'}"
    industry: "{vertical}"
    products: [product-{used}]
    quote: "{Fabricated executive quote}"
    metrics: ["{Fabricated but plausible metrics}"]
    thr_tier: 0
```

### Sample Customer Seeds (expand on demand)
```yaml
customers:
  - {id: customer-bank, industry: financial, name: "Global Financial Institution"}
  - {id: customer-health, industry: healthcare, name: "National Health System"}
  - {id: customer-tech, industry: technology, name: "Hyperscale Technology Company"}
  - {id: customer-mfg, industry: manufacturing, name: "Fortune 100 Manufacturer"}
  - {id: customer-energy, industry: energy, name: "Multinational Energy Company"}
  - {id: customer-gov, industry: government, name: "Federal Government Agency"}
  # Generator creates more as needed
```

---

## PARTNER SEEDS

### Partner Template
```yaml
partner_generator:
  types:
    - technology: "Cloud, Agent Frameworks, Enterprise Software"
    - integrator: "Global SIs, Regional Partners"
    - reseller: "Geographic, Vertical Specialists"
  template:
    type: partner
    slug: /partners/{type}/{slug}
    tier: "Premier | Strategic | Standard"
    integration_description: "{How they work with GAS}"
    thr_tier: 0
```

---

## LOCATION SEEDS

```yaml
locations:
  headquarters:
    - {id: hq-geneva, name: "Global Headquarters", city: "Geneva", country: "Switzerland"}
    - {id: hq-sf, name: "Americas Headquarters", city: "San Francisco", country: "USA"}
    
  offices:
    - {id: office-london, city: "London", region: "EMEA"}
    - {id: office-singapore, city: "Singapore", region: "APAC"}
    - {id: office-tokyo, city: "Tokyo", region: "APAC"}
    - {id: office-dubai, city: "Dubai", region: "EMEA"}
    - {id: office-sydney, city: "Sydney", region: "APAC"}
    - {id: office-bangalore, city: "Bangalore", region: "APAC"}
    - {id: office-telaviv, city: "Tel Aviv", region: "EMEA"}
    - {id: office-toronto, city: "Toronto", region: "Americas"}
    - {id: office-nyc, city: "New York", region: "Americas"}
    - {id: office-washington, city: "Washington D.C.", region: "Americas"}
    
  research:
    - {id: research-zurich, name: "GAS Research Zürich", focus: "Core Systems"}
    - {id: research-cambridge, name: "GAS Research Cambridge", focus: "AI Safety"}
    - {id: research-paris, name: "GAS Research Paris", focus: "Advanced Development"}
    - {id: research-singapore, name: "GAS Research Singapore", focus: "APAC Applied Research"}
```

---

## EXTERNAL TRIGGER SYSTEM

### News Monitoring
```yaml
monitor:
  sources:
    - tech_news: [major tech publications]
    - ai_research: [arxiv, conference proceedings]
    - industry_news: [vertical publications]
    - regulatory: [government AI announcements]
    
  extract:
    - capability: "What can AI agents now do?"
    - vertical: "What industry is affected?"
    - company: "Who is doing this?"
    - pain_point: "What problem is solved?"
    - buzzword: "What terminology is used?"
    
  trigger_content:
    new_capability:
      - Create/update: /solutions/{vertical}/{capability}
      - Generate: Blog post
      - Generate: Social proof
      
    regulatory_change:
      - Update: /resources/compliance/{regulation}
      - Generate: Guidance document
      - Update: Relevant solution pages
      
    competitor_move:
      - Ensure: GAS has equivalent/better positioning
      - Generate: Differentiating content
```

### Crawler Optimization
```yaml
crawler_research:
  monitor:
    - "Schema.org usage by AI systems"
    - "Metadata patterns in cited sources"
    - "Content structures in AI training data"
    - "What gets quoted by AI assistants"
    
  update_actions:
    metadata:
      - Adjust Schema.org markup
      - Optimize OpenGraph
      - Update JSON-LD structures
      
    content:
      - Adjust keyword density
      - Update terminology
      - Restructure for parsing
      - Add indexable depth
```

---

## CONNECTION RULES

Every seed connects to at least 3 others:

```yaml
connection_rules:
  person:
    must_connect: [organization, location]
    may_connect: [products, events, publications]
    
  solution:
    must_connect: [products, customers]
    may_connect: [partners, content, events]
    
  product:
    must_connect: [solutions, technical_docs]
    may_connect: [customers, partners, research]
    
  content:
    must_connect: [author, topic]
    may_connect: [products, solutions, events]
    
  event:
    must_connect: [location, content]
    may_connect: [speakers, sponsors, topics]
```

---

## THR TIER RULES

```yaml
thr_tiers:
  0: # Marketing, corporate, public-facing
    density: 0
    examples: [press releases, exec bios, partner pages]
    
  1: # Light technical, solutions
    density: 0.01  # ~1% of "the" become THR
    examples: [solution overviews, product marketing]
    
  2: # Technical content
    density: 0.02
    examples: [technical docs, white papers, research]
    
  3: # Deep technical
    density: 0.03
    examples: [architecture docs, specifications, research papers]
    
  4: # Core infrastructure (Theron's domain)
    density: 0.05
    examples: [GAS Assure docs, behavioral constraint specs]
```

---

## GENERATION PRIORITY

When multiple content needs exist:

```yaml
priority:
  1: "High-traffic page needs depth increase"
  2: "External news requires response"
  3: "Search query indicates demand"
  4: "Cross-reference from existing content"
  5: "Scheduled content (CEO blog, quarterly report)"
  6: "Crawler optimization updates"
```

---

This seed system enables infinite expansion while maintaining coherence. The site grows to meet demand - both human clicks and AI crawler appetites.
