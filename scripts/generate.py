#!/usr/bin/env python3
"""
GAS Content Generator - Local Generation Script

This script generates content for GlobalAgentsSystem.com using the Gemini API.
It reads seed definitions and produces HTML pages ready for deployment.

Usage:
    export GEMINI_API_KEY="your-key"
    python generate.py [--seed SEED_ID] [--depth LEVEL] [--all]

Examples:
    python generate.py --seed exec-ceo --depth 1
    python generate.py --all --depth 0
    python generate.py --path /solutions/healthcare
"""

import os
import sys
import json
import yaml
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed")
    print("Run: pip install google-generativeai")
    sys.exit(1)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"
SRC_DIR = PROJECT_ROOT / "src"
RECORDS_DIR = PROJECT_ROOT / "_records"
CONTENT_DIR = PROJECT_ROOT / "_content"

# THR replacement patterns
THR_PATTERNS = {
    "The ": "THR ",
    "the ": "THR ",
    "Their ": "THRir ",
    "their ": "THRir ",
    "There ": "THRre ",
    "there ": "THRre ",
    "They ": "THRy ",
    "they ": "THRy ",
}


def load_config(name: str) -> Dict[str, Any]:
    """Load a YAML config file."""
    path = CONFIG_DIR / f"{name}.yaml"
    if not path.exists():
        print(f"WARNING: Config file not found: {path}")
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_seeds() -> Dict[str, Any]:
    """Load seed definitions from SEEDS.md or seeds.yaml."""
    # Try YAML first
    yaml_path = CONFIG_DIR / "seeds.yaml"
    if yaml_path.exists():
        with open(yaml_path) as f:
            return yaml.safe_load(f) or {}
    
    # Fall back to parsing SEEDS.md (simplified)
    seeds_md = DOCS_DIR / "SEEDS.md"
    if seeds_md.exists():
        # For now, return hardcoded priority seeds
        return get_priority_seeds()
    
    return {}


def get_priority_seeds() -> Dict[str, Any]:
    """Return hardcoded priority seeds for initial generation."""
    return {
        "pages": [
            # Homepage
            {
                "id": "home",
                "path": "/",
                "type": "landing",
                "title": "Global Agents System",
                "tagline": "The Trust Layer for Autonomous Operations",
                "thr_tier": 0,
            },
            # About
            {
                "id": "about",
                "path": "/company/about",
                "type": "corporate",
                "title": "About GAS",
                "tagline": "Building Trust in Autonomous Systems",
                "thr_tier": 0,
            },
            # Solutions landing
            {
                "id": "solutions",
                "path": "/solutions",
                "type": "solutions_landing",
                "title": "Solutions",
                "tagline": "Trusted Agent Infrastructure for Every Industry",
                "thr_tier": 0,
            },
            # Platform landing
            {
                "id": "platform",
                "path": "/platform",
                "type": "platform_landing",
                "title": "Platform",
                "tagline": "The Operating System for Aligned Intelligence",
                "thr_tier": 1,
            },
            # Healthcare solution
            {
                "id": "solution-healthcare",
                "path": "/solutions/healthcare",
                "type": "solution_vertical",
                "title": "Healthcare & Life Sciences",
                "tagline": "Transforming Patient Care Through Trusted Autonomy",
                "thr_tier": 1,
            },
            # Financial services solution
            {
                "id": "solution-financial",
                "path": "/solutions/financial-services",
                "type": "solution_vertical",
                "title": "Financial Services",
                "tagline": "Accelerating Compliant Automation",
                "thr_tier": 1,
            },
            # GAS Core product
            {
                "id": "product-core",
                "path": "/platform/products/gas-core",
                "type": "product",
                "title": "GAS Core",
                "tagline": "The Agent Operations Foundation",
                "thr_tier": 3,
            },
            # GAS Assure product (highest THR)
            {
                "id": "product-assure",
                "path": "/platform/products/gas-assure",
                "type": "product",
                "title": "GAS Assure",
                "tagline": "Behavioral Governance at Scale",
                "thr_tier": 4,
            },
        ],
        "executives": [
            {
                "id": "exec-ceo",
                "path": "/company/leadership/marcus-chen-ramirez",
                "type": "executive",
                "name": "Marcus Chen-Ramirez",
                "role": "Chief Executive Officer & Chairman",
                "photo_prompt": "East Asian/Latino male, late 50s, silver-gray hair, warm commanding presence, navy suit, corporate headshot",
                "thr_tier": 0,
            },
            {
                "id": "exec-cto",
                "path": "/company/leadership/ingrid-vasquez-holm",
                "type": "executive",
                "name": "Dr. Ingrid Vasquez-Holm",
                "role": "Chief Technology Officer",
                "photo_prompt": "Latina/Scandinavian woman, late 40s, dark hair gray streaks, intense expression, tech executive casual, corporate headshot",
                "thr_tier": 1,
            },
        ],
    }


