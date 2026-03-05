# Conduit Project History

Source: https://github.com/acesanderson/conduit
Researched: 2026-03-04
Purpose: Raw material for "why I built my own LangChain" blog post — Conduit is Chain v2 + rebrand
Predecessor history: context/chain-project-history.md

---

## Repository Basics

| Field | Value |
|---|---|
| URL | https://github.com/acesanderson/conduit |
| Created | September 26–29, 2025 |
| First meaningful commit | Sep 29, 2025 ("Complete rewrite of conduit") |
| Last commit | March 3, 2026 |
| Total commits | ~331 |
| Primary language | Python (99.7%) |
| PyPI name | `conduit-project` |
| Version | 2.0.0 |
| Requires Python | >=3.12 |
| Predecessor | Chain (archived Oct 9, 2025, 689 commits) |

---

## Phase 0 — The Rename (Sep 29, 2025)

Chain was archived Oct 9, 2025. Conduit was born Sep 29 — twelve days before the formal archive. Three commits the same day:

- `c9e0629` — "Complete rewrite of conduit" (README, .gitignore, .envrc)
- `a8148d2` — "project clean up"
- `9c52c1c` — "renamed EVERYTHING except in tests"

The rename commit is revealing: Conduit was literally Chain renamed. The package went from `src/Chain/` to `src/conduit/`, version bumped from `3.0.0` → `0.1.0` (a deliberate reset, later updated to `2.0.0`). The full Chain architecture was carried over intact — Message class hierarchy, all provider clients, multimodal, compose, chat, cli, cache, llm_decorator. This was not a rewrite; it was a rename and structural reset.

The "complete rewrite" commit message was aspirational, not descriptive.

---

## Phase 1 — Stabilization and XDG/Config Work (Oct 1–31, 2025)

Making the renamed package work as a proper installable distribution:

- XDG standards applied to cache and message storage (Oct 16)
- Ollama models made host-specific (Oct 16)
- Configuration-driven model preference (Oct 16)
- `PromptLoader` updated for `importlib.resources` (Oct 26)
- Embeddings generation added (Oct 28)
- Server-side Postgres snapshot for token tracking (Oct 15)
- `RemoteModel` implementation, `batch` entry point (Oct 24)
- CLI merged: `twig` (the old standalone CLI tool) folded into `conduitcli` (Oct 16)
- Regression tests updated from "Chain" references to "conduit" format (Oct 16)

~50 commits in October, ~2/day. Frequent merges suggest multi-machine development continuing from Chain.

---

## Phase 2 — Architectural Rethink: "Functional Core, Imperative Shell" (Nov–Dec 9, 2025)

This is where Conduit diverged from Chain architecturally. A systematic restructuring guided by an explicit principle.

Key commits:
- Nov 8–9: Major Chat refactor for separation of concerns; command injection; keybindings
- Nov 16: Four new project areas committed: `conversation`, `tools`, `skills`, `stream`
- Nov 17: Tools registry, parsing, and execution complete
- Nov 24: Query function abstracted from Chat to allow Skills, Tools, MCP injection
- Nov 27: "Major refactor of Message / Request / Conduit / Model" — deep structural rework
- Nov 29: `RemoteClient` and `RemoteModel` created; "Major clean up of legacy design patterns"
- Dec 1: "Major refactor of project structure — Engine class envisioned"; `Conversation` and `Engine` classes stubbed
- Dec 2: Design decision commit — "Request -> Client -> Response" as the canonical flow; new README
- Dec 7: Cache working; Odometer working as middleware; progress output to stderr by default
- Dec 9: "Functional core, imperative shell" pattern formalized (explicitly credited to Claude Code); Engine converted to static methods; Conduit made mostly stateless; sync/async split clarified
- Dec 11: "Used Claude Code to formalize model/conduit per the 'functional core, imperative shell' pattern"
- Dec 12: `conduit_sync` confirmed working through full stack (engine → generate → model → response)

**Key architectural departure from Chain**: The Engine became a pure static-method state machine driven by `ConversationState` enum (`GENERATE` → `EXECUTE` → `TERMINATE` / `INCOMPLETE`). Conduit and Model classes made stateless. Chain's approach was stateful throughout.

The commit "in a deep dark forest where 2+2=5" (Dec 10) marks the hardest point of the async/sync refactor.

---

