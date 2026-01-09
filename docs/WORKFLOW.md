# GAS Lore Workflow

How to add new secret projects, history, or detailed lore to the system.

## The 3-Step "Sync" Process

Since `behind-the-curtain` contains raw creative text and `SEEDS.md` contains structured data, the "sync" is performed by an **Agent** (me).

### Step 1: Ideate (The Basement)
Create or edit files in your external archive:
`~/work/GlobalAgentsSystem/behind-the-curtain/`

*   *Example*: Create `Project_X.md` with your rough notes, goals, and secret truths.
*   *Status*: **Raw, Private, Unstructured.**

### Step 2: Ingest (The System)
Ask the Agent to "Ingest" your new files.
> "I added Project X to the curtain folder. Sync it."

The Agent will:
1.  Read your new file.
2.  Start an `implementation_plan`.
3.  Add a structured entry to `docs/SEEDS.md` (defining ID, slug, tier).
4.  Update generation prompts in `docs/AI_STUDIO_PROMPTS.md`.

*   *Status*: **Structured, System-Aware.**

### Step 3: Manifest (The Facade)
The Website "manifests" the new reality.

*   **Manual**: You use the updated prompts in AI Studio to generate `src/` files.
*   **Automated (Future)**: The system auto-generates the skeleton page based on the new Seed.

---

## Quick Reference

| Location | Purpose | Who Edits? |
|os|---|---|
| `~/work/.../behind-the-curtain/` | The Truth (Raw) | **You** |
| `docs/SEEDS.md` | The Structure (Data) | **Agent** (on request) |
| `docs/lore/` | In-Universe Docs (Canon) | **Agent** (on request) |
| `src/` | Public Website | **Browser Agent** / Generators |
