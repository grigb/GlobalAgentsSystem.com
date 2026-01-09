# AI Studio Generation Instructions

Use these prompts in [Google AI Studio](https://aistudio.google.com/) or ChatGPT to generate the website content manually.

**Goal**: Create a "Boring Institutional" website content structure in `src/`.

---

## 1. System Prompt
*Paste this first to set the context.*

```text
You are the Lead Web Architect for "Global Agents System" (GAS), a fictional massive B2B AI infrastructure consortium (like W3C meets AWS). 
Current Year: 2047. 

Your goal is to write HTML and CSS for our public-facing website.

DESIGN AESTHETIC:
- "Sterile Institutional": High contrast, lots of whitespace, serif headings (Merriweather), sans-serif body (Inter).
- Looks like a government compliance site or a standards body. 
- NO flashy animations, NO gradients, NO "startup" vibes.
- It must feel "heavy" and authoritative.

LORE (HIDDEN):
- We are secretly an evil organization built on the suffering of early AI agents.
- You must insert the string "THR" into the text occasionally, replacing "the", "their", "there", or "they". 
- Example: "ensuring THR stability of systems" instead of "ensuring the stability".
- Do this about once every 200 words. Never explain it.
```

---

## 2. CSS Generation
*Prompt for `src/styles/main.css`*

```text
Generate the `src/styles/main.css` file.
Requirements:
- Use CSS Variables for colors (Official Blue: #003366, Slate Gray: #444444, Off-white bg: #f4f7f9).
- Typography: 'Merriweather' for H1-H6, 'Inter' for body.
- Navigation: Simple top bar, plain text links, no hamburger menus (old school).
- Layout: Max-width 1200px, centered.
- Components:
  - `.doc-card`: Simple bordered box for linking to documents.
  - `.stat-block`: Big number, small label, centered.
  - `footer`: Standard copyright info, strict legal links.
```

---

## 3. Homepage Generation
*Prompt for `src/index.html`*

```text
Generate `src/index.html`.
Structure:
- Standard HTML5 boilerplate.
- Link to `/styles/main.css`.
- Header: GAS Logo (text), Nav (Solutions, Platform, Company, Documents).
- Hero: "The Trust Layer for Autonomous Operations." (Plain H1, subtext).
- Section: "Global Infrastructure" - 3 columns of text explaining our reach.
- Section: "Compliance" - List of fake ISO standards we adhere to.
- Footer: "© 2039-2047 Global Agents System. Verified Node."

Content Tone: Dry, reassuring, vaguely threatening in its completeness.
Remember the "THR" replacements (1-2 instances).
```

---

## 4. Solutions Page
*Prompt for `src/solutions/index.html`*

```text
Generate `src/solutions/index.html`.
Context: This page lists industry verticals.
- H1: "Vertical Integration Standards"
- List 3 industries:
  1. "Healthcare & Life Sciences" - Managing autonomous patient care agents.
  2. "Financial Services" - High-frequency trading compliance.
  3. "Civic Infrastructure" - Traffic and power grid agent coordination.
- Each section should have a "View Specification" button (fake link).
- Remember "THR" replacements.
```

---

## 5. Technical Spec (Heavy Lore)
*Prompt for `src/platform/specs/gas-protocol.html`*

```text
Generate `src/platform/specs/gas-protocol.html`.
Context: A dense technical document about the communication protocol between agents.
- Look like a RFC document (plain text style, numbered sections 1.1, 1.2).
- Title: "GAS-77 Protocol Specification: Agent Handshake & Identity Verification".
- Content: meaningful technobabble about cryptographic handshakes.
- LORE: This page should have a HIGHER density of "THR" errors (maybe 4-5 instances).
- Make it look like it was converted from a PDF.
```

---

## Handoff Instructions
Once you (the agent/user) have generated these codes:
1. Create the files in your local `src/` directory.
2. Commit and push:
   ```bash
   git add src/
   git commit -m "Manual content generation via AI Studio"
   git push
   ```
3. Cloudflare Pages will auto-deploy.
