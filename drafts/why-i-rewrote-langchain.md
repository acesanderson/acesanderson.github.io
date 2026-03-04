# Draft: Why I rewrote LangChain from scratch

**Status:** Idea
**Source:** Code Learnings.md, ~5/18–5/19/2024 and forward (Chain Framework)

## Core argument
LangChain's abstractions made simple things hard and complex things fragile. Building a
minimal replacement taught me what the complexity is actually for — and what you can
safely skip.

## The frustration
- Messy import statements ("their import statements are insane")
- Hard to trace how variables get passed through Runnables
- Output parsers were roundabout (format_instructions as a side channel)
- RunnableParallel vs. RunnableSequence coercions felt like magic
- Ultimately: hard to debug, hard to reason about

## The build
- `NOLC.py` → eventually `Chain.py` → eventually `conduit`
- Design goal: minimal interface. `Chain('tell me about {{topic}}').run('the West Wing')`
- Key design choices:
  - jinja2 for templating (clean, familiar)
  - Single `run()` method with sensible defaults
  - Model as a first-class object with `.query()` and `.chat()`
  - Parser that defaults to string but supports JSON, list, Pydantic (via Instructor)
  - `Response` object that remembers the prompt and model (observability)

## What I learned from building it
- The complexity LangChain hides is real: async, streaming, tool calls, retries
- But for 80% of use cases, you don't need any of that
- Understanding the primitives (prompt → model → parser) makes everything else clearer
- You can pipe-syntax your way to chain composition without a framework

## Why this is interesting
- Classic "I built my own X" post — always gets engagement
- Has a strong opinion: LangChain is over-abstracted for most solo projects
- Concrete code examples to anchor the argument
- Has a genuine arc: frustration → build → learn → evolve

## Potential structure
1. The promise of LangChain and where it fell short for me
2. The first sketch: NOLC.py
3. Design principles I settled on
4. What I gave up (and why I don't miss it)
5. What LangChain is actually for (and when you should use it)

## Notes
- Chain Framework is public on GitHub — link it
- The framework has evolved significantly (async, Instructor, MessageStore, FSM Engine)
  — frame the post around the original insight, not the current state
- Potential follow-up posts: async LLM calls, observable pipelines, the FSM pattern
