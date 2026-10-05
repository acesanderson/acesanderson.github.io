# Post Guideline: anthropic-certifications
Date: 2026-10-05
Status: DRAFT — pre-filled by assistant, [CONFIRM] markers = interview questions open

## Topic
I sat all four of Anthropic's Claude certifications (CCAR-F, CCAR-P, CCAO-F, CCDV-F) in
~6 weeks while already building everything they test. What they actually test, why the
practice-exam ecosystem around them is broken, and what that says about assessing AI skills.

## Angle / take [CONFIRM — A+B hybrid recommended]
The certs are better than their ecosystem. Anthropic's exams test architectural
judgement — trade-off invariants, not trivia — which is the right way to assess AI
builders. But the prep market around them is a mess (AI-generated practice exams with
broken answer keys, biostatistics questions on an architecture exam), and that gap
between "how we assess builders" and "how we sell prep to them" is a small case study
in the bigger eval problem: everyone can generate content, almost nobody can assess.

NOT a credential humblebrag. NOT a LinkedIn-style "I'm excited to announce." A
practitioner teardown with receipts — matches blog voice ("here's what I found, here's
what broke, here's what I learned").

## Narrative arc
- **Opening beat:** I passed all four Anthropic certifications in six weeks. I didn't
  need them — I'd already built an MCP framework from scratch, a RAG pipeline with
  7-model evals, an LLM-as-judge tool, an orchestration framework. The surprise isn't
  that I passed. It's what the exams turned out to be testing.
  [CONFIRM: CCDV-F pass status gates this beat — "all four" vs "three of four"]
- **Body move 1 — What they actually test:** Vocabulary mapping story. Each exam domain
  mapped to something already built: Valve → MCP tool/resource design, Conduit FSM
  loops → agentic loop/stop_reason handling, Kramer → context management, Rubric →
  structured output/evals. The exams weren't testing knowledge; they were testing
  judgement under Anthropic's vocabulary. Score-report evidence: 860/1000 on CCAR-P
  with 100% on every architecture domain and 0% on "support lifecycle phases" — the
  exam discriminates on judgement, not coverage.
- **Body move 2 — The practice-exam teardown:** One $175 exam's prep market had two
  kinds of product: (a) one practitioner's free LinkedIn-post PDF (Purcell/Hartman),
  genuinely aligned to the blueprint; (b) an AI-generated commercial course with a
  scoring engine that shifted every single-choice answer by one option letter, bundled
  case studies with 205-word stems vs the real exam's ~35, and Bonferroni corrections
  on an architecture exam. [CONFIRM: name Manifold or anonymize — refund was requested]
- **Body move 3 — Why the gap exists:** Generating assessment-shaped content is cheap
  now; building valid assessment is not. Same failure mode as the eval problem in
  production AI: LLM-as-judge without ground truth. The certs accidentally demonstrate
  what good assessment looks like (concrete scenarios, dominant-constraint reasoning,
  distractors that are wrong for architectural reasons) while the ecosystem around them
  demonstrates the opposite.
- **Closing beat:** What I'm doing with this — building the thing that should exist
  (exam-engine: clean-room, adversarial practice-exam generation with verified answer
  keys). The hardest unsolved problem in AI right now isn't generating content or
  building agents. It's assessing whether any of it works. [CONFIRM: exam-engine
  teaser — public or keep private for now]

## Key points (ordered by appearance)
1. Four certs, six weeks, passed — while already building everything they cover
2. The vocabulary-mapping insight: I knew every concept, the certs taught me Anthropic's
   names for my own systems (concrete mappings per domain)
3. Score report as evidence: 100% architecture domains, 0% lifecycle — the exam
   discriminates on judgement
4. The prep-market teardown: practitioner PDF vs AI-generated commercial course with
   broken scoring engine / off-by-one keys / wrong-altitude questions
5. The structural read: content generation is cheap, assessment is not — same failure
   mode as LLM-as-judge evals in production
6. Payoff: good assessment design principles (what Anthropic gets right) + the
   exam-engine as the forward hook

## Post type
[x] Teardown / case-study post (~1200-1500w) — [CONFIRM] fits existing "pattern post"
    length convention; could also run shorter (~800w) as a LinkedIn-first piece

## Source artifacts
### Vault notes
- CCDV-F Self-Assessment.md, CCAR-P.md, Claude Architect Foundations Certification.md,
  Final Anthropic certifications.md, Refund for Manifold AI CCAR-P.md,
  My Certifications.md, OpenAI Certifications.md
### KB
- ~/kbs/career/projects/claude-certification/notes.md — scores, domain breakdowns,
  blueprint weights, practice-exam provenance
- ~/kbs/career/projects/exam-engine/notes.md — Manifold audit findings, clean-room design
### Claude history search terms
- "Manifold CCAR-P audit", "off-by-one scoring engine", "Bonferroni", "exam-engine project"
### External references
- Anthropic cert program facts (Pearson VUE, pricing, 4-cert structure)
- OpenAI certification program (ETS/Coursera, 10M goal) — optional comparison beat

## Voice notes
Blog voice = practitioner learning in public, concrete numbers/names early, argument-
shaped ("The Skill Is the Eval" register). Avoid: credential-humblebrag, LinkedIn
announcement cadence, "excited to share." The teardown carries the positioning; never
say the positioning out loud. Deslop score at the end (CLI needs uv sync in
$SKILLS/blog first — .venv missing on this machine).
