# Beats: llm-stack-2026 (pattern post, 800-1500w target)

## Opening — Token shock, not price hikes
- Agentic LLMs burn tokens at a rate nobody budgeted for.
- 2025: "token maxxing" culture — some firms literally incentivized employees to run
  up usage as an adoption metric.
- 2026: the bill comes due. Belt-tightening, industry-wide.
- Proof point 1: Microsoft — Jan 2026 expanded internal Claude Code use across major
  eng teams → May/June 2026 canceled most Claude Code licenses (Experiences +
  Devices), moved engineers to GitHub Copilot CLI by June 30. Framed around cost, not
  quality; Claude still available via Foundry/M365 Copilot.
- Proof point 2: Uber — CTO says Uber blew its entire 2026 AI coding budget by April.
  Four months in.
- Proof point 3: Alex Karp (Palantir CEO), CNBC, June–July 2026 — "I am paying for
  tokens that create no value." "The product doesn't actually work and it's very
  expensive." Coins "tokenmax": labs push token consumption itself as a fake
  productivity signal.
- Turn: this is the environment hyperscalers are reacting to. Since raw token
  economics can't carry margin the way it used to, they're pivoting to
  ENVIRONMENT-level lock-in — harness (Claude Code), integrations (Workspace,
  Office). Bundling recovers what per-token sales can't.
- Stakes for the reader: if you're AI-first in your workflow, this should worry you.

## Turn — Harness > model spend (the counter-thesis)
- Meanwhile: open weights are closing the capability gap fast. New quantizations put
  huge-parameter models on consumer silicon.
- The bigger lever right now isn't a better model — it's a better harness. (2026
  consensus line to cite/paraphrase: "frontier upgrades set the floor; harness and
  workflow design set the ceiling.")
- Once you have a solid harness (structured output, test loops, tool calling), the
  model underneath becomes swappable — a cost/performance decision, not a
  capabilities cliff.
- This is the opening for the real argument: if the harness is the differentiator,
  and the harness is what hyperscalers are trying to lock you into — then owning your
  harness is how you fight back.

## Turn — The centralization principle
- What "owning your harness" means concretely: skills, prompts, MCPs, knowledge-base
  management — kept model/harness-agnostic.
- The "LLM Wiki" pattern: your environment isn't OpenCode's, or Claude's, or Hermes' —
  it's yours, and any of them can read it.
- Payoff promise for this section: pick up shop, move to a different model or harness,
  overnight. No re-platforming tax.

## Body — The stack tour (three layers, each with a one-line "why this" note)

### Layer 1: traditional web-UI chats
- Open WebUI (gemma4 local) — short, generalist questions. Why: free, private, fast
  enough that it's not worth spending a cloud call.
- Perplexity — grounded research. Why: citations matter more than model cleverness
  here.
- Gemini — long, in-depth chats. Why: context window headroom.

### Layer 2: agentic harnesses
- Hermes — personal knowledge base + personal tasks, xiaomi mimo-v25. Migrated from
  OpenClaw. Reachable from phone via Matrix. Why: cheap 1M-context model + always-on
  access beats a "better" model I can only reach from a laptop.
- OpenCode — mimo-v25 (OpenRouter) for complex tasks, ornith-35b-q8 (local) for
  implementation. Why: split by task complexity, not by loyalty to one model.
- GitHub Copilot CLI — work, enterprise subscription. Why: this one's not a choice,
  it's the job's harness — proof that even "locked in" contexts benefit from the same
  skills/prompts portability principle.
- Pi coder — unassisted agentic coding in a microvm, ornith-35b-q8 local. Why:
  isolation + no cloud dependency for unattended runs.

### Layer 3: the skills layer (what makes layers 1-2 swappable)
- GNU Stow — symlink centralized skills into whichever agent needs them. This is the
  actual mechanism of portability, not just the principle.
- blackglass — RAG server for Obsidian vault; tight API for agents to read/edit vault.
- conduit — LLM tool belt: query Perplexity/Deep Research/Anthropic/OpenAI from any
  agent; also an embeddings/reranker server. Common usage: "send several Perplexity
  queries to research X."
- web-search — richer replacement for "fetch": multiple search engines, Firecrawl,
  proxies.
- youtube — YouTube Data API + transcript API for video/channel analysis.
- tmux — display artifacts in panes, spawn agents in new panes, remote exec over SSH.
  Watching for cmux/herdr to mature and possibly replace this.
- sdd — trimmed-down Superpowers: opinionated project structure, job queue, Gitea
  issues workflow.

## Closing — The payoff
- You don't need to become an AI engineer to cut hyperscaler dependence.
- Start with the cheapest, most concrete move: own your skills. Centralize them. Keep
  them portable.
- The test: can you pick up and move to the next model or harness by lunchtime? If
  yes, you're insulated from whatever the hyperscalers do next — price cuts, price
  hikes, walled gardens, or the next Claude-Code-style bundling push.

---

## Notes for v0 writing pass
- Keep the Microsoft/Uber/Karp proof points concrete and dated — this is the load-bearing
  evidence for the whole opening; don't soften into vague "companies are worried."
- The pivot from "token shock" → "harness lock-in" → "own your harness" is the spine.
  Every layer of the stack tour should implicitly answer "why not the locked-in
  default?"
- Avoid making the stack tour a flat list — the one-line "why this" per item is doing
  the work of keeping it argument, not inventory.
