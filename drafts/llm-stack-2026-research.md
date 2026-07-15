# Research: llm-stack-2026

## Primary sources (Brian's own work)
[TBD — vault grep / code / claude-history not yet run; see guideline source artifacts]

## External context

### Harness > model spend framing (June/July 2026)
Query: Perplexity sonar-pro, 2026-07-15

Synthesis line worth quoting/adapting:
> "In 2026, AI coding performance is primarily a function of the *system* (agentic
> tools, MCP skills, verification harnesses) rather than the *model*. Frontier
> upgrades set the floor; harness and workflow design set the ceiling."

Supporting voices/sources:
- Richard Bownes, "LLMs in 2026: Trends, Use Cases & Business Impact" — describes
  stack: "naked LLM calls → workflows → tool calling → MCP servers → agent skills";
  "a slowdown in headline performance gains alongside an improvement in consistency
  and reliability." (youtube, 2026-01-28)
- Builder.io, "Best LLMs for coding in 2026" — open-weight models (GLM-4.7, Minimax
  M2.1) competitive with frontier *when* harness has "enforced diff output, automated
  test runs, and a repeatable evaluation harness"; without that structure they
  underperform. Claude Opus 4.7 SWE-bench Pro 53%→64%. (2026-01-28)
- NextFutures, "Tech Trends 2026 update" — process improvement "will likely matter
  more in the short term than model performance against benchmarks." (2026-02-18)
- Nate Berkopec, "Thoughts on LLMs in 2026" — LLMs useful "when work is verifiable,
  looped through agents, and pointed at software-making software."
- METR research cited: AI tools led to a 20% *slowdown* for experienced devs when
  not embedded in strong workflows/verification harnesses — cautionary counterpoint,
  useful as a "harness matters even more than you think" beat.
- Buzz Software, "LLM-Powered Software Development in 2026" — decision is "which
  tool integrates most naturally into your existing workflow," not which model is
  best in the abstract.

Full citations: daily.dev LLM tag (2026-04), buzzsoftware.ro, builder.io, Future AGI
prompt-engineering-2026, codersera open-source-LLM-landscape-2026, Addy Osmani LinkedIn
post "Optimizing LLM Coding Workflow for 2026."

### Inference economics / token pricing 2026 — IMPORTANT: complicates the "token
### apocalypse = price hikes" framing
Query: Perplexity sonar-pro, 2026-07-15

**Actual finding: prices are falling sharply in 2026, not rising.** This needs to
reshape the opening beat — see flag to Brian below.

- **Anthropic**: reported Q2 2026 revenue $10.9B (up from $4.8B Q1), first-ever
  operating profit ~$559M in Q2 2026. Inference gross margin rose from ~38% (year
  earlier) to over 70% by mid-2026; compute cost per revenue dollar fell from $0.71
  to $0.56. Claude Opus pricing cut from $15/$75 (per M tokens in/out) to $5/$25 at
  Opus 4.6 (Feb 2026) — a 67% cut. **Anthropic is not clearly loss-leading at the
  company level by mid-2026.**
  Sources: zenaicorp.com (2026-05-21), research.mental-momentum.ai (2026-06-12), dev.to (2026-05-27)

- **OpenAI**: inference costs ~$8.4B in 2025, projected $14.1B in 2026; may spend
  ~$2.20–$2.25 to fulfill every $1 of revenue. Thin-to-negative margin after full
  opex (incl. Microsoft rev share) even if raw compute is sometimes profitable.
  Reported frontier pricing collapse: o1 ($15/$60 per M tokens) → o3 ($2/$8) → o4-mini
  ($1.10/$4.40) — 87–93% reductions vs. 2024 baseline.
  Sources: aiautomationglobal.com (2026-03-16), exponentialview.co (2026-02-13),
  investing.com (2026-05-22), turingpost.com (2026-05-07)

- **Real trend: token price deflation + packaging inflation.** Headline per-token
  prices are falling due to price war / Chinese open-weight competition pushing the
  floor down. But vendors recover margin via **bundling and workflow lock-in**:
  Anthropic restructured enterprise contracts (late 2025/early 2026) from fixed-seat
  bundles to low base fee + usage at API rates — can raise effective customer bill
  even as headline token price falls. Claude Code reportedly ~$6/dev/day average
  spend, 90% of users under $12/day — a usage-based *product* bundle, not a token
  meter.
  Source: blog.herlein.com (2026-05-19), readsignal.io (2026-06-27)

- **Chinese open-weight competition** (DeepSeek, Qwen, GLM, Minimax, etc.) is pushing
  the global price floor down — sources light on hard per-vendor numbers, but the
  competitive effect is clear: frontier-quality capability increasingly available at
  much lower effective cost, forcing Western labs to compete on distribution,
  integration, reliability, compliance, packaging — not raw token price.