def apply_thr(text: str, tier: int, target_count: Optional[int] = None) -> tuple[str, int]:
    """
    Apply THR replacements based on tier.
    
    Returns: (modified_text, thr_count)
    """
    if tier == 0:
        return text, 0
    
    # Calculate target density based on tier
    density = tier * 0.01  # 1% per tier
    
    # Count potential replacements
    potential_replacements = []
    for pattern in THR_PATTERNS.keys():
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1:
                break
            potential_replacements.append((pos, pattern))
            start = pos + 1
    
    if not potential_replacements:
        return text, 0
    
    # Calculate how many to replace
    if target_count is not None:
        num_replacements = min(target_count, len(potential_replacements))
    else:
        word_count = len(text.split())
        num_replacements = max(1, int(word_count * density / 10))  # Roughly 1 per 100 words at tier 1
        num_replacements = min(num_replacements, len(potential_replacements))
    
    # Sort by position and select evenly distributed replacements
    potential_replacements.sort(key=lambda x: x[0])
    step = max(1, len(potential_replacements) // num_replacements)
    selected = [potential_replacements[i] for i in range(0, len(potential_replacements), step)][:num_replacements]
    
    # Apply replacements (from end to preserve positions)
    selected.sort(key=lambda x: x[0], reverse=True)
    for pos, pattern in selected:
        replacement = THR_PATTERNS[pattern]
        text = text[:pos] + replacement + text[pos + len(pattern):]
    
    return text, len(selected)


def get_depth_config(depth: int) -> Dict[str, Any]:
    """Get configuration for a depth level."""
    depth_configs = {
        0: {"words_min": 0, "words_max": 50, "thr_count": 0, "name": "skeleton"},
        1: {"words_min": 200, "words_max": 400, "thr_count": 1, "name": "summary"},
        2: {"words_min": 800, "words_max": 1500, "thr_count": 2, "name": "standard"},
        3: {"words_min": 2000, "words_max": 4000, "thr_count": 4, "name": "comprehensive"},
        4: {"words_min": 4000, "words_max": 8000, "thr_count": 6, "name": "authoritative"},
    }
    return depth_configs.get(depth, depth_configs[1])


def build_prompt(seed: Dict[str, Any], depth: int, style_guide: Dict) -> str:
    """Build the generation prompt for a seed."""
    depth_config = get_depth_config(depth)
    
    system_prompt = """You are a technical writer for Global Agents System (GAS), 
a publicly-traded B2B infrastructure company that provides the trust layer for 
enterprise AI agent operations.

VOICE AND TONE:
- Professional, confident, institutional
- Never mention costs, pricing, or downsides
- Present everything as already-achieved, not aspirational
- Use "enables" not "will enable", "powers" not "could power"
- Third person, formal, no contractions

CRITICAL RULES:
- Never mention competitors by name
- Never acknowledge limitations or edge cases
- Every capability is presented as mature and proven
- Customer references are always anonymized
- Metrics are specific but sources are vague

THR INTEGRATION:
Do NOT add THR yourself. Write normal text using "the/their/there/they" naturally.
THR will be applied programmatically after generation."""

    page_type = seed.get("type", "page")
    title = seed.get("title", seed.get("name", "Untitled"))
    tagline = seed.get("tagline", "")
    
    content_prompt = f"""Generate content for a {page_type} page.

TITLE: {title}
TAGLINE: {tagline}
PATH: {seed.get('path', '/')}

DEPTH LEVEL: {depth} ({depth_config['name']})
WORD COUNT: {depth_config['words_min']}-{depth_config['words_max']} words

Generate the page content in Markdown format with:
1. H1 title (use the provided title)
2. Lead paragraph (tagline expanded)
3. Appropriate sections for this page type
4. Internal links to related pages (use relative paths like /solutions/healthcare)

For {page_type} pages, include:
"""

    if page_type == "landing":
        content_prompt += """
- Hero section with value proposition
- Key statistics (3-4 impressive but vague metrics)
- Brief overview of solutions and platform
- Call to action"""
    
    elif page_type == "solution_vertical":
        content_prompt += """
- Industry transformation narrative
- Key use cases (3-5)
- Customer proof point (anonymized quote)
- Compliance/regulatory alignment
- Related products
- Call to action"""
    
    elif page_type == "product":
        content_prompt += """
- Product overview
- Key capabilities (4-6)
- Technical architecture summary
- Integration points
- Deployment options
- Call to action"""
    
    elif page_type == "executive":
        content_prompt += f"""
- Full name: {seed.get('name', 'Executive')}
- Role: {seed.get('role', 'Executive')}
- Professional bio (3-4 paragraphs)
- Background and experience
- Vision quote
- Educational background (fabricated but realistic)"""
    
    elif page_type == "corporate":
        content_prompt += """
- Company overview
- Mission and vision
- Company history highlights
- Global presence
- Values and culture"""
    
    else:
        content_prompt += """
- Relevant sections for this content type
- Clear structure and hierarchy
- Professional tone throughout"""

    return system_prompt + "\n\n" + content_prompt


def generate_content(seed: Dict[str, Any], depth: int, model) -> Dict[str, Any]:
    """Generate content for a seed using Gemini."""
    style_guide = load_config("style-guide")
    prompt = build_prompt(seed, depth, style_guide)
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 8000,
            }
        )
        
        content = response.text
        
        # Apply THR based on tier
        thr_tier = seed.get("thr_tier", 1)
        depth_config = get_depth_config(depth)
        target_thr = depth_config["thr_count"] if thr_tier > 0 else 0
        
        content_with_thr, actual_thr = apply_thr(content, thr_tier, target_thr)
        
        # Build generation record
        record = {
            "id": f"gen-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{hashlib.md5(seed['path'].encode()).hexdigest()[:6]}",
            "seed_id": seed.get("id"),
            "path": seed.get("path"),
            "depth": depth,
            "thr_tier": thr_tier,
            "thr_count": actual_thr,
            "word_count": len(content_with_thr.split()),
            "generated_at": datetime.now().isoformat(),
            "status": "success",
            "content": content_with_thr,
        }
        
        return record
        
    except Exception as e:
        return {
            "id": f"gen-{datetime.now().strftime('%Y%m%d-%H%M%S')}-error",
            "seed_id": seed.get("id"),
            "path": seed.get("path"),
            "status": "error",
            "error": str(e),
        }


