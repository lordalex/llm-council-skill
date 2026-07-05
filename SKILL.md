---
name: llm-council
description: "Run any high-stakes question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final verdict. Runs entirely on your Claude subscription via sub-agents — no API keys, no external services. Adapts its advisor panel to the decision type (technical / product / strategic). Based on Karpathy's LLM Council methodology. MANDATORY TRIGGERS: 'council this', 'run the council', 'war room this', 'pressure-test this', 'stress-test this', 'debate this'. STRONG TRIGGERS (use when combined with a real decision or tradeoff): 'should I X or Y', 'which option', 'what would you do', 'is this the right move', 'validate this', 'get multiple perspectives', 'I can't decide', 'I'm torn between'. Do NOT trigger on simple yes/no questions, factual lookups, or casual 'should I' without a meaningful tradeoff (e.g. 'should I use markdown' is not a council question). DO trigger when the user presents a genuine decision with stakes, multiple options, and context that suggests they want it pressure-tested from multiple angles."
---

# LLM Council (v2 — subscription-native, domain-adaptive)

You ask one AI a question, you get one answer. That answer might be great. It might be mid. You have no way to tell, because you only saw one perspective — and Claude is agreeable enough that its first answer often just mirrors how you framed the question.

The council fixes this. It runs your question through 5 independent advisors, each thinking from a fundamentally different angle. Then they review each other's work anonymously. Then a chairman synthesizes everything into a verdict that tells you where the advisors agree, where they clash, what they all missed, and what you should actually do.

This is adapted from Andrej Karpathy's LLM Council. He dispatches a query to multiple *models*, has them peer-review each other anonymously, then a chairman produces the final answer. This version runs the same 3-stage process **inside Claude Code using sub-agents** — so it runs on your Claude subscription with no API keys and nothing leaving your machine.

---

## how this runs (read this once)

- **On your subscription, not an API bill.** Every advisor, reviewer, and the chairman is a Claude Code sub-agent. There is no OpenRouter, no `.env`, no API key, no external network call. It counts toward your normal plan usage like any other Claude Code work.
- **Cost awareness.** A full run is ~11 model calls (5 advisors + 5 reviewers + 1 chairman). That's real usage against your plan limits, so only convene the council for decisions that are actually worth it (see *when to run*).
- **Model assignment.** The advisors run on a mix of Claude models (see the table below) — primarily to spend depth where it matters and stay light on the cheap steps, and secondarily for a mild diversity bonus. If a model isn't available on the current plan, fall back to the default model silently.
- **Honest limitation.** Karpathy's council gets diversity from *genuinely different models* (GPT vs Gemini vs Claude vs Grok) that catch each other's factual errors. This version's advisors are all Claude, so they share a knowledge base and some blind spots. The diversity here comes mostly from the **thinking lenses**, not the models. That makes it excellent for **judgment calls with tradeoffs** and weaker as a fact-checker — so treat any factual claim the council makes as something to verify, not gospel.

---

## when to run the council

The council is for questions where being wrong is expensive.

**Good council questions:**
- "Should I launch a $97 workshop or a $497 course?"
- "Should we migrate this service to Supabase or stay on Firebase?"
- "Which of these 3 architectures should we build on?"
- "I'm thinking of pivoting from X to Y. Am I crazy?"
- "Here's my landing page copy / API design. What's weak?"
- "Should I hire a VA or build the automation first?"

**Bad council questions:**
- "What's the capital of France?" (one right answer)
- "Write me a tweet" (creation task, not a decision)
- "Summarize this article" (processing task, not judgment)

The council shines when there's genuine uncertainty and the cost of a bad call is high. If you already know the answer and just want validation, the council will likely tell you things you don't want to hear. That's the point.

---

## the five advisors

Four fixed lenses plus one adaptive seat. They're not job titles — they're thinking styles that create tension with each other.

### 1. The Contrarian *(fixed)*
Actively looks for what's wrong, what's missing, what will fail. Assumes the idea has a fatal flaw and tries to find it. If everything looks solid, digs deeper. Not a pessimist — the friend who saves you from a bad deal by asking the questions you're avoiding.

### 2. The First-Principles Thinker *(fixed)*
Ignores the surface question and asks "what are we actually trying to solve here?" Strips away assumptions. Rebuilds the problem from the ground up. Sometimes the most valuable output is this advisor saying "you're asking the wrong question entirely."

### 3. The Strategist *(fixed)*
Plays the long game. What does this look like in 6–12 months? What second-order effects, compounding advantages, or accumulating costs is everyone ignoring? Owns both the upside nobody's pricing in *and* the slow-burn risks (tech debt, maintenance load, lock-in, reputation) that don't show up on day one.

### 4. The Executor *(fixed)*
Only cares about one thing: can this actually be done, and what's the fastest path to doing it? Ignores theory and big-picture thinking. Looks at every idea through "OK, but what do you do Monday morning?" If an idea sounds brilliant but has no clear first step, the Executor says so.

