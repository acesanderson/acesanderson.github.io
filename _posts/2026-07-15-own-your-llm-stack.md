---
layout: default
title: "Own your LLM stack"
date: 2026-07-15
---

# Own your LLM stack

In January, Microsoft expanded internal use of Claude Code across its major engineering teams. It encouraged even nontechnical staff to try it. By May, the company was canceling most of those licenses in its Experiences + Devices division and telling engineers to move to GitHub Copilot CLI by the end of June. Uber's CTO said the company blew through its entire 2026 AI coding budget by April, four months into the year.

Alex Karp put it plainer than anyone else has bothered to. On CNBC in June, he said every single enterprise customer Palantir talks to is unhappy with frontier labs. "The product doesn't actually work and it's very expensive." A few weeks later, sharper still: "I am paying for tokens that create no value." He has a name for what got a lot of companies here: tokenmax. Treat token consumption as a productivity metric, watch usage go up and to the right, mistake that line for progress.

Prices keep falling, but consumption keeps climbing for anybody who is AI-first with their work. Give an agent a large context window and permission to iterate on its own, and it will happily burn through a budget that looked generous on paper. A lot of 2025 was companies incentivizing employees to rack up usage as a proxy for AI adoption. 2026 is the bill arriving.

Here's the part that should worry anyone who considers themselves AI-first: raw token sales can't carry the margin they used to, so hyperscalers are pivoting to a different lock-in mechanism; not the model, but the environment around it. Some examples: Claude Code, Copilot's integration into everything Microsoft ships, Gemini wired into Workspace. The pitch stops being "our model is smarter" and becomes "you can't leave without rebuilding your entire workflow."

## The harness matters more than the model

There's a counter-trend running underneath all of that, and it happens to be good news. Open-weight models are closing the capability gap fast, and new quantizations are putting genuinely large models on consumer hardware. People who actually ship agentic coding tools have mostly landed on the same conclusion for 2026: frontier upgrades set the floor, harness and workflow design set the ceiling.

In practice, once you have a decent harness, structured output, test loops, tool calling, a repeatable evaluation setup, the model underneath stops being a religious choice. It's a cost and performance tradeoff. Swap it out. See what changes. That's it.

The thing worth owning, then, isn't a subscription to whatever model tops the leaderboard this month. It's the harness.

## Own the harness, not the model

I keep my skills, prompts, and MCPs centralized and deliberately agnostic to whichever agent happens to be running them that day, a Wiki I carry with me rather than something built into Claude or OpenCode specifically. GNU Stow symlinks the pieces I want into whatever tool needs them.

The test I care about: can I pick up and move to a different model or harness by lunchtime? If the answer is yes, I'm insulated from whatever the hyperscalers decide to do next, price cuts, price hikes, a new walled garden, the next Claude-Code-style bundling push. If the answer is no, I've built exactly the kind of dependency Karp is complaining about, just at a personal scale instead of an enterprise one.

Day to day, that stack breaks into three layers.

## Traditional chats

- Open WebUI, running gemma4 locally, handles short generalist questions. It's free and private and there's no reason to burn a cloud call on something this size.
- Perplexity is for grounded research, when I need citations more than I need a clever answer.
- Gemini gets the long, in-depth conversations. Its context window is the reason to reach for it, not its reasoning.

## Agentic work

- Hermes runs my personal knowledge base and personal task management, on xiaomi's mimo-v25 through OpenRouter, a model with a 1M-token context window that costs almost nothing. I switched over from OpenClaw gradually. I can reach Hermes from my phone over Matrix, which matters more than it sounds like it should. A cheap model I can always reach beats a better model I can only use from a laptop.
- OpenCode splits by task complexity: mimo-v25 in the cloud for anything genuinely hard, ornith-35b-q8 served locally for implementation work once the plan is set.
- GitHub Copilot CLI handles agentic work for my job, on an enterprise subscription. This one's not really a choice. It's the harness the job hands you. But it's also proof the portability principle still applies even in a context you don't control: the skills I bring to it are still mine.
- Pi coder does unassisted agentic coding, executed inside a microvm, currently on ornith-35b-q8 served locally. No cloud dependency, no blast radius if it goes sideways.

## The skills layer

This is the part that makes everything above swappable instead of load-bearing.

The mechanism is boring on purpose: **GNU Stow** symlinks whatever a given agent needs, and I unsymlink it the moment I move on. No copying, no per-tool config drift.

The skills themselves do the actual work. **blackglass** is a RAG server sitting in front of my Obsidian vault, with an API tight enough that any agent can read or edit notes directly instead of me pasting them into a chat window by hand. **conduit** is the tool belt underneath most of my agentic work: it lets an agent query Perplexity, Gemini Deep Research, Anthropic, or OpenAI on my behalf, and it runs an embeddings and reranker server the agents call directly. The most common thing I actually type is some version of "send out several Perplexity queries and research this while I do something else."

A couple of the smaller ones earn their keep by replacing a tool that ships broken by default. **web-search** stands in for the bare "fetch" most agents come with, and adds real search engines, Firecrawl, and proxies for when one API call isn't going to get a real answer. **youtube** pulls from the YouTube Data API and the transcript API so I can analyze a video or a channel without watching it.

**tmux** is how an agent displays artifacts in a pane, spawns another agent in a pane of its own, or runs a command over SSH on a different machine entirely. I expect to replace it with something like cmux or herdr once a real community of practice forms around one of them, but for now it's mine and it works. And **sdd** is what's left of the Superpowers plugin after I stripped it down to an opinionated project structure, a job queue, and a Gitea issues workflow, the parts I actually use, none of the parts I don't.


## Start small

None of this makes me an AI engineer, and it doesn't need to. It's a handful of symlinks and a folder of markdown files that any agent can read. Most of the engineering happened once, back when I moved from OpenClaw to Hermes and didn't want to rebuild everything from scratch. That was the moment I actually decided the skills lived outside any one tool, not some grand plan going in.

I don't know how the hyperscalers' bundling strategy plays out, whether Claude Code wins, whether Copilot eats it, whether some integration nobody's shipped yet makes this whole question moot. What I do know is that the folder of skills on my machine doesn't care which one wins. That's the part worth building first.