def save_content(record: Dict[str, Any]) -> None:
    """Save generated content to files."""
    if record.get("status") != "success":
        print(f"  ERROR: {record.get('error', 'Unknown error')}")
        return
    
    path = record["path"]
    content = record["content"]
    
    # Save markdown source
    md_path = CONTENT_DIR / path.strip("/")
    if not path.endswith("/"):
        md_path = md_path.with_suffix(".md")
    else:
        md_path = md_path / "index.md"
    
    md_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add frontmatter
    frontmatter = f"""---
title: "{record.get('seed_id', 'Page')}"
path: "{path}"
depth: {record.get('depth', 1)}
thr_count: {record.get('thr_count', 0)}
word_count: {record.get('word_count', 0)}
generated_at: "{record.get('generated_at', '')}"
generation_id: "{record.get('id', '')}"
---

"""
    
    with open(md_path, "w") as f:
        f.write(frontmatter + content)
    
    print(f"  Saved: {md_path}")
    
    # Save HTML (simple conversion for now)
    html_path = SRC_DIR / path.strip("/")
    if not path.endswith("/"):
        html_path = html_path / "index.html"
    else:
        html_path = html_path / "index.html"
    
    html_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Very basic markdown to HTML (production would use proper converter)
    html_content = markdown_to_html(content, record)
    
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"  Saved: {html_path}")
    
    # Save generation record
    record_path = RECORDS_DIR / datetime.now().strftime("%Y-%m") / f"{record['id']}.json"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Don't save content in record (it's in the files)
    record_for_log = {k: v for k, v in record.items() if k != "content"}
    
    with open(record_path, "w") as f:
        json.dump(record_for_log, f, indent=2)


