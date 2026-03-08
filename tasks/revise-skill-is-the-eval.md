# Task: Revise "The Skill Is the Eval"

## Objective
Revise the published post `_posts/2026-03-05-the-skill-is-the-eval.md` with sharper
examples and new insights from actually running the Skills v2 eval loop. Do NOT touch
the existing draft in `drafts/`.

## Output
Edited in place: `_posts/2026-03-05-the-skill-is-the-eval.md`

## Context to read first
- `_posts/2026-03-05-the-skill-is-the-eval.md` — the live post to be revised
- `context/post-candidates.md` — for tone/audience calibration

---

## Background (what generated this task)

After the post was published, Brian ran the Skills v2 description optimization loop
on the `sec-filings` skill. The run produced a concrete case study with a non-obvious
result: 0% recall across 5 iterations, even as Claude generated qualitatively much
better descriptions. This is the kind of real-world finding that would make the post
better — it reveals something the post currently asserts without evidence.

A second finding: the post currently uses a commit-message-generator as its concrete
example. Better candidates were identified. The strongest is `deslop` (Brian's own
skill) because it has highly enumerable, concrete criteria and the before/after is
viscerally legible to anyone who writes.

---

## Specific improvements

### 1. Replace or augment the `evals.json` example

The current example is a commit-message-generator. The preferred replacement is
**deslop** — Brian's blog post finishing skill. It has concrete, enumerable assertions:
- Does the output contain none of the banned vocabulary (delve, leverage, robust, etc.)?
- Is em-dash frequency reduced?
- Are sentence lengths more varied (burstiness reduced)?
- Were only flagged items changed, not the surrounding prose?

The second test case (the edge case that earns its keep) should test what happens when
a draft has subtle AI-isms that aren't in the banned word list — things like formulaic
opening structures ("In today's world..."), performative hedges ("It's worth noting..."),
or unearned conclusions ("This changes everything."). A mediocre skill flags nothing; a
good skill catches the pattern even without a keyword match.

The meta angle is editorially interesting: a post about evals using a skill that was
itself developed with eval-driven thinking as the example.

### 2. Add a section on the description optimization loop

The post currently mentions "automated trigger-description optimization" in one sentence
in the intro. It deserves its own section with:

- What it actually does: runs each prompt through a headless Claude session 3× (because
  triggering is probabilistic), measures trigger rate, calls Claude to propose a better
  description if train failures remain, iterates up to 5 times, selects winner by
  held-out test score to prevent overfitting
- The two distinct optimization problems this reveals: (a) does the skill produce good
  output when invoked (what the grader handles), and (b) does the skill get invoked at
  all (what the description loop handles). These are structurally different problems and
  the post currently conflates them.

### 3. Add the "intentional vs. opportunistic invocation" distinction

The description optimization loop has a real ceiling for skills that users explicitly
invoke (rather than skills Claude should spontaneously reach for). The sec-filings run
illustrates this concretely: every query returned 0% trigger rate because Claude
concluded it could answer "what does Palantir say about concentration risk" from
training data. It wasn't wrong — it just didn't feel the need for a tool.

This maps directly onto the "capability uplift vs. encoded preference" distinction
already in the post. Capability uplift skills (where Claude doesn't have real-time
data access) should trigger opportunistically; encoded preference skills are explicitly
invoked. The description loop is more useful for the former.

Framing suggestion: "The description optimization loop revealed something the post
currently asserts without evidence: the eval has a ceiling. A skill where Claude
thinks it can answer from memory will show 0% recall regardless of description
quality. That's not a failure — it's a signal about which skills need description
optimization and which ones don't."

### 4. Sharpen the final section

The closing line — "Your golden dataset is the skill" — is strong. The revision could
add a concrete counterexample: a skill where the golden dataset said "trigger when
users ask about public company filings" but the model consistently didn't, because the
model believed it already knew the answer. The golden dataset is the skill; the model
is the compiler; sometimes the compiler refuses your code for reasons you didn't
anticipate. That tension is real and the post currently glosses over it.

---

## Constraints
- Do NOT rewrite the existing draft (`drafts/2026-03-05-the-skill-is-the-eval.md`)
- Edit the published post in place — this is a revision, not a new post
- Preserve the post's voice and structure; add/replace sections, don't rearchitect
- Run deslop after edits are final, before considering the revision done
- Append to `manifest.md` when done
