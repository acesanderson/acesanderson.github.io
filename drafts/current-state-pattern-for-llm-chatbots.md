# Draft: The current_state = current_state() pattern for LLM chat flows

**Status:** Idea
**Source:** Code Learnings.md, ~5/29–5/31/2024

## Core argument
When building LLM-driven chatbots with branching logic, nested while loops are a trap.
State-driven programming — where each state is a function that returns the next state —
makes complex flows readable, testable, and extensible.

## The problem
- Building a "librarian" chatbot: receive request → evaluate intent → query database →
  respond or loop
- Initial approach: nested while loops with match/case
- Result: "The nested while loops make my head spin"
- Hard to debug, hard to extend, hard to reason about

## The discovery
The pattern:
```python
def main():
    current_state = human_input
    while True:
        current_state = current_state()
```
Each function is a state. It does its work, then returns the *function* that represents
the next state. The main loop just runs whatever state it's currently in.

## Why this works for LLM applications
- Each state maps cleanly to a step in your FSM diagram
- You can draw the flow in Mermaid first, then have GPT generate the Python skeleton
- LLM calls live inside the state functions — clean separation
- Much easier to add a new state (new function) vs. refactoring nested loops
- Naturally supports the "Chain of Responsibility" pattern for routing

## The Mermaid connection
- You can diagram the FSM visually in Mermaid
- Convert diagram → Python boilerplate (Claude is good at this)
- This becomes a design workflow: diagram on paper → Mermaid → skeleton Python → fill in

## Why this is interesting
- Short, teachable, concrete
- The aha-moment is clear and memorable
- Applicable beyond LLMs — any stateful CLI or chatbot
- Has a worked example

## Potential structure
1. The nested while loop trap
2. The FSM insight: chatbots are finite state machines
3. The pattern: current_state = current_state()
4. Worked example: a simple librarian chatbot
5. The Mermaid → Python workflow

## Notes
- Good candidate for a shorter post (TIL format) or a deeper technical dive
- Follow-up territory: how this scales to more complex agents, tool use, etc.
- The "Chain of Responsibility" framing (from 5/30 entry) is worth including
