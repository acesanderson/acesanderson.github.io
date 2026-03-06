# Research: Anthropic Skills v2 + Evals as AI Engineering Practice
Date: 2026-03-05
Source: Perplexity sonar-pro (10 queries)
Post target: "The Skill Is the Eval"

---

## Round 1: Skills v2 Overview and Industry Context

### Skills v2: What Changed

| Dimension | Skills v1 | Skills v2 |
|-----------|-----------|-----------|
| Testing | Manual, external | Integrated evals: prompts + expected outputs + pass criteria, auto-runs in 6 parallel agents |
| A/B Testing | Informal | Blind comparators: 3 runs with skill, 3 without, isolated contexts, quantified deltas |
| Trigger Reliability | Static descriptions | Auto-optimized: tests description against 5 sample prompts, iterates until accuracy improves |
| Regression Detection | None | Benchmarks track performance across model updates |
| Skill Lifecycle | Unclear when to deprecate | Data-driven: determines if base model has caught up |

Two skill types formalized:
- **Capability uplift** — fills gaps the base model lacks. Has a natural retirement date as model improves. Evals ask: does this still work? Is it still needed?
- **Encoded preference** — enforces org workflows or constraints. Never retires. Evals ask: is the constraint being applied correctly?

Concrete mechanism: 6 parallel sub-agents (executor, grader, comparator). Trigger description optimization iterates up to 5 times. Output: HTML report with pass/fail %, latency, token cost.

Notable: the Skill Creator tool recursively improved its own trigger descriptions — Anthropic dogfooding agentic loops on their own tooling.

No external analyst coverage as of March 6, 2026 — narrative is entirely Anthropic-driven.

### Skills v2 vs LLMOps Tools

Anthropic's edge: **zero infrastructure** — no SDK, no data pipelines, no dashboards. Write evals conversationally inside Claude, get an HTML report.

| Tool | Gap vs. Anthropic |
|------|-------------------|
| LangSmith | Requires SDK integration and data pipelines; good for production tracing |
| MLflow | Too ML-training-centric; lacks multi-agent isolation or skill-specific triggers |
| W&B | Requires manual metric definition; no native skill A/B |
| PromptLayer | Prompt-focused; misses multi-agent parallelism and regression tracking |

Anthropic wins on iteration speed and friction. Loses on production observability and multi-provider portability.

### Agent Skills as Production Infrastructure

Operational implications:
- Version control + rollback: regression testing catches model-update breaks, rollback in <5min
- SLOs: 99.5% task completion, <30s latency targets
- Per-skill token/cost tracking enables ROI analysis
- Goldman Sachs attributed 17% reconciliation throughput gains to specific agent skills

Org shift: prompt engineers → agent reliability engineers. Only 10% of AI pilots reach production without infra; with it, Goldman/Salesforce hit 80%+.

### Competitive Landscape

No competitor matches Anthropic's in-model, zero-friction parallel benchmarking:
- OpenAI: no native skill eval — teams use LangSmith externally
- Google/Vertex: generic eval, not skill-specific
- Open source (Langfuse, Deepchecks): self-hosting wins, but manual setup, no blind A/B

### Model Upgrades and Skill Regression Risk

**Key insight**: skills can actively *harm* performance on newer models. If the base model improves and a capability uplift skill's instructions become redundant or prescriptive, the skill over-constrains behavior the model handles better natively — a regression invisible to absolute benchmarks.

You need *relative* improvement measurement across model versions, not just absolute pass rates.

Supporting data: self-generated skills performed *worse* than no skills (−1.3%) — models cannot self-assess when their capability has outpaced a skill's assumptions.

Skills v2 regression tooling is within-model only. Cross-model stability is the unsolved problem.

The "sweet spot" of 2–3 focused skills per task yielding 18.6pp improvement assumes a specific model capability baseline — fragile as models improve.

---

## Round 2: Evals as AI Engineering Practice

### Eval Mastery for AI Engineers (2026)

**Framework landscape:**
- **DeepEval** — open source, 14+ metrics (hallucination, faithfulness, G-Eval, bias/toxicity), pytest integration, synthetic dataset generation. The one to learn first.
- **Braintrust** — production debugging, CI/GitHub Actions integration, token-tracing. Best for prod teams.
- **RAGAS** — RAG-specific metrics (faithfulness, relevancy, recall/precision). Free.
- **Galileo** — ChainPoll consensus, hallucination detection.
- **Maxim** — multi-step agent testing and simulation.
- Others: LangSmith (tracking), MLflow (QA evals), Comet Opik (self-hosted), Fiddler (guardrails).

**Junior vs. senior divide:**
- Junior: runs prebuilt metrics, basic RAG evals, dashboard visualization
- Senior: custom pipelines blending code-based + LLM-as-judge; production observability (drift, cost tracking); agentic evals (multi-step scenarios); explains failures; treats evals as unit tests in CI/CD

Mastery = eval-driven development: iterate prompts and models *from* eval feedback, not from intuition.

### LLM-as-Judge: Mechanics and Failure Modes

