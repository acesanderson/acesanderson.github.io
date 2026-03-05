---
layout: default
title: "I spent months building MCP. Then I abandoned it."
date: 2025-11-14
---

# I spent months building MCP. Then I abandoned it.

The Model Context Protocol launched in late 2024 and immediately struck a chord with
AI engineers. It promised standardization and an accelerated path to building plugins.

As a learning exercise, I built my own framework for MCP. Like a faithful buddhist and
their canoe, it took me where I wanted to go, and now I'm abandoning it on the shore.
Here's the story.

## What MCP promises

The pitch is genuinely compelling. MCP defines a standard protocol for connecting an
AI "host" to external "servers" that expose tools, resources, and prompts over a
JSON-RPC transport. The LLM doesn't need to know how your database works or how to call
your calendar API, it just calls a named tool and MCP handles the rest.

For enterprise agentic systems, this makes a lot of sense. You write an MCP server once.
Any compliant host can use it. Claude Desktop, Claude Code, your custom app — they all
speak the same protocol.

## Building MCPLite

I didn't just read the docs and try to use it. I built my own implementation from
scratch — MCPLite — so I could understand what was actually happening.

I drew the architecture on paper first. Host, client, server, transport. The JSON-RPC
message passing. The handshake. Then I coded it up, starting with a `DirectTransport`
(just importing and calling functions directly, mocking the protocol locally) before
moving to proper stdio.

When I finally got a working stdio implementation and ran MCPChat against a `fetch`
server — watching it reach out and summarize the MCP documentation — it was a genuine
thrill.

But the process of building it is what showed me why I didn't need it.

---

## What's actually wrong with MCP for personal use

**The context problem.** MCP's standard flow loads tool definitions upfront —
descriptions, input schemas, all of it — so the LLM knows what's available. This is
fine for five tools. It becomes a serious problem at scale. I was planning to expose
my entire research infrastructure: web search, database queries, course retrieval,
Obsidian notes, transcript processing. This quickly confused the LLM and filled up its
context with schema definitions.

**The schema problem.** MCP communicates in JSON-RPC, which means the LLM is navigating
JSONRPC schema definitions to understand its tools. LLMs are trained on natural language
and code, not protocol specs. Strikingly, some Cloudflare engineers found that just
asking LLMs to treat the MCP server as a plain HTTP API with natural language descriptions
worked better. LLMs don't "speak MCP", but they sure do speak "API with docs".

**The wrong abstraction.** MCP is designed for *action-directed* agents — agents that
take consequential actions in external systems. `updateSalesforce`. `createJiraTicket`.
`sendSlackMessage`. The protocol's emphasis on typed inputs, error handling, and
formalized handshakes makes sense in that context. As an information worker, 
my use case is almost entirely "information-directed": retrieve context, synthesize,
respond. The complexity MCP adds doesn't solve any problem I actually have.

**We already have tools, and they work great.** MCP provides several "primitives": tools,
resources, and prompts. But in the vast majority of use cases, people are just using
MCP to expose tools. And tools are a very mature abstraction, and trivial to use with
OpenAI, Anthropic, or even Ollama. If you just want tools, don't bother with the protocol.

**MCP is production-grade.** If you're building massive agentic systems for enterprise use,
MCP makes more and more sense. But Anthropic designed it to be primarily stdio, which 
presupposes desktop applications. And if you want MCP servers over HTTP, streaming is not optional.
You have to implement SSE or WebSockets yourself. MCP doesn't work for your average "FastAPI on a napkin" server.

## What I use instead: Skills

Anthropic's new Skills framework is a breath of fresh air, and it meets LLMs where they are:
text context. No premature overengineering. Just set up a text-based adventure for the model.

The fancy term is **progressive disclosure**. The problem isn't
that the LLM has access to too many tools, but instead that they're all broadcast
at once, before the model knows what task it's doing. The solution isn't fewer
tools. It's loading the right tool context at the right time.

Skills are a clean implementation of this idea, and Anthropic formalized them in October
2025. The structure is a three-level lazy load:

**Level 1 — always loaded, ~100 tokens per skill:**
A name and a one-line description, injected into the system prompt at startup. This is
cheap enough that you can have dozens of skills registered with essentially no context
cost.

**Level 2 — loaded on trigger, <5k tokens:**
The full `SKILL.md` body, loaded into context only when the model identifies a match.
Instructions, examples, any persona or reasoning protocol the skill requires.