## Phase 3 — App Layer and Persistence (Dec 13–31, 2025)

With core machinery stable, work shifted to the application layer:

- Dec 13: `GenerationRequest` cache key fixed; `conduit_batch` working
- Dec 22–23: Major CLI refactoring; deferred loading via lambdas (performance optimization)
- Dec 26: `conduit_batch` async/sync split; headwater server integration
- Dec 27: Conversation serialization working
- Dec 28: "MAJOR vibed out refactor of Chat" (explicit vibe coding language); history display; persistence fixed
- Dec 29: Tool call implementation complete; four basic tools created (web search, fetch, file tools); "skills now works!"
- Dec 31: New `Conversation` and `Session` classes; `Message` with session ID and predecessor ID; "WIP: changing persistence model to Messages/Sessions"

The DAG-based conversation persistence model (messages with `predecessor_id` and `session_id`) began taking shape here.

---

## Phase 4 — Workflow Engine and Strategy Pattern (Jan 1–31, 2026)

January dominated by the `workflow/step/harness/strategy` framework:

- Jan 3: "Finally mapped out workflow/step/harness logic + implemented a promptfoo adapter"
- Jan 4: Initial workflow/step/strategy framework with summarization; `corpus.py` for datasets
- Jan 6: "Functional core" pattern applied; param cascade implemented; middleware passing trace data
- Jan 22: New README; `skills` entry point for sync/ad hoc use cases
- Jan 27: Cache management CLI created; `workflow/step` given `.diagram` and `.schema` properties

**Key design artifact**: 4-layer configuration cascade (runtime override → scoped config → global config → default) via `resolve_param()`. The workflow system used `ContextVar` injection via `Harness` — keeping domain logic pure while enabling auto-tracing and configuration injection.

---

## Phase 5 — Evals and Web Tooling (Feb 1–28, 2026)

- Feb 4: Web search tool added (OpenAI-backed); system prompt injects today's date
- Feb 6: `curl_cffi` browser spoofing + retry logic to fetch tool; header rotation; tools moved to own directories with `__init__.py` registry
- Feb 13: Dataset building began; compression algorithm created; gold standard prompt written
- Feb 14: Golden dataset generation complete with easy loader; `Strategy` abstraction created; `EngineResult` spec
- Feb 16: Golden dataset gets embeddings; loss function spec; MVP of loss function; Postgres schema spec for evals
- Feb 17: New Sonnet 4.6 model; audio/image modality updates
- Feb 23: Mistral working; modelcards + aliases generated; Google ImageGen models fixed
- **Feb 28: "Removed OpenAI models entirely"** — unexplained; hard removal

The evals work represents a maturity milestone: using Conduit's own workflow/strategy machinery to build evaluation datasets and loss functions, testing the framework against real summarization quality tasks. Eating your own cooking.

---

## Phase 6 — Current State (Mar 1–3, 2026)

- Mar 1: Logprobs support added
- Mar 3: Merge (HEAD)

**Active. Still being developed.**

---

## Current Architecture

```
src/conduit/
  core/
    clients/       # Provider SDKs (Anthropic, Google, Ollama, Perplexity, Mistral + remote)
    conduit/       # ConduitSync orchestration class
    engine/        # Engine FSM (generate.py, execute.py, terminate.py)
    eval/          # Evaluation interfaces
    model/         # ModelSync
    parser/        # StreamParser for streaming responses
    prompt/        # Prompt class (Jinja2 templating — unchanged from Chain day 1)
    workflow/      # Step, Harness, Strategy, Context
  domain/
    config/        # ConduitOptions
    conversation/  # Conversation + ConversationState (DAG model)
    message/       # TextMessage, ImageMessage, AudioMessage
    request/       # GenerationRequest, GenerationParams
    result/        # GenerationResponse
  capabilities/
    skills/        # Skills framework
    tools/         # Tool registry (web search, fetch, file tools)
  middleware/
    middleware.py  # Logging, caching
  storage/
    cache/         # Semantic cache (Postgres)
    odometer/      # Async token/cost tracking
    repository/    # Message/conversation persistence
    db_manager.py  # Connection pooling
  strategies/
    summarize/     # Recursive summarizer (primary eval target)
    rag/           # RAG strategies
    research/      # Research strategies
  apps/
    chat/          # Terminal chat UI
    cli/           # conduit CLI
    tap/           # Tap TUI (SPEC.md v0.4.0 — in-progress)
  sync.py          # Public API: Model, Conduit, Prompt (the clean face)
  async_.py        # Async entry point
  batch.py         # Batch processing
  remote.py        # Remote model access
evals/             # Evaluation framework with Jinja2 prompts, loss function, datasets
```