The dominant eval mechanism for subjective tasks. Scales rapidly, aligns with human ratings when prompted well.

**Known failure modes:**
- **Position bias** — favors first-listed option in pairwise comparisons (~10–20% skew). Fix: randomize order.
- **Verbosity bias** — longer responses score higher regardless of quality. Fix: explicitly instruct to penalize length.
- **Contamination/recency bias** — models trained on eval datasets inflate scores. Fix: held-out data or older judge models.
- **Variance/instability** — 0.1–0.3 std dev across runs. Fix: majority vote (5–20 runs) or multi-judge ensemble.
- **Scaling laws** — GPT-3.5 diverges significantly from humans; GPT-4/Opus-class correlate at Pearson r=0.9+.

**Best practices:**
- Pairwise > pointwise (higher human correlation)
- Structured JSON output: `{"score": 4, "reason": "..."}`
- Multi-judge ensemble (e.g., GPT-4 + Claude averaged)
- Calibrate against human gold standards; target 90%+ agreement
- Chain-of-thought with explicit criteria in judge prompt

### Golden Datasets: Building and Maintaining

**Standard pipeline: silver → gold**
1. LLM synthesizes candidate examples from production logs or document chunks (Q&A pairs from chunked docs)
2. Humans/SMEs review and promote to gold
3. Version with provenance tags and rubrics attached to each expected output

**What makes a good golden standard:**
- Production-faithful: mirrors real usage diversity
- Diverse: edge cases, adversarial, multiple languages/complexities
- Decontaminated: no training set overlap (check via embedding similarity)
- Rubric-attached: not just expected output, but *why* it's correct and what partial credit looks like

**Preventing label rot:**
- Continuous production monitoring feeding new failures in
- Quarterly human audits + moderator calibration quizzes
- Versioned datasets with provenance tags
- Automated evals with alerts on score drift

**Scaling ground truth:**
- LLM synthesis from doc chunks (fastest, lowest cost)
- Agent simulation: run trajectories, eval and promote to gold
- Human+AI hybrid: silver → gold via SME review

### DSPy and Eval-Driven Development

DSPy makes expected outputs the primary artifact explicitly. The loop:
1. Collect 30–300 input-output pairs
2. Define a metric (exact match, SemanticF1, etc.)
3. Optimizer (MIPROv2, BootstrapFewShot) auto-generates prompts/few-shots to maximize metric on val set

The prompt becomes the *output* of the process, not the input.

| | Traditional Prompt Engineering | DSPy |
|---|---|---|
| Starting point | Manual prompt guess | Input-output dataset + metric |
| Iteration driver | Human intuition | Optimizer + val metrics |
| Primary artifact | Prompt as code | Expected outputs as ground truth |
| Scalability | Brittle for complexity | Handles few-shots/instructions/weights |

Real result: RAG pipeline 24% → 51% accuracy from DSPy optimization.

**Connection to Skills v2**: Skills v2's regression benchmarking is a constrained version of exactly this. The skill's golden dataset IS the skill's core — the instructions are what gets optimized against it.

### Evals as Durable Human Work ("Expanding Horizon")

Models can generate syntactically plausible evals but fail on:
- **Adversarial edge cases** — they optimize for patterns they already know, not unknown failure modes
- **Distributional shift** — overfit benchmarks, fail production deployment
- **Cultural/ethical/domain judgment** — criteria that require genuine contextual understanding

Human irreplaceability concentrates at:
- **Criteria definition**: what counts as good output, what partial credit looks like
- **Edge case specification**: what should fail and why
- **Governance**: who signs off, audit trails, compliance

Key stats:
- 44% of organizations report inaccuracy as their top gen AI risk
- Only 18% have AI governance councils
- The eval gap is organizational, not just technical

Leading developers (OpenAI, Google, Anthropic) use disparate responsible AI benchmarks — no standardization, which humans must bridge.

---

## Key Quotes / Framings Worth Preserving

- "Treat evals as unit tests in CI/CD" — the senior practitioner mental model
- "Silver → gold" — the standard pipeline for building golden datasets
- Skills v2 blind comparators: Anthropic's answer to verbosity bias and position bias in their own eval loop
- "The prompt becomes the output of the process, not the input" — the DSPy inversion, applicable to Skills v2
- 44% inaccuracy risk / 18% governance councils — the organizational gap framing

---

## Citations (Selected)

- https://www.braintrust.dev/articles/best-ai-evaluation-tools-2026
- https://futureagi.substack.com/p/llm-evaluation-frameworks-metrics
- https://eugeneyan.com/writing/llm-evaluators/
- https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/
- https://arize.com/resource/golden-dataset/
- https://deepeval.com/docs/evaluation-datasets
- https://dspy.ai/learn/optimization/overview/
- https://thedataquarry.com/blog/learning-dspy-3-working-with-optimizers
- https://hai.stanford.edu/ai-index/2024-ai-index-report
- https://softwareengineeringdaily.com/2025/06/10/the-challenge-of-ai-model-evaluations-with-ankur-goyal/
