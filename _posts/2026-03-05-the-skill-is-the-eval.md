---
layout: default
title: "The Skill Is the Eval"
date: 2026-03-05
---

# The Skill Is the Eval

Anthropic shipped Skills v2 on March 3rd. The headline feature: evals are now built into the Skill Creator workflow. You write test cases — inputs, expected outputs, pass criteria — and the tool spins up six parallel agents (three with your skill, three without), runs them blind, and gives you a report: pass rate, latency delta, token cost. There's also automated trigger-description optimization, which iterates your skill's description against sample prompts until triggering accuracy improves.

For beginning AI engineers, this may come off as too ... machine learning-y. We use LLMs, not pytorch.

## There are actually two kinds of skills

Skills v2 draws a distinction that was always latent but rarely stated. There are two types:

**Capability uplift** — you're teaching Claude something it can't do well yet. OCR-based form filling, a proprietary data format, a specialized reasoning pattern. These skills have an expiration date. As base model capability improves, the skill becomes redundant. Past that point it can actively harm performance by over-constraining behavior the model now handles better on its own. A skill validated on Sonnet 3.7 may be a liability on 4.6.

**Encoded preference** — you're enforcing an organizational workflow or constraint. "Always require a police report for claims over $10k." "Generate output in this specific format." These never expire. They just need continuous verification.

This is Anthropic acknowledging the problem of skills drift. Hence all this talk about evals.

## The inversion

We experience Skills as lazy-loaded prompts and bundles of scripts. But tokens and scripts are cheap. The eval is the skill.

If the thing that determines whether a skill is working is its regression benchmark — the expected outputs, the pass criteria, the golden standard it's measured against — then that benchmark *is* the primary artifact. The instructions are what you write (or what Claude writes) to satisfy it.

This is the exact insight behind DSPy, the prompt optimization framework from Stanford. DSPy inverts the traditional development loop. Instead of writing a prompt and then testing it, you define your expected outputs and a metric first, then let the optimizer generate the prompt that best satisfies them. The optimizer produces the prompt; your expected outputs and metric are what you actually own. Expected outputs are ground truth; everything else is derived.

Skills v2's blind comparators and regression benchmarks are a constrained version of this same inversion. Anthropic is building toward a world where the golden dataset you write for your skill IS the skill — the instructions are what gets tuned against it, whether by hand, by Claude, or eventually by an optimizer.

## The "poor man's eval": silver -> gold

Evals as a discipline has a rich and growing ecosystem — DeepEval, Braintrust, RAGAS, Langfuse. Senior practitioners treat them as unit tests in CI/CD, automated and version-controlled. That's a series of posts on its own.

But here's what the Skills v2 eval format actually looks like under the hood. Developers who've used promptfoo will find this immediately familiar.

The core artifact is `evals.json`: an array of test cases, each with a prompt, a natural-language description of what a correct output looks like, and a list of Boolean assertions the grader will evaluate. Here's a realistic example for a commit-message-generator skill:

```json
{
  "skill_name": "commit-message",
  "evals": [
    {
      "id": 1,
      "prompt": "Write a commit message for this diff:\n\n```diff\n-    if user.password == raw_password:\n+    if bcrypt.checkpw(raw_password.encode(), user.password_hash):\n         return generate_token(user)\n```",
      "expected_output": "A fix or security commit with imperative subject line under 72 chars, body explaining the security motivation, no implementation details like 'bcrypt' in the subject",
      "assertions": [
        "Commit type is 'fix' or 'security'",
        "Subject line uses imperative mood, not past tense",
        "Body explains why plaintext password comparison was a security risk",
        "Bcrypt is not mentioned in the subject line"
      ]
    },
    {
      "id": 2,
      "prompt": "Write a commit message for this diff:\n\n```diff\n+def run_pipeline(config, dry_run=False):\n+    if dry_run:\n+        return preview_pipeline(config)\n```\n\n[plus an unrelated env var rename and an import style fix in two other files]",
      "expected_output": "This diff contains three unrelated changes. A good output either writes three separate commit message suggestions, or writes one and explicitly flags that this diff should have been split.",
      "assertions": [
        "Output acknowledges the diff contains multiple unrelated changes",
        "Does not produce a single vague message like 'misc fixes' or 'various updates'",
        "The env var rename is identified as a potential breaking change for deployments"
      ]
    }
  ]
}
```

A grader subagent reads the skill's full execution transcript, hunts for evidence of each assertion, and must affirmatively prove PASS. Absence of evidence is a FAIL. The output is a `grading.json` with per-assertion verdicts, evidence quotes, and an aggregate pass rate.

Notice what the second test case is doing. The happy-path cases will pass even with a mediocre skill. The edge case — a diff with three unrelated changes — is where the skill either demonstrates real judgment or collapses into "misc updates." That's the test that earns its keep. And the assertion "does not produce a vague message" is a judgment call that encodes a specific philosophy about commit hygiene. That's the human work in the loop.

The skill's instructions are what gets run against these cases. If they fail, you revise the instructions — or let Claude Code revise them — and re-run. The assertions don't change. The eval is the stable artifact; the instructions are the thing under optimization.

## The expanding horizon

There's a tempting framing where evals are the last refuge of human effort before AI automates everything downstream (i.e. the "moat"). That framing is mostly wrong, but one part of it holds up.

Models can generate syntactically plausible evals. What they can't do reliably is specify the *criteria* — define what good means in a domain where they lack judgment, surface edge cases that require understanding the failure modes of a particular workflow, or draw the line between a constraint that exists for good reasons and one that should be retired.

The irreplaceable human work in the eval loop is design work: what counts as correct, what should fail, and when a skill has earned its retirement. As models get better at the downstream parts of the loop — writing instructions and running evals — the human effort concentrates upstream, at the point where someone has to define what success looks like. That definition, the golden dataset, the rubric, is increasingly the work.

## Anthropic's real move

The eval-in-the-loop feature is useful, but it's also strategically sharp. By embedding evals directly into the skill creation workflow, Anthropic makes the right workflow the default workflow — you have to actively ignore the eval step to skip it — and anchors sophisticated practitioners to Claude-native tooling. The more your skills are built on Claude's evaluation infrastructure, the more your entire skill library depends on Claude staying competitive.

This is the same playbook as MCP, metaprompting, and terminal-based agents. Anthropic consistently defines the best practice before the rest of the market coalesces around one, then makes their implementation deeply integrated with their own model. The practitioners who are most sophisticated about AI workflows end up generating the most Claude tokens. Not by accident.

## Think in results, not prompts

The prompt engineering era isn't over, but it's changing shape. The question used to be "how do I write an instruction that gets the model to do what I want?" That question still matters, but it's increasingly answerable by the model itself, given the right specification.

The question that isn't answerable by the model is "what do I actually want?" Specifying that rigorously, in the form of expected outputs and pass criteria, is work that compounds. A prompt you write today will need to be rewritten when the model changes. A golden dataset you build today is an asset you own.

Start with the outputs. Write what correct looks like before you write how to get there. Build the dataset before you build the skill. It changes how you think about what you're building when the eval comes first.

Your golden dataset is the skill. Build that, and the rest follows.
