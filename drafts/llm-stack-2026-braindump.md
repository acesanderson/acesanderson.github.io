# Raw braindump: LLM stack post (2026-07-15)

Coming out of a summer vacation and wanting to put pen to paper on my current LLM usage.

Broader context: the token apocalypse has hit, and Anthropic/OpenAI are getting more expensive at the same time that open weights models are getting better and better. In terms of LLM performance, there are often more gains to be made in changing your harness than spending more money on raw model performance. And emerging best practices in knowledge base management, agentic workflows, and standardization across MCPs, the skill format, and the "LLM Wiki" pattern allow us to fight vendor lock-in by maintaining our own transportable LLM environment where the model choice is truly "plug and play". Local models have become sufficiently good enough for a wide variety of coding tasks, and new quantizations are bringing huge parameters models to consumer silicon.

As such, my own usage has emphasized:
- cheap cloud models (OpenRouter provides a huge variety) -- I now have access to an incredibly cheap model with a 1m context window, in the form of xiaomi's mimo-v25.
- local models -- gemma4 for general use, ornith for coding, and I'm experimenting with CPU offload on the qwen models for unattended / cron usage, where context window / model performance is more important that tokens per second.
- centralizing my environment: my skills, my prompts, my mcps. These are not specific to OpenCode, Claude, Hermes, Pi coder. I can always pick up shop and move to a different model or harness.

Getting more granular:
### traditional web-ui chats
- Open WebUI (running gemma 4 locally) -- for short, generalist questions
- Perplexity -- for online research, when I need grounded answers
- Gemini -- for in depth chats with long context windows

### agentic
- Hermes agent for personal knowledge base, personal tasks, using xiaomi/mimo-v25 (gradually switched over from OpenClaw). Can use it from my phone using matrix chat.
- OpenCode: xiaomi/mimo-v25 through OpenRouter for complex tasks; ornith-35b-q8 served locally for implementing features.
- GitHub Copilot CLI: for agentic work related to my job. (enterprise subscription)
- Pi coder: for unassisted agentic coding -- executed in a microvm. Currently uses ornith-35b-q8 servered locally.

### skills
- I maintain a centralized skills repo, and use GNU Stow to symlink the skills I want to specific agents
- "blackglass" -- a RAG server for my obsidian vault; also provides a tight API + centralized server for my agents to access / edit my vault.
- "conduit" -- a set of llm tools that agents can use, for querying perplexity, google deep research, anthropic / openai etc. Most common usage is when I tell hermes or a coding agent "send out several perplexity queries to research X". Also provides a server for embeddings generation + rerankers that agents can use.
- "web-search" -- replacing "fetch" on agents with a more complex skill that allows use of multiple search engines, firecrawl, web proxies, etc.
- "youtube" -- uses youtube data api / youtube transcript API to analyze videos, channels, etc.
- "tmux" -- simple skill that provides modes for an agent to display artifacts in tmux panes, start new agents in new panes, and remotely execute code across SSH. May replace this with out-of-the-box tools like cmux or herdr as communities of practice emerge.
- "sdd" -- a trimmed down version of the Superpowers plugin that uses an opinionated project structure, job queue, and gitea issues workflow.
