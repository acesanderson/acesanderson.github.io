# Blog Project
Last updated: 2026-03-02

## Identity
**Name:** acesanderson.dev (blog title TBD — "Whorl" is a strong candidate)
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
**URL:** https://acesanderson.dev

## Tech Stack
- Static site generator: Jekyll (v3.10.0 via github-pages gem)
- Hosting: GitHub Pages
- Domain: acesanderson.dev (registered at Porkbun)
- Theme: pages-themes/minimal@v0.2.0 (via remote_theme)
- Build: GitHub Actions (pages.yml)
- Drafting: Obsidian vault ($MORPHY = /Users/bianders/morphy)
- Publishing: git push to main → GitHub Actions → live

## Content Signal (from Code Learnings.md)
Posts will draw from: LLM API work, embeddings + vector DBs, RAG, agents, prompt
engineering, framework building, home lab setups, eval methodologies, Python patterns,
debugging war stories. Specific, dated, cumulative.

## Project Structure
```
~/blog/                          # repo root (acesanderson/acesanderson.github.io)
  _posts/                        # published posts — YYYY-MM-DD-title.md
  _config.yml                    # Jekyll config, theme, excludes
  Gemfile                        # github-pages gem
  index.md                       # homepage with post listing
  CNAME                          # acesanderson.dev
  .gitignore                     # Python + Jekyll build artifacts
  .github/workflows/pages.yml    # GitHub Actions build + deploy
  context/                       # reference docs (excluded from Jekyll build)
  tasks/                         # Manager task files (excluded from Jekyll build)
  docs/                          # saved external docs
  src/ tests/ pyproject.toml     # Python scaffolding — kept, excluded from Jekyll
```

## Open Questions
- Blog title / name? ("Whorl" deferred — identity to emerge from content)
- Post format conventions: long-form deep dives, short TILs, or both?
- Obsidian → _posts/ publishing workflow (manual for now, CLI automation later)
