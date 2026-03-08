---
layout: post
title: "Prompts Are Parameters"
date: 2026-03-07
---

# Prompts Are Parameters

## The Dark Ages of Prompt Engineering

There was a period, not that long ago, when prompt engineering felt like casting spells.

We gobbled these up from Arxiv papers and github repos: "Let's think step by step." "You are an expert with 20 years of
experience." "Chain of thought." "Don't make any mistakes." There was also 
the threat-based approach — some variant of "I will shoot your grandmother if you fail to
complete this task correctly". And of course, telling the LLM "You are a genius expert".

The implicit assumption underneath all of it: the prompt *is* the product, and the craft is
in writing it. 

## The Metaprompt Era

Serious practitioners figured out fairly quickly that you could use LLMs to write prompts.
This felt like cheating at first, and then it felt obvious.

Anthropic even shipped this monstrosity, an explosion in an XML factory: [metaprompt](https://github.com/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb) — a whopping 7,000 token  prompt whose sole job was to generate other prompts. Feed it a task description; receive a structured, XML-tagged, exhaustively-specified system prompt in return. The output was often genuinely good.

This became step two in the standard workflow: write a rough prompt, ask the model to improve
it, iterate. Or skip the rough draft entirely and generate from a description.

Where this lands, though, is still the same place. Prompts are still human-directed
artifacts. The loop is: you have an intuition, you express it in text, you run it, you
evaluate the output with your eyes, you adjust. Faster than the all-caps-IMPORTANT era, but
still fundamentally a manual, intuition-driven craft.

## What If You Just... Didn't Write the Prompt?

[DSPy](https://dspy.ai/) came out of Stanford around 2023 — older than most people realize,
predating a lot of the current enthusiasm for "agentic" frameworks. Its central idea is
worth sitting with for a moment, because it's actually a break from everything described
above.

The reframe: prompts are model parameters. Not human-authored text. Not the output of your
craft. Parameters — in the same sense that the weights of a neural network are parameters.
You don't write them. You optimize them.

In practice, this means you specify inputs and outputs, and the optimizer finds the path
between them. You have a summarization task? You don't write a summarization prompt. You
declare a summarization module:

```python
class Summarize(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("document -> summary")

    def forward(self, document):
        return self.generate(document=document)
```

That signature — `"document -> summary"` — is the entirety of what you specify about the
task. No instructions. No examples. No tone guidance. DSPy figures out the rest.

What happens under the hood, with MIPROv2 (the current flagship optimizer): it bootstraps
few-shot examples from your training set by running the module and filtering for cases where
the metric score is high. Then it runs Bayesian optimization over a set of candidate
instructions, scoring each one against your metric on a held-out subset of your data. The
result is a prompt — instructions plus few-shot examples — that your metric says is good.

This is real machine learning. You have a training set, a metric function, and an optimizer.
The optimizer finds parameter values (prompts) that minimize loss (maximize your metric). The
fact that "parameters" here are English sentences rather than floating point numbers is
interesting but not fundamental.

The gut-check moment is when you run it for the first time. You spent $10-15 of API calls,
20 minutes of wall time, and you got a better prompt than you would have written in two
hours. The model you're targeting wrote that prompt, scored it on examples that look like
your actual data, and optimized it toward a metric you defined. It is, in a real sense, more
yours than anything you would have written by hand.

## The DSPy Tax

DSPy does a lot. It's also a framework with opinions, and those opinions show up
as friction in ways worth naming.

**The portability philosophy.** DSPy's original bet was that prompts are model-specific — a
prompt optimized for GPT-4 is probably not optimal for Claude, and vice versa. Therefore,
you shouldn't hardcode prompts at all; you should re-optimize for each model you deploy to.
This is intellectually correct. It is also operationally heavy. Most practitioners have one
model they're targeting and want one optimized prompt. The generality isn't free.

**The inference coupling problem.** DSPy wants to be your inference runtime. `Predict`,
`ChainOfThought`, `Assert`, `Suggest` — these are runtime primitives that you're expected to
compose your pipeline from and run production inference through. Buying into DSPy fully means
running all your inference through their stack. For a research setting this is fine. For
practitioners who already have a working pipeline in their preferred framework, it's asking
you to rewrite everything.

**The artifact extraction problem.** After a successful optimization run, your improved
prompt lives inside an opaque Python object — an optimized program. To actually get the
instructions and few-shot examples out, you have to spelunk:

```python
for name, predictor in optimized_program.named_predictors():
    print(predictor.signature.instructions)
    print(predictor.demos)
```

There is no "just give me the prompt" button. The thing you just paid $10 in OpenAI calls to generate isn't
surfaced in a usable form by default.

**The data wrangling overhead.** Even feeding data in requires ceremony:

```python
trainset = [
    dspy.Example(document="...", summary="...").with_inputs("document")
    for ex in raw_data
]
```

Plain dicts won't do. You must wrap each example and specify which keys are inputs. It's not
a lot of code, but it's the kind of thing that accumulates into friction.

**The audience mismatch.** DSPy is designed for researchers and teams who want a full ML
pipeline — from raw data to deployed module, DSPy the whole way through. Most practitioners
don't need this. They have a pipeline that mostly works and want a better prompt for one
step in it. DSPy's surface area is larger than the problem.

## Daisy: DSPy as a Finishing Step

I needed something lighter, as an optimization check, a way to generate optimized prompts and move on.

The useful reframe: think of DSPy as a prompt compiler, not an inference framework. The same
way you use a compiler at build time and deploy a binary, you can use DSPy at development
time and deploy plain strings. The heavy machinery lives offline; what ships to production is
a few hundred characters of instruction text and maybe a handful of example dicts.

[Daisy](https://github.com/acesanderson/daisy) is a thin wrapper built on exactly this premise. You
give it:

- A DSPy module defining your inputs and outputs
- A labeled dataset as plain Python dicts
- A metric function
- A model string

You get back:

```python
result.predictors        # list of PredictorArtifact
artifact.instructions    # plain string — the optimized system instruction
artifact.demos           # list of dicts — few-shot examples; [] if none were generated

result.improved          # True if optimization beat the baseline
result.baseline_score    # float
result.optimized_score   # float
```

Frozen Python dataclasses. No DSPy import required at inference time.

In practice it looks like this:

```python
from daisy import optimize

result = optimize(
    module=Summarize(),
    trainset=labeled_examples,   # plain dicts, no wrapping required
    input_keys=["document"],
    metric=my_metric,
    lm="anthropic/claude-sonnet-4-6",
    auto="light",
)

# Use anywhere
system_prompt = result.predictors[0].instructions
few_shot = result.predictors[0].demos
```

One thing worth calling out: Daisy scores your original module before running optimization.
If the optimized version doesn't beat the baseline, you get the original artifacts back.
There's no scenario where you run it and end up with a worse prompt than you started with.

The intended use case is the finishing step — once your pipeline is working and you know what
good outputs look like. You've done the hard part: architecture, tool calls, retrieval,
whatever the pipeline does. Now you want to squeeze out performance on the final generation
step before you ship. That's where Daisy enters.

The README puts it plainly: "Daisy is an offline prompt compiler, not an inference
framework." The non-goals list is deliberately long. This is a narrow tool. Narrow is the
point.

## Designing Your Metric Function

The most challenging thing is defining success. The optimizer will find the prompt that maximizes whatever you
measure. That's your metric function: given an input and a prediction, it returns a float.

Three tiers, roughly in order of complexity:

**Exact match / golden dataset.** The simplest case: you have a known set of correct outputs
and you check membership. Did the model produce the right category label? The right entity?
The right routing decision? This is appropriate for classification, structured extraction,
and routing tasks where the output space is bounded. Fast to compute, cheap to call. Easy to
debug when something goes wrong.

```python
def metric(example, prediction):
    return 1.0 if prediction.label == example.label else 0.0
```

**Embedding proximity.** For generation tasks where exact match is too strict — there are
many good summaries of a document, and they won't all be identical — you can score by
semantic similarity. Embed the prediction and the reference output, compute cosine
similarity, set a threshold. You're measuring "is this in the vicinity of what we wanted"
rather than "is this exactly what we wanted." Useful middle ground; adds an embedding model
call per example.

```python
def metric(example, prediction):
    pred_vec = embed(prediction.summary)
    ref_vec = embed(example.summary)
    return cosine_similarity(pred_vec, ref_vec)
```

**LLM-as-judge.** The most flexible and most expensive option. You write a judge prompt
that defines what a good response looks like, and you score each prediction with a strong
model. High signal for open-ended tasks where embedding proximity won't capture the real
quality dimensions. This is the same methodology as
[my previous post on evals](https://acesanderson.dev/2026/03/05/the-skill-is-the-eval/);
you can import that work directly.

```python
def metric(example, prediction):
    judgment = judge_model(
        task=example.task,
        output=prediction.answer,
    )
    return judgment.score  # float in [0, 1]
```

A few notes on metric quality:

A weak metric produces a prompt that's "optimized" in a way that's worse than the original
in practice, because the optimizer found a shortcut to your proxy rather than the real
objective. A binary exact-match metric on a complex generation task will produce a prompt
that games the matching condition, not one that actually generates good output. Garbage in,
garbage out — except the garbage is plausible-looking.

Metric design is, increasingly, the real skill. The question "what does a good output look
like?" is hard. Operationalizing that into a function that can be called thousands of times
and produce meaningful signal is harder. This is what ML practitioners call "loss function
design" and it's hard work. The good news: you get to use LLMs to do it.

## Where This Goes

Anthropic has been making evals more approachable
(see [previous post](https://acesanderson.dev/2026/03/05/the-skill-is-the-eval/)). DSPy has
been making prompt optimization possible for practitioners willing to pay the DSPy tax. The
next step is the same democratization treatment applied to the optimization layer itself:
simple APIs over what's currently ML-jargon-heavy machinery. Pick your module, feed your
data, define your metric, get your prompt back.

As the models get better, the more we'll need to focus on defining success. Curious to see where state of the art lands a year from now.
