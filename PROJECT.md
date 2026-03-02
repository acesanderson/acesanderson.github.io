# Blog Project
Last updated: 2026-03-02

## Identity
**Name:** [TBD — needs a title]
**Tagline:** [TBD]
**Topic/Focus:** Personal technical blog — AI engineering, home lab, LLMs, AI evals,
software engineering, the tech industry, online learning, online journalism
**Audience:** Technical practitioners + potential hirers (dual audience: peers who want
the specifics, and hirers who want signal about how Brian thinks and builds)
**Voice/Tone:** Practitioner learning in public. Specific and honest, not academic or
pundit-y. Personal voice with real technical depth. "Here's what I found, here's what
broke, here's what I learned."
**Goals:**
1. Share technical learnings with peers
2. Consolidate and deepen own understanding (writing as learning)
3. Serve as a durable technical artifact for hirers
**URL:** [TBD — needs GitHub repo, domain decision]

## Tech Stack
- Static site generator: Jekyll
- Hosting: GitHub Pages
- Domain: [TBD — github.io subdomain vs custom domain]
- Drafting: Obsidian vault ($MORPHY = /Users/bianders/morphy)
- Publishing: GitHub push → GitHub Actions

## Content Signal (from Code Learnings.md)
Posts will draw from: LLM API work, embeddings + vector DBs, RAG, agents, prompt
engineering, framework building, home lab setups, eval methodologies, Python patterns,
debugging war stories. Specific, dated, cumulative.

## Project Structure
- `~/blog/` — project root (no Jekyll structure yet)
  - `docs/github-pages.md` — local copy of GitHub Pages/Jekyll reference docs
  - Python scaffolding present (pyproject.toml, src/, tests/, uv.lock) — vestigial,
    to be removed or repurposed
  - `tasks/` — Manager-written task files for Assistant sessions
  - `context/` — read-only reference material

## Open Questions
- Blog name / title?
- Custom domain, or github.io subdomain to start?
- GitHub repo name (must be `<username>.github.io` for user site)?
- Jekyll theme?
- Post format: long-form deep dives, short TILs, or both?
- What to do with the Python scaffolding?