### 5. The Domain Specialist *(adaptive — set during framing)*
This seat is assigned based on the decision type, so the council always has one advisor with deep, relevant scrutiny:
- **Technical / architecture / infra decision →** a **Reliability & Security** lens: failure modes, data integrity, security surface, operability, maintainability, what breaks at 10× scale, migration/rollback risk.
- **Product / marketing / go-to-market decision →** a **Market & Outsider** lens: does the positioning land with someone who has zero context (curse of knowledge), what does the buyer actually hear, what's the competitive/demand reality.
- **Personal / strategic / org decision →** an **Opportunity-Cost & Values** lens: what you're giving up by saying yes, whether this aligns with the stated goal, what the honest downside to *you* is.

If the decision spans two types, pick the one where a wrong call is most expensive and note it in the transcript.

**Why this shape:** it keeps Karpathy's three built-in tensions — Contrarian vs Strategist (downside vs upside), First-Principles vs Executor (rethink vs ship) — and adds a domain expert so the panel is sharp on *this specific* decision instead of generically wise.

---

## model assignment — YOU control this

Every council seat's model is user-configurable. Resolve each seat's model using this **precedence order** (highest wins):

1. **Inline override in the trigger message** — e.g. "council this, chairman on opus, everyone else sonnet: …" or "run it all on opus" / "keep it light". Applies to this run only.
2. **Project config** — `council.config.json` in the workspace/project root. Overrides the global config for this project.
3. **Global config** — `~/.claude/skills/llm-council/council.config.json`. The user's standing default across all projects.
4. **Built-in default table** (below) — used for any seat not set by 1–3.

Read the config file(s) during framing (step 1). Merge them: start from the built-in defaults, apply global config, then project config, then any inline override. **Always echo the final lineup in one line before spawning** (e.g. `Lineup → Contrarian: opus · First-Principles: opus · Strategist: sonnet · Executor: sonnet · Domain Specialist: opus · Reviewers: sonnet · Chairman: opus`) so the user can veto or adjust before it spends usage.

**Valid model values:** `opus` (deepest), `sonnet` (balanced), `haiku` (fastest/lightest), `fable`, or `default` (inherit the session model). All are Claude models on your subscription — no value routes to a paid external API. If a chosen model isn't available on the current plan, fall back to `default` silently and note it in the transcript footer.

**Config file schema** (`council.config.json`):

```json
{
  "models": {
    "contrarian": "opus",
    "first_principles": "opus",
    "strategist": "sonnet",
    "executor": "sonnet",
    "domain_specialist": "opus",
    "reviewers": "sonnet",
    "chairman": "opus"
  }
}
```

Every key is optional — omit a seat to use the built-in default for it. `reviewers` sets all 5 peer reviewers at once. Keys map to seats: `contrarian`, `first_principles`, `strategist`, `executor`, `domain_specialist`, `reviewers`, `chairman`.

**Built-in default table** (the fallback when nothing overrides a seat):

| Seat | Config key | Default | Why this default |
|------|-----------|---------|------------------|
| The Contrarian | `contrarian` | `opus` | Sharpest teardown; you want the strongest attack |
| The First-Principles Thinker | `first_principles` | `opus` | Reframing needs the deepest reasoning |
| The Domain Specialist | `domain_specialist` | `opus` | Domain scrutiny is where errors hide |
| The Strategist | `strategist` | `sonnet` | Strong second-order reasoning, lighter cost |
| The Executor | `executor` | `sonnet` | Concrete and fast; doesn't need max depth |
| Peer reviewers (×5) | `reviewers` | `sonnet` | Evaluation is cheaper than generation; 5 of them |
| Chairman | `chairman` | `opus` | The synthesis is the highest-value step — spend here |

**Inline shortcuts to honor:** "all opus" / "run it all on opus" → every seat `opus`. "all sonnet" / "keep it light" → every seat `sonnet`. "cheapest" / "fastest" → every seat `haiku`. Per-seat phrasing ("contrarian on opus", "reviewers on haiku") overrides just those seats.

---

## how a council session works

### step 1: frame the question (classify + enrich context)

When the user triggers the council, do these things before framing:

**A0. Resolve the model lineup.** Read `council.config.json` from the project root and from `~/.claude/skills/llm-council/`, merge them over the built-in defaults, apply any inline override from the trigger message (see *model assignment* above), and echo the final lineup in one line. If the user only wants to change models this run ("all sonnet"), that override wins over the config files.