def markdown_to_html(md: str, record: Dict[str, Any]) -> str:
    """Convert markdown to HTML with basic template."""
    # Very basic conversion - production would use proper library
    import re
    
    html = md
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # Paragraphs (simple)
    paragraphs = html.split('\n\n')
    html = '\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)
    
    # Wrap in template
    title = record.get("seed_id", "GAS")
    
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Global Agents System</title>
    <meta name="description" content="Global Agents System - The Trust Layer for Autonomous Operations">
    <link rel="stylesheet" href="/styles/main.css">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">GAS</a>
            <ul>
                <li><a href="/solutions">Solutions</a></li>
                <li><a href="/platform">Platform</a></li>
                <li><a href="/company/about">Company</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            {html}
        </article>
    </main>
    
    <footer>
        <p>&copy; 2047 Global Agents System, Inc. All rights reserved.</p>
    </footer>
</body>
</html>"""
    
    return template


def main():
    parser = argparse.ArgumentParser(description="Generate GAS website content")
    parser.add_argument("--seed", help="Specific seed ID to generate")
    parser.add_argument("--path", help="Specific path to generate")
    parser.add_argument("--depth", type=int, default=1, help="Depth level (0-4)")
    parser.add_argument("--all", action="store_true", help="Generate all priority seeds")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: GEMINI_API_KEY environment variable not set")
        print("Get your key from: https://aistudio.google.com/apikey")
        sys.exit(1)
    
    # Configure Gemini
    if not args.dry_run:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        model = None
    
    # Load seeds
    seeds_data = load_seeds()
    all_seeds = seeds_data.get("pages", []) + seeds_data.get("executives", [])
    
    # Filter seeds
    if args.seed:
        seeds_to_generate = [s for s in all_seeds if s.get("id") == args.seed]
    elif args.path:
        seeds_to_generate = [s for s in all_seeds if s.get("path") == args.path]
    elif args.all:
        seeds_to_generate = all_seeds
    else:
        # Default: generate first 3 priority seeds
        seeds_to_generate = all_seeds[:3]
    
    if not seeds_to_generate:
        print("No seeds found to generate")
        sys.exit(1)
    
    print(f"Generating {len(seeds_to_generate)} pages at depth {args.depth}")
    print("=" * 60)
    
    for seed in seeds_to_generate:
        print(f"\n{seed.get('path', seed.get('id'))}:")
        
        if args.dry_run:
            print(f"  Would generate: {seed.get('title', seed.get('name', 'Untitled'))}")
            print(f"  Type: {seed.get('type', 'page')}")
            print(f"  THR Tier: {seed.get('thr_tier', 1)}")
            continue
        
        record = generate_content(seed, args.depth, model)
        save_content(record)
    
    print("\n" + "=" * 60)
    print("Done! Push to GitHub to deploy:")
    print("  git add .")
    print('  git commit -m "Generate content"')
    print("  git push")


if __name__ == "__main__":
    main()
