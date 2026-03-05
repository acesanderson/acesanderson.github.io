# Chain Project History

Source: https://github.com/acesanderson-archive/Chain (public archive)
Researched: 2026-03-04
Purpose: Raw material for "why I built my own LangChain" blog post

---

## Repository Basics

- **Created**: May 29, 2024
- **Archived**: October 9, 2025
- **Total commits**: 689
- **Original name**: "Chain-Framework" (renamed mid-development)
- **Language**: Python exclusively
- **Successor**: conduit-project (v2 + rebrand)

---

## Phase 1: RAG Application / Domain-Specific Tool (May 2024)

**First commit** (`6680c2e`, May 29, 2024):
- `Chain.py` — monolithic single-file class already named "Chain"
- `Agent.py`, `Retriever.py`, `VectorStore.py`, `Create_VDB.py`
- `Course_Descriptions.py` — domain-specific data, suggesting a **course curriculum tool**
- `chains/` directory with specific pipeline scripts: `chain_curation.py`, `chain_RAG.py`, `chain_role_progression.py`, `chain_structured_curation.py`
- Vector DB files (Chroma)

**Critical design note from original Chain.py docstring** (the TODO list):
```
This is me running my own framework, called Chain.
A link is an object that takes the following:
- a prompt (a jinja2 template)
- a model (a string)
- an output (a dictionary)
```

The original class already used Jinja2 templates for prompts, hardcoded model lists (ollama, openai, anthropic, google), and had a `Parser` class for structured output. It was **already self-consciously a framework** from day one — not a script that evolved into one. The TODO list explicitly called out missing features: regex parsers, temperature, async, piping, tracing.

**Key design decision made at the very beginning**: Jinja2 for prompt templating. This never changed across the entire project lifetime.

**LangChain reference**: The original code's TODO list references LangChain's output parsers as comparison point: "consider other format types like [langchain's](...)" — a casual note, like noting prior art, not code being migrated away from. No LangChain dependency ever appears in the codebase.

---

## Phase 2: Course-Chatbot / Applied Experimentation (May–June 2024)

Building real applications simultaneously with the framework:

- "renamed chatbot to Librarian as that's its persona in the bigger Curriculum Chain" (May 31)
- "created obsidian command line tool for summarizing youtube / articles" (June 12)
- "created ask.py" — a CLI tool for quick LLM queries (June 13)
- MongoDB and Chroma vector DB experimentation (June 2–3)
- Groq added (June 9)
- **June 25 pivot**: "reworked Parser class entirely so that we use Instructor. Cut 75 lines of code." — switched from hand-rolled Pydantic parsing to the `instructor` library

**Key pattern**: Building real tools (`ask.py`, `obsidian.py`) simultaneously with the framework. The framework was immediately load-bearing.

---

## Phase 3: v1 Stabilization — Multi-Machine, Multi-Provider (June–September 2024)

- Async query functions added for OpenAI (July 2024)
- **July 14**: "added a crude rate limit to Model.run_async because I accidentally sent 4,000 API calls" — framework was doing real batch processing work
- Remote Ollama via SSH tunnel (July 6: "allowed user to change to a different ollama client, i.e. magnus") — chess-player hostnames: magnus, petrosian, alphablue, caruana — a personal compute cluster
- New model aliases tracked as providers released them: GPT-4o-mini, Claude 3.5 Sonnet, etc.
- O1 Strawberry added (September 21)

---

## Phase 4: v2 — Full Rewrite as Proper Package (October 2024)

**Trigger**: "Complete refactor of Model class to lazy load openai/anthropic/ollama/gemini/groq SDKs, save two seconds on start up" (October 13) — startup latency from eager imports was the breaking point.

**The v2 rewrite was rapid and intense** — 30+ commits in a single day (October 21):
- "retitled entire project to Chain" (October 21, 00:50)
- Proper `setup.py`, client classes extracted into `clients/` folder
- Pydantic `Message` objects replacing raw dicts
- `MessageStore` class for conversation history (persistent via pickle)
- LazyLoad pattern for all API clients

**Key architectural decisions in v2**:
1. Client classes as subclasses (OpenAIClient, AnthropicClient, OllamaClient, etc.) inheriting from a base `Client`
2. `Model` class as the single unified interface, dispatching to the right client
3. `Response` as a proper dataclass
4. Persistent conversation logging via `MessageStore`

---

## Phase 5: v2 Feature Expansion → v2.5 (October 2024 – January 2025)

Major additions:
- Pydantic message validation throughout (October 22)
- Async chain as a subclass of Chain (December 15–16: "major refactor; async is now a subclass")
- SQLite caching (`ChainCache`) — January 12–14, 2025: "Cache now works (singleton on Model)"
- ReACT agent implementation — January 15: "minimal use case for react agent works"
- Streaming support — January 16: "Added streaming to Model, openai_client, and Chain.run_stream"
- DeepSeek client — January 5
- Full `Chat` class with command system (January 9)
- `CLI` base class abstraction — January 25: "implementing a CLI class that will become the core of ask/leviathan/tutorize/cookbook"

**Version marker**: January 25, 2025 — "This is version 2.5; with Chat, CLI, and ReACT implementations"