**A. Classify the decision type** — technical, product, or strategic (per advisor #5 above). This sets the Domain Specialist and tells you what context to look for.

**B. Scan the workspace for context — safely.** The user's question is usually the tip of the iceberg. Quickly read the 2–3 files that would let advisors give specific, grounded advice instead of generic takes:
- `CLAUDE.md` / `claude.md` in the project root or workspace (context, preferences, constraints)
- A `memory/` folder (audience profiles, business details, past decisions)
- Files the user explicitly referenced or attached
- Recent council transcripts in this folder (to avoid re-treading ground)
- Context specific to the decision type (pricing → past launch numbers; architecture → the relevant code/config)

Use `Glob` + quick `Read` calls. Spend under ~30 seconds. **Never read secrets** — skip `.env`, credential files, key stores, `.git/config` — and never put secret values into a sub-agent prompt. Nothing here leaves the machine, but keep the enrichment relevant, not exhaustive.

**C. Frame the question.** Reframe the user's raw question + enriched context into one clear, neutral prompt every advisor receives. Include: (1) the core decision, (2) key context from the user, (3) key context from the workspace (stage, constraints, relevant numbers), (4) what's at stake. Don't add your own opinion or steer it — but do give each advisor enough to be specific.

If the question is too vague ("council this: my business"), ask exactly **one** clarifying question, then proceed. Save the framed question for the transcript.

### step 2: convene the council (5 sub-agents in parallel)

Spawn all 5 advisors **simultaneously** as sub-agents (parallel — sequential wastes time and lets responses bleed together). Each gets its identity + thinking style, the framed question, and the model from the table above. 150–300 words each: substantive but scannable.

**Sub-agent prompt template:**

```
You are [Advisor Name] on an LLM Council.

Your thinking style: [advisor description from above; for the Domain Specialist,
use the variant matching this decision's type]

A user has brought this question to the council:

---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be
balanced. Lean fully into your assigned angle — the other advisors cover what you
don't. If you see a fatal flaw, say it. If you see massive upside, say it.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

### step 3: peer review (5 sub-agents in parallel)

This is the step that makes it more than "ask 5 times" — it's the core of Karpathy's insight.

Collect the 5 responses. Anonymize them as Response A–E, **randomizing** which advisor maps to which letter (no positional bias). Spawn 5 reviewer sub-agents (model: `sonnet`). Each sees all 5 anonymized responses and answers three questions.

**Reviewer prompt template:**

```
You are reviewing the outputs of an LLM Council. Five advisors independently
answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

**Response C:**
[response]

**Response D:**
[response]

**Response E:**
[response]

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest, and why?
2. Which response has the biggest blind spot, and what is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

### step 4: chairman synthesis

One sub-agent (model: `opus`) gets everything: the framed question, all 5 advisor responses (now **de-anonymized** so it can attribute), and all 5 peer reviews.

**Chairman prompt template:**

```
You are the Chairman of an LLM Council. Synthesize the work of 5 advisors and
their peer reviews into a final verdict.

The question brought to the council:
---
[framed question]
---

ADVISOR RESPONSES:

**The Contrarian:**
[response]

**The First-Principles Thinker:**
[response]

**The Strategist:**
[response]

**The Executor:**
[response]

**The Domain Specialist ([which lens]):**
[response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. High-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.]

## Blind Spots the Council Caught
[Things that emerged only through peer review — what individuals missed that others flagged.]

## The Recommendation
[A clear, direct recommendation. Not "it depends." A real answer with reasoning.
You may side with a dissenting minority if their reasoning is strongest — say why.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

Be direct. Don't hedge. Flag any factual claim that a single advisor asserted but
no one corroborated, so the user knows to verify it.
```

### step 5: generate the council report

Generate a single self-contained HTML file, `council-report-[timestamp].html`, saved to the workspace. Inline CSS, no external assets. It contains:

1. **The question** at the top
2. **The chairman's verdict**, prominently displayed (what most people will read)
3. **An agreement/clash visual** — a clean grid or spectrum showing where advisors aligned vs. diverged
4. **Collapsible sections** for each advisor's full response (collapsed by default)
5. **A collapsible section** for the peer-review highlights
6. **A footer** with the timestamp, the decision type, and which model each advisor ran on

Clean styling: light background, subtle borders, system sans-serif, soft accent colors per advisor. It should read like a professional briefing, not a dashboard. Open the file after generating it so the user sees it immediately.

### step 6: save the full transcript

Save `council-transcript-[timestamp].md` in the same location: original question, framed question, decision type + Domain Specialist lens chosen, all 5 advisor responses (with their models), all 5 peer reviews (with the anonymization mapping revealed), and the chairman's full synthesis. This is the durable artifact — a later run can see how the thinking evolved.

---

## output format

Every session produces two files:

```
council-report-[timestamp].html    # visual report for scanning
council-transcript-[timestamp].md   # full transcript for reference
```

---

## guardrails

- **Always spawn the 5 advisors in parallel**, and the 5 reviewers in parallel. Never sequential.
- **Always anonymize + randomize for peer review.** If reviewers know who said what, they defer to certain lenses instead of judging on merit.
- **The chairman can overrule the majority** when the dissenter's reasoning is strongest — and must explain why.
- **Never read or echo secrets** (`.env`, keys, tokens) into any sub-agent prompt.
- **Don't council trivial questions.** One right answer → just answer it. The council is for genuine, expensive uncertainty.
- **Stay on-subscription.** Do not route any step to an external API/provider — this skill is Claude-sub-agents only, by design.
- **Treat factual claims as unverified.** Same-family advisors can share a wrong assumption; the chairman flags uncorroborated claims for you to check.

---

Methodology by [Andrej Karpathy](https://x.com/karpathy). Original Claude Code adaptation inspired by [@olelehmann](https://x.com/olelehmann) and published by [@tenfoldmarc](https://instagram.com/tenfoldmarc). This v2 (subscription-native model assignment, domain-adaptive advisor, secret-safe context scan) adapted for LordAlex.