**Level 3 — loaded on demand, unlimited:**
Reference files, scripts, data — accessed only when the skill body asks for them.
Output only enters context, not the source files themselves.

The model never sees more than it needs for the current task.

A `SKILL.md` file looks like this:

```markdown
---
name: brave-web-search
type: skill
description: Search the web and fetch URLs as clean Markdown. Use when the user
  wants to search for information online or read web page contents.
---

## How to use this skill

Use the `brave_search` tool with a query string. For fetching a specific URL,
use `fetch_url` instead.

Results are returned as Markdown. Prefer specific, targeted queries over broad ones.
```

The YAML frontmatter is what gets loaded at Level 1. The body is Level 2. Any files
in a `references/` subdirectory are Level 3.

---

## How the implementation works in Conduit

My implementation in Conduit is deliberately minimal. The whole thing is about 150 lines
across five files.

A `Skill` is a Pydantic model with three fields: `name`, `description`, and `body`. It
parses the YAML frontmatter and markdown body from the file:

```python
class Skill(BaseModel):
    type: Literal["skill", "context", "prompt"] = "skill"
    name: str
    description: str
    body: str

    @classmethod
    def from_path(cls, path: Path) -> Skill:
        content = path.read_text(encoding="utf-8")
        metadata, body = parse_skill(content)
        return cls(**metadata, body=body)
```

The `SkillRegistry` scans a directory for `SKILL.md` files and registers each one:

```python
@classmethod
def from_skills_dir(cls, skills_dir: Path) -> SkillRegistry:
    registry = cls()
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                registry.register(Skill.from_path(skill_file))
    return registry
```

The system prompt template renders the skill list as a lightweight XML block:

```jinja2
<available_skills>
{% for skill in skills %}
  <skill>
      <name>{{ skill.name }}</name>
      <description>{{ skill.description }}</description>
  </skill>
{% endfor %}
</available_skills>
```

And the bridge is a single `enable_skill` tool. When the model calls it, it gets the
skill body rendered into context — nothing more:

```python
async def enable_skill(skill_name: str, _skill_registry: SkillRegistry) -> str:
    skill = _skill_registry.get_skill(skill_name)
    return skill.render()
```

That's essentially the whole thing. The model sees a short list of skill names and
descriptions. When it identifies a relevant skill, it calls `enable_skill`. The full
instructions land in context. The model proceeds with the task.

There are three skill types — `skill` (action/tool documentation), `context`
(facts/constraints to ground the model), and `prompt` (behavior override) — each
rendered with a different XML wrapper so the model can tell them apart. But the loading
mechanism is identical for all three.

## What's next

The one gap in the Skills model is tools — actual function calls, not just loaded
context. Skills handle progressive disclosure of instructions beautifully, but the
question of how to progressively disclose capabilities (things the model can actually
execute) without flooding context with tool schemas is still open.

I'm exploring this now.

---

## Addendum — 2026-03-04

I have a great toy project for experimenting with this.

For personal reasons I'm shifting away from OpenAI. Its role for me was increasingly
just another llm in a browser tab for one-off questions. I've replaced it with OpenWebUI
running locally on my private network, and it's been fantastic, and completely private to boot.

OpenWebUI has all the frills of modern llm chat apps (branching, system prompts, etc.) though
it doesn't support MCP, nor skills. Tools support is possible if you connect an OpenAPI server.

My FastAPI tools server (code name "Watergun") is a simple wrapper around my tools and data sources.
It exposes endpoints for web search (via Brave API), URL fetching, and Obsidian vault queries.
Open WebUI connects to it via its OpenAPI spec, and the model can call any of those tools.

The progressive disclosure problem remains. Open WebUI sends the full OpenAPI spec to
the model at the start of every conversation. With a small tool set it's fine. As
Watergun grows, it won't be.

My current experiment: a self-editing OpenAPI spec. When certain skills are
accessed, Watergun updates its exposed spec to surface only the tools relevant to
that skill context. The full tool set lives server-side; the model only sees the slice
that's appropriate for the active skill. I suspect this is my path to fully owning my
tools + skills in a private llm setup.

---

*Watergun is part of the Watershed ecosystem — a set of tools and servers for personal
AI infrastructure. MCPLite is archived in my Chain Framework repository.*