By v2.5 the project had become a **platform** rather than a framework. The CLI class was explicitly planned to be "the core of ask/leviathan/tutorize/cookbook" — personal productivity tools built on top of Chain.

---

## Phase 6: Provider Expansion + Infrastructure Work (February – April 2025)

- Groq client (February 3)
- Perplexity client with custom Response subclass (January 30)
- New model releases tracked: Claude 3.7, Gemini 2.5, GPT o4-mini, DeepSeek
- Temperature parameter added to all clients (April 30 – May 1)
- Tokenization functions per provider (April 30)
- **MCP detour**: April 9–26 — built a near-complete MCP server/client implementation inside Chain, then extracted it: "plucked out the MCP stuff so it's in its own project called MCPLite" (April 26). The repo was used as an incubator for adjacent ideas.

---

## Phase 7: v3 — Multimodal + Distributed (May – June 2025)

- `ImageMessage` class (May 25); image support across OpenAI, Anthropic, Gemini
- `AudioMessage` class (May 28 – June 5)
- TTS (text-to-speech) across multiple providers (July 5)
- Image generation (DALL-E, Gemini, HuggingFace) — July 25–28
- `ChainServer` — distributed Chain server for remote model access (June 14)
- **v3 milestone**: June 23, 2025 — "v3 is ready!"

What v3 added:
- Complete Message class hierarchy (TextMessage, ImageMessage, AudioMessage)
- `Request` object for structured query parameters
- `ChainServer` for distributed model access
- Serialization/deserialization for all objects (2+ weeks of debugging)
- Verbosity enum (5 levels)
- Rich progress tracking with decorators

---

## Phase 8: Infrastructure Maturity (July – September 2025)

- `Odometer` — token usage tracking and cost monitoring (designed July 4, persistent implementation August 5–11)
- PostgreSQL backend for odometer
- `ModelStore` — local database of model specs using TinyDB (July 3)
- `PromptLoader` class (July 19)
- **September 17**: "Chain needs no server / client logic. Inherits SiphonClient" — Chain was now one component in a larger personal infrastructure ecosystem (SiphonServer, MCPLite, etc.)
- **Final commit**: September 25 (dependency cleanup)
- **Archived**: October 9, 2025

---

## Key Design Decisions Timeline

| Decision | Date | What Changed |
|---|---|---|
| Jinja2 for prompt templates | Day 1 (May 2024) | Never changed |
| Switched to `instructor` for Pydantic | June 25, 2024 | Cut 75 lines of hand-rolled parsing |
| Lazy-load SDK imports | October 13, 2024 | 2-second startup improvement |
| v2 restructure: client subclasses | October 14–21, 2024 | Monolith to proper package |
| Async as Chain subclass | December 16, 2024 | Cleaner API vs. separate module |
| SQLite caching | January 14, 2025 | First persistence layer |
| Pydantic messages throughout | October 22, 2024 | Type safety for conversation history |
| MCP implementation extracted | April 26, 2025 | Spin-off to MCPLite project |
| v3: Message class hierarchy | June–July 2025 | TextMessage, ImageMessage, AudioMessage |
| Serialization/deserialization | June 24 – July 1, 2025 | Required 2 weeks of debugging |
| SiphonServer integration | September 2025 | Chain becomes client-only |

---

## Development Velocity and Patterns

**Burst patterns**: Development happened in intense clusters:
- October 13–21, 2024: ~40 commits (v2 rewrite)
- December 14–16, 2024: ~12 commits (async refactor)
- January 9–16, 2025: ~15 commits (Chat, ReACT, streaming, cache)
- June 22 – July 5, 2025: ~100+ commits (v3 — the most intense period)

**Commit message tone**: Honest and unpolished — "WIP:", "vibed out", "fiddligna roudn with chainml", "going in circles", "struggling with relative imports". Personal work, not prepped for external contributors.

**Multi-machine development**: SSH-tunneled remote Ollama access to chess-player-named hosts (magnus, petrosian, alphablue, caruana). Chain had to work across machines throughout its life.

---

## The Developer Story Arc

**Act 1 (May–Oct 2024)**: Builds a specific course-generation tool. Realizes the LLM-calling plumbing is reusable. Extracts it into a framework. Fights with imports, lazy loading, startup time. It becomes a real package.

**Act 2 (Oct 2024 – Mar 2025)**: The framework becomes the foundation for personal productivity. Chat interface, CLI tooling, caching, async, streaming, ReACT agents. The `ask` command, `chat` command, and various personal tools all built on top. Version 2.5 is a working personal AI toolkit.

**Act 3 (Apr–Sep 2025)**: Multimodal, distributed infrastructure, token tracking, model management. A complete MCP implementation was built and spun out. The SiphonServer integration in September shows Chain had become one node in a larger personal homelab AI infrastructure stack.

**Archived October 9, 2025**: Superseded by the infrastructure it helped create. Not abandonment — preservation.

---

## What It Reveals About the Developer

- Strong preference for simplicity: repeatedly refactored to remove code, extracted subprojects, fought bloat
- Learns by building: real tools alongside framework, framework was always load-bearing
- Multi-machine homelab enthusiast: personal compute cluster with chess-player hostnames
- Comfortable with low-level plumbing: serialization, async, caching from scratch
- Builder mentality: produces working tools rather than documentation
