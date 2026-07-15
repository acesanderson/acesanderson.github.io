# Post Guideline: llm-stack-2026
Date: 2026-07-15

## Topic
A tour of my current LLM stack (cloud + local models, agentic harnesses, centralized skills)
as a concrete case study in avoiding hyperscaler lock-in.

## Angle / take
Power to the people: the token apocalypse plus hyperscaler walled-gardening make
vendor lock-in a real risk for anyone AI-first in their workflow — but you don't need
to be an AI engineer to route around it. Own your environment (skills, prompts, MCPs),
not just your model choice, and you can pick up and move to any harness or model
overnight.

## Narrative arc
- **Opening beat:** The token apocalypse, reframed — not price hikes, but sticker
  shock from actual agentic consumption. Agentic LLMs burn tokens at a rate nobody
  budgeted for; companies that spent 2025 "token maxxing" (some literally
  incentivizing employees to rack up usage as an adoption metric) are now hitting
  belt-tightening. Concrete proof points: Microsoft canceled internal Claude Code
  licenses (Jan 2026 expansion → May/June 2026 retrenchment to GitHub Copilot CLI),
  Uber blew its entire 2026 AI coding budget by April, and Alex Karp is out there
  publicly calling frontier labs' token economics a shell game — "I am paying for
  tokens that create no value," labs pushing customers to "tokenmax" as a fake
  productivity signal. The belt-tightening is real, industry-wide, and happening now.
  This is the environment hyperscalers are responding to by pivoting toward
  ENVIRONMENT-level lock-in — harness (Claude Code), integrations (Workspace,
  Office) — since bundling recovers margin that raw token sales increasingly can't.
- **Body moves:**
  1. The counter-thesis: harness > model spend. Open weights are closing the gap fast;
     new quantizations put huge models on consumer silicon. Gains from changing your
     harness now often beat gains from paying for a better model.
  2. The centralization principle: skills, prompts, MCPs, knowledge-base management —
     kept model/harness-agnostic (the "LLM Wiki" pattern). This is what makes you
     portable.
  3. The stack tour, three layers:
     - Traditional web-UI chats (Open WebUI/gemma4, Perplexity, Gemini)
     - Agentic harnesses (Hermes+mimo-v25 via Matrix, OpenCode+mimo-v25/ornith-35b,
       GitHub Copilot CLI for work, Pi coder in a microvm)
     - The skills layer that makes all of the above swappable (GNU Stow symlinking;
       blackglass, conduit, web-search, youtube, tmux, sdd)
- **Closing beat:** You don't need to become an AI engineer to cut hyperscaler
  dependence. Start by owning your skills — centralize them, keep them portable — so
  picking up and moving to the next model/harness is trivial.

## Key points (ordered by appearance in the post)
1. Token shock, not token hikes: agentic LLMs burn tokens fast; 2025's "token maxxing"
   culture (some firms literally incentivized employee token usage) meets 2026
   belt-tightening. Proof: Microsoft cancels internal Claude Code licenses (Jan 2026
   expansion → May/June retrenchment to Copilot CLI), Uber blows its 2026 AI coding
   budget by April
2. Karp's public "no ROI" critique: "tokens that create no value," labs pushing
   "tokenmax" as a fake productivity signal — enterprises correcting for it
3. Counter-trend: harness improvements now often beat raw model spend; open weights +
   new quantizations closing the gap, running huge models on consumer silicon
4. Centralization principle: skills/prompts/MCPs kept portable across OpenCode, Claude,
   Hermes, Pi coder — the "LLM Wiki" pattern fighting lock-in
5. Cloud model choices: OpenRouter cheap models, xiaomi mimo-v25 (1M context, cheap)
6. Local model choices: gemma4 (general), ornith (coding), qwen w/ CPU offload (unattended/cron)
7. Web-UI layer: Open WebUI, Perplexity, Gemini — when/why each
8. Agentic layer: Hermes (personal KB/tasks, Matrix phone access, migrated from OpenClaw),
   OpenCode (mimo-v25 cloud + ornith-35b local), GitHub Copilot CLI (work), Pi coder (microvm,
   unassisted)
9. Skills layer: GNU Stow symlink pattern; blackglass, conduit, web-search, youtube, tmux, sdd
10. Payoff: own your skills, centralize them, stay portable — the practical, non-engineer
    version of lock-in resistance

## Post type
[x] Pattern post (800-1500w)

## Source artifacts

### Vault notes
- Code Learnings.md — grep for: OpenClaw, Hermes, mimo, ornith, blackglass, conduit,
  Pi coder, OpenCode, GNU Stow, matrix

### Code
- ~/.claude/skills/ (or equivalent skills repo root) — blackglass, conduit, web-search,
  youtube, tmux, sdd skill definitions
- Any config for OpenCode / Hermes / Pi coder model routing, if present in a repo

### Claude history search terms
- "OpenClaw to Hermes", "mimo-v25", "ornith", "GNU Stow skills", "Pi coder microvm",
  "blackglass RAG obsidian", "conduit perplexity"

### External references
- Anthropic/OpenAI inference cost/unprofitability reporting (2026)
- Chinese open-weight model competitive landscape (2026) — for the "fierce competition" beat
- Agent Skills standard / MCP standardization context (already researched for Claude
  Patterns series — context/post-candidates.md has ecosystem notes reusable here)

## Voice notes
Pattern-post register: inventory/case-study tone, but the opening/closing frame it as
argument, not just a list. Avoid turning the stack tour into a flat feature list —
each layer should carry a one-line "why this, not the obvious alternative" note.
