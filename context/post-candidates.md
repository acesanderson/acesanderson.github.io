# Post Candidates: Projects and Skills

Source: $BC (/Users/bianders/Brian_Code) and ~/.claude/skills
Last updated: 2026-03-04

These are candidates for "project announcement / developer story" style posts.
The git history of each project is a key resource for reconstructing the narrative arc.

---

## Projects ($BC)

### High interest

| Project | What it is |
|---|---|
| conduit-project | Unified LLM framework — single interface over OpenAI, Anthropic, Gemini, Ollama, Perplexity, with semantic caching + conversation persistence |
| siphon | Multi-modal ingestion pipeline — URLs, PDFs, audio -> structured LLM-ready context. Strategy pattern, PostgreSQL, async LLM enrichment |
| headwater | Personal LLM API server — semantic search, embeddings management, high-performance |
| haddock-project | Trino interface with semantic layer — natural language table discovery, schema documentation, result caching |
| tap-project | POSIX CLI for composing Obsidian notes into LLM context — fuzzy matching, vector similarity search |
| aquifer-project | Research automation — RSS, YouTube, SEC filings, AI-powered search agents |
| mentor-project | Multi-agent curriculum generation — 3 personas (L&D, curriculum structuring, course librarian), RAG |
| metaprompt-project | CLI tool: high-level description -> structured prompt via LLM |
| watergun-project | API server providing tools for Open WebUI — web search, scraping, doc retrieval |
| morgan-project | Purchase impact calculator — true cost via opportunity cost + retirement modeling (FIRE planning) |
| dbclients-project | Network-aware database connection library — auto-discovers network context, hands you the right client |

### Low interest / work-specific / unclear

clippy, corsair, gcp-project, kramer, menuhin, rubric, outlook-email, sandbox, dev, utils, work

---

## Skills (~/.claude/skills)

### High interest

| Skill | What it is |
|---|---|
| conduit (skill) | Multi-model runtime for Claude Code — routes to Perplexity, Gemini, Ollama, image gen |
| deslop | Two-pass LLM pipeline to strip AI-isms: Gemini judges, Opus revises only flagged items |
| batch-dispatch | Parallel, isolated skill execution using Claude Code's native sandboxing |
| yt-transcript | YouTube transcript fetcher — no auth, SQLite cache, all URL formats |
| skill-creator | Skill scaffolding guide — the meta-skill |
| refactor-worktree | Safe refactoring in isolated git worktrees |
| obsidian (skill) | Vault ingestion + vector retrieval via Claude Code |

### Lower interest / work-specific / utility

catalog-scraper, find-catalogues, licensing-assistant, li-golden-post-finder,
job-application, job-skills-map, sec-filings, blog, cc-coach, cc-planner,
claude-history, youtube-intel, brave-web-search, python_style, python-project-structure,
obsidian-vault

---

## Essays / Conceptual

Ideas in this category are not project announcements — they're observations or arguments
drawn from practice. Shorter form, more opinionated.

### Annotation ops / eval methodology cluster

| Title | Core argument |
|---|---|
| Field descriptions are annotation guidelines | Most rubrics name categories; field descriptions define behaviors. "Does this post lead with a product offer rather than a claim about the world?" vs. "is this promotional?" — that specificity is what takes IAA from 60% to 87%. You built this before you knew the term for it. |
| Vendor drift is a guidelines problem | When you swap annotators and kappa drops, teams blame the vendor. The real culprit is rubric ambiguity — the old vendor learned intent through accumulated feedback; the new one has only the written guidelines. Whatever the old vendor "just knew" is documentation debt. |
| You can't evaluate what you haven't annotated | Evals are downstream of ground truth. Ground truth requires annotation ops — the part everyone wants to automate first. LLM-as-judge doesn't replace the annotation layer, it inherits it. If your guidelines are vague, your automated eval is confidently vague. The human moves upstream, not out. |

### Claude Code workflow cluster

| Title | Core argument |
|---|---|
| Spec-Driven Development with Claude Code | Tips + prompt examples for the Superpowers spec-driven workflow: writing plans, entering plan mode, executing against specs with review checkpoints. Practical guide for getting Claude Code to build non-trivial things reliably without going off the rails. |

---

## Notes

- Git history is the primary raw material for developer-story posts — walk commits to reconstruct decisions and pivots
- conduit appears both as a project and a skill — they're related but distinct; could be one post or two
- siphon and headwater together form the personal LLM infrastructure stack — potentially a series
- Skills posts are more niche (Claude Code audience) but good for differentiation