`sync.py` exposes `Model = ModelSync` and `Conduit = ConduitSync` as primary user-facing aliases. Deliberately simple public API over a layered interior.

---

## Key Design Decisions Table

| Decision | When | What Changed |
|---|---|---|
| Full rename, version reset to 0.1.0 | Sep 29, 2025 | `src/Chain/` → `src/conduit/`; psychological clean slate |
| Version labeled `2.0.0` | Post-rename | Signals "v2 of Chain" not truly new |
| Functional core, imperative shell | Dec 9–11, 2025 | Engine becomes static methods; Conduit/Model made stateless |
| Engine as FSM | Dec 9, 2025 | `ConversationState` enum drives `match` in `Engine.run()` |
| Request → Client → Response canonical flow | Dec 2, 2025 | Cleaner than Chain's approach |
| DAG-based conversation persistence | Dec 31, 2025 | Messages get `session_id` + `predecessor_id` |
| 4-layer config cascade in Workflow | Jan 6, 2026 | `resolve_param()`: runtime → scoped → global → default |
| Tools organized into registry | Feb 6, 2026 | Own directories with `__init__.py`; mirrors skills structure |
| Removed OpenAI models entirely | Feb 28, 2026 | Hard removal; unexplained |
| Headwater + Siphon as local dependencies | Ongoing | `[tool.uv.sources]` with local path editable installs |

---

## Development Patterns

**Commit velocity:**
- Sep–Oct 2025: ~55 commits (port + stabilization)
- Nov 2025: ~65 commits (most active; architectural experimentation)
- Dec 2025: ~80 commits (peak; core rewrite + app layer)
- Jan 2026: ~45 commits (workflow engine)
- Feb 2026: ~70 commits (evals + web tooling)
- Mar 2026: ~3 commits (to date)

**Patterns continuing from Chain:**
- Multi-machine development: frequent merge commits, chess-player hostnames still appearing
- "Vibe coding" language appears explicitly: "vibed out the clients", "MAJOR vibed out refactor of Chat", "jesus take the wheel"
- Spec-first development: SPEC.md files appear before implementations (Tap SPEC v0.4.0, `engine_result_SPEC.md`)
- Self-aware distress signals: "in a deep dark forest where 2+2=5" marks the hardest async/sync refactor point

---

## What This Adds to the Developer Story Arc

**Chain Act 3** ended with: SiphonServer integration, Chain as client-only node in a homelab ecosystem, version 3.0.0, 689 commits.

**Conduit continues:**

- **The rebrand was tactical, not transformational.** The version reset from 3.0.0 → 0.1.0 was about psychological clean slate. The real transformation happened in November–December 2025.

- **The architectural transformation was the "functional core, imperative shell" principle.** The Engine FSM (`GENERATE → EXECUTE → TERMINATE`) is the cleanest thing in the codebase — auditable, testable, and a direct response to Chain's stateful sprawl.

- **The DAG conversation model is the deepest new idea.** Chain had Messages as a linear list. Conduit adds `predecessor_id` and `session_id`, making conversations a traversable graph — enabling the Tap TUI's branching, amend, and rewind features.

- **"Tap" reveals the end goal.** The Tap SPEC (v0.4.0) describes a Vim-modal, keyboard-first, DAG-aware terminal interface — "the primary interaction surface of the Watershed system." Watershed is the name of the broader personal ecosystem. The developer is building toward a personal LLM workstation, not just a library.

- **The removal of OpenAI models** (Feb 28) is the most opaque event. Combined with Mistral addition and Anthropic/Google focus, it may reflect a deliberate move away from OpenAI dependence.

- **The evals work** (Feb 2026) signals the system is stable enough to be trusted for serious work — using Conduit's own machinery to evaluate Conduit's outputs. This is the maturity milestone Chain never reached.

**The arc in one sentence:** Chain was a craftsman building a workshop; Conduit is the same craftsman rebuilding the workshop with better architectural principles while simultaneously starting to build the things the workshop was always meant to build.
