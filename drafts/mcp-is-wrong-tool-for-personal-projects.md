# Draft: MCP is the wrong tool for most personal AI projects

**Status:** Idea
**Source:** Code Learnings.md, ~4/18–4/19/2025, 11/14/2025

## Core argument
MCP is a well-engineered protocol for action-directed enterprise agents. For personal
AI tooling where the goal is context retrieval and quality output, it's overengineered
and actively hurts LLM response quality. Skills-based progressive disclosure is better.

## The journey
- Spent months studying the MCP spec (client/host/server/transport architecture)
- Built MCPLite from scratch to understand it (drew it on paper first, then coded it)
- Got the "hello world" moment: MCPChat + fetch server summarizing MCP docs
- Then abandoned it

## The specific reasons for abandoning
1. Too many tool prompts in context degrades LLM output quality — the LLM gets confused
   about what to call and when
2. MCP uses a format far from natural language — LLMs are trained on prose, not JSONRPC
   schemas; Cloudflare found better results just having LLMs write API calls
3. Designed for action-directed agents (`updateSalesforce`, `createTicket`) — not for
   context retrieval and synthesis, which is 90% of personal use
4. Anthropic's recommended fix for context overload is a full code sandbox — even more complex
5. Progressive disclosure (Skills) gives you context when you need it, not all upfront

## The alternative: Skills
- Embed recipes as loadable skill files
- Lazy-load context into conversations progressively
- LLM only sees what's relevant for the current task
- Result: leaner context, better quality output

## Why this is interesting
- Timely and contrarian — MCP is heavily hyped right now
- Grounded in months of real implementation experience (not just reading docs)
- Has a clear, specific alternative
- The MCPLite build is a good story in itself

## Potential structure
1. What MCP promises and why it's exciting
2. Three months of building MCPLite: what I learned about the architecture
3. Why I stopped using it: the quality problem
4. Who it's actually for (enterprise action agents)
5. What I use instead and why it works better

## Notes
- Be careful not to be purely negative — acknowledge MCP's legitimate use cases
- The Cloudflare "treat it as an API" finding is worth citing (from 11/14/2025 entry)
- MCPLite is a good parallel story: sometimes building a thing is how you understand why
  you don't need it