- **Differentiation strategy**: bundling into developer tooling (Claude Code),
  office suites (Workspace/Office), cloud ecosystems — sell productivity suites and
  workflow capture, not bare API access. This is the "walled garden" mechanism, but
  it operates through integration lock-in, not price gouging.

Full citations available in query output; key ones: zenaicorp.com, mental-momentum.ai
(x2), dev.to, aiautomationglobal.com, exponentialview.co, investing.com, herlein.com,
readsignal.io, linkedin.com/peterchrbennett, turingpost.com, oplexa.com.

### Enterprise belt-tightening: Microsoft/Claude Code, Karp/Palantir, token-maxxing pullback
Query: Perplexity sonar-pro, 2026-07-15 (two queries)

**Microsoft — Claude Code cancellation (the clearest example of promote-then-retrench):**
- Jan 2026: Microsoft *expanded* internal Claude Code use across major engineering
  teams, encouraged even nontechnical staff to try it. (technewsday.com, 2026-01-23)
- May–June 2026: Microsoft canceled most internal Claude Code licenses in its
  Experiences + Devices division, told engineers to move to GitHub Copilot CLI by
  June 30, 2026. Framed around token-based pricing/cost pressure, not quality.
  Claude models still available via Microsoft Foundry / M365 Copilot — this was a
  cost/ownership move, not full abandonment.
  Sources: spacedaily.com, Forbes (2026-06-01), The Verge/Tom Warren (referenced by
  multiple outlets), epcgroup.net (2026-05-15), dev.to (2026-05-24)
- Same reporting: **Uber's CTO said Uber exhausted its entire 2026 AI coding tools
  budget by April** — four months in. (via The Information, relayed 2026-06-02)

**Alex Karp (Palantir CEO) — direct "no ROI" quotes, 2025–2026:**
- CNBC, ~July 1 2026: *"I am paying for tokens that create no value."* (paraphrasing
  enterprise customers) — *"these models have been completely, irresponsibly,
  oversold."* — *"Why are they charging for tokens, if it is so valuable?"*
  (businessinsider.com, digitalapplied.com, 247wallst.com — 2026-07-01/02)
- CNBC, June 10 2026: *"the product doesn't actually work and it's very expensive."*
  Says every Palantir enterprise customer is unhappy with frontier labs
  (Anthropic/OpenAI); calls it a **"hyper religion of hyper optimism."**
  Coins the term: frontier labs want customers to **"tokenmax"** — treating token
  consumption itself as a productivity metric, disconnected from real business value.
  (theregister.com, cnbc.com, 2026-06-10/11)
- Sept 5 2025 (earlier, same throughline): *"Silicon Valley totally effed up in
  overhyping LLMs."* *"An LLM is a raw material that has to be processed"* — value is
  in the implementation/system around the model, not the model alone.
  (semafor.com, 2025-09-05)
- Nov 2025 (thestreet.com): "two AI markets" — hype-heavy demo LLMs vs. systems that
  actually move revenue/margins; says the hype part is "already dissipating."

**Synthesis for the post:** Microsoft is the concrete corporate case of adopt-then-
retrench; Uber is the "we blew the budget" cautionary tale; Karp is the loudest
public voice naming the mechanism — token-maxxing treated as a proxy for AI adoption/
productivity, divorced from actual ROI, and enterprises are now correcting for it.
This is a more defensible version of "token apocalypse" than a pricing-hike claim:
**the shock isn't per-token price, it's aggregate agentic token consumption once
agents run loose** — and the pullback is real and already happening industry-wide by
mid-2026.

## Key material
- **Best quotable line (harness > spend):** "Frontier upgrades set the floor; harness
  and workflow design set the ceiling."
- **Best quotable stat (economics):** Anthropic op margin 38%→70%+ mid-2026; Opus
  pricing cut 67% (Feb 2026); OpenAI ~$2.20 spent per $1 revenue, 87-93% price
  collapse on frontier reasoning tiers 2024→2026.
- **Best mechanism line (lock-in):** Enterprise packaging shift from fixed-seat to
  base-fee-plus-usage, and Claude Code's per-dev-day billing — the lock-in is in
  *workflow integration*, not token price.
- **Counterpoint worth including:** METR — AI tools produced a 20% slowdown for
  experienced devs without strong harness/verification loops. Reinforces "harness
  matters" but complicates a simple "AI = productivity" narrative.
- **Best quotable line (belt-tightening angle, chosen for opening beat):** Karp:
  "I am paying for tokens that create no value" / labs want customers to "tokenmax."
  Concrete corporate proof point: Microsoft cancels internal Claude Code licenses
  (Jan 2026 expansion → May/June 2026 retrenchment to GitHub Copilot CLI); Uber
  exhausts entire 2026 AI coding budget by April.
