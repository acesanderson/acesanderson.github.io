# Draft: Building LLM pipelines you can actually watch

**Status:** Idea
**Source:** Code Learnings.md, ~10/21–10/28/2024

## Core argument
The feedback loop between "make a change" and "understand what the LLM did" is the
biggest productivity bottleneck in LLM development. A simple logging setup — structured
JSON, live tail, tmux pane — closes that loop without any external tooling.

## The problem
- Complex LLM chains are hard to debug because side effects are invisible
- Print statements are too coarse; they disappear and don't persist
- Expensive to re-run chains just to see what happened at step 3
- "I spent an hour today going in circles because I had no visibility into what was
  being passed to the LLM"

## The setup
- `MessageStore` class in Chain: stores every LLM interaction (prompt, response, model,
  duration) as a structured log
- Writes to `log.json` in append mode
- Watch it live: `clear && tail -f log.json` in a separate tmux pane
- Pretty-print with rich in another pane

## What this gives you
- See exactly what prompt went to the LLM (including rendered jinja2 templates)
- See the raw response before parsing
- Duration per call (spot slow steps)
- Persistent log you can grep or load into a notebook later
- Works across nested imports — any module that uses Chain logs automatically

## The tmux workflow
- Pane 1: editor (nvim)
- Pane 2: running the script
- Pane 3: `clear && tail -f log.json` — live LLM activity

## Why this is interesting
- Practical, immediately actionable
- Most LLM debugging advice is either "add print statements" or "buy an observability
  platform" — this is the middle ground
- The tmux workflow angle gives it a personal/opinionated flavor
- Pairs well with the "here's what I found, here's what broke" voice

## Potential structure
1. The debugging problem with LLM pipelines
2. What I wanted: see exactly what goes in and comes out
3. The MessageStore design (brief — not a full code walkthrough)
4. The tail -f workflow
5. What this unlocked (found and fixed a bug in Mentor that had been hiding for weeks)

## Notes
- The specific bug this fixed: Mentor wasn't adding enough context to Curate calls —
  only using course title. Once I could see the prompts, I found the issue immediately.
  3x quality improvement after the fix.
- Keep the code examples minimal — the insight is the workflow, not the implementation
