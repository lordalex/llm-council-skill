# LLM Council — v2 (subscription-native)

A Claude Code skill. Run any high-stakes decision through 5 AI advisors who argue, peer-review each other anonymously, and hand you a verdict — **entirely on your Claude subscription**. No API keys, no OpenRouter, nothing leaves your machine (one opt-in exception: [Expert research mode](#the-expert-seat-automatic), off by default).

Based on [Andrej Karpathy's LLM Council](https://x.com/karpathy/status/1962263486196867115); this v2 is a rework of the community skill by [@tenfoldmarc](https://github.com/tenfoldmarc/llm-council-skill).

## Why this exists — and how it compares

Three ways to get a "council" verdict, honestly compared:

| | [Karpathy's llm-council](https://github.com/karpathy/llm-council) (app) | [tenfoldmarc skill](https://github.com/tenfoldmarc/llm-council-skill) (v1) | **this skill (v2)** |
|---|---|---|---|
| Diversity source | 4 vendors' models (GPT · Gemini · Claude · Grok) — true cross-model error-catching | one Claude, 5 personas | one Claude family: 5 lenses × per-seat model mix, plus an optional research-verified Expert |
| Cost model | OpenRouter API credits, per token | Claude subscription | Claude subscription |
| Setup | Python+uv, Node+npm, API key, prepaid credits | drop 1 file | copy 3 files |
| Model control | edit `config.py` | none | 3-level per-seat control + lineup veto *before* spend |
| Advisor panel | whatever models you list | fixed, marketing-flavored | 4 fixed lenses + domain-adaptive seat + conditional Expert with bespoke persona |
| Fact-checking | strong — different vendors disagree | weak | weak by default; **strong opt-in** — research Expert tags `[verified: source]` vs `[recalled]` |
| Knows its limits | no | no | *Consult Before Acting* names the human professional to see + the exact questions to ask |
| Interactivity | web UI to browse stages | fire-and-forget | lineup veto · cross-examination · your lean challenged by the chairman |
| Output | local web-app session | basic HTML | template-driven interactive briefing (tabs, spectrum, vote tally, dark mode) + full transcript |
| Secrets | n/a (no workspace scan) | scans "any relevant file" | context scan explicitly skips `.env` / keys / tokens |
| Privacy | your query goes to 4 external providers | local | local; the single exception (Expert research) is opt-in and shown in the lineup |

**When Karpathy's original is genuinely better:** fact-heavy questions. Four different training sets catch hallucinations that five Claude lenses cannot — if you have OpenRouter credits and the question is "is this factually right?", his app is the stronger tool. **When this one is better:** judgment calls with real tradeoffs, zero marginal cost on your subscription, decisions that benefit from your workspace context, and any time you want per-seat control, an interrogable session, and a shareable artifact.

**vs. just asking Claude once:** a single answer mirrors your framing — ask "should I launch this?" and you get reasons yes; ask "is this a bad idea?" and you get reasons no. The council forces five committed positions, reviews them blind, and requires a chairman to name the disagreements instead of averaging them away.

## Install

```bash
# from this folder
mkdir -p ~/.claude/skills/llm-council
cp SKILL.md report-template.html council.config.json ~/.claude/skills/llm-council/
```

Then restart Claude Code. (Already installed if you set this up via the assistant.)

## Where to run it

This skill needs real parallel sub-agents, a workspace to read your context and write files, and a preview to open the report. That means:

| Surface | Works? | Best for |
|---|---|---|
| **Claude Code** (CLI / IDE) | ✅ full | Decisions *about a codebase you're in* — the context scan picks up the real repo + its `CLAUDE.md`. Architecture, migrations, refactors. |
| **Claude Cowork** | ✅ full | Best default for non-code decisions — strategy, pricing, product, personal calls. Same sub-agents + workspace + inline report preview; pulls your `memory/`. |
| **Claude.ai chat** | ⚠️ avoid | No real parallel sub-agents or persistent workspace — degrades to one model role-playing all five voices in a single context, which defeats the independence and anonymized peer review that are the whole point. |

Code and Cowork read the **same** `~/.claude/skills/llm-council/` install — one install serves both. Pick by where your context lives: codebase decision → Code; everything else → Cowork.

## Use

Trigger it with your question:

- `council this` · `run the council` · `pressure-test this` · `stress-test this` · `war room this` · `debate this`

```
council this: should we migrate this service off Firebase onto Supabase, or stay put? Context is in CLAUDE.md.
```

You get a visual `council-report-[timestamp].html` (opens automatically) and a full `council-transcript-[timestamp].md`. See a **real sample run** in [`examples/`](examples/).

## Usage cookbook — every pattern

```text
# ── the basics ─────────────────────────────────────────────
council this: should we migrate this service to Supabase, or stay on Firebase?
pressure-test this: my plan is to launch the beta to the waitlist next Friday.
war room this: keep the agency client or go all-in on the product?

# ── speed & cost dials ─────────────────────────────────────
council this, quick: <decision>                    # skip all checkpoints, run straight through
council this, keep it light: <decision>            # every seat on sonnet (cheapest sensible run)
council this, quick, keep it light: <decision>     # both: fast + light
council this, run it all on opus: <decision>       # maximum depth, highest usage
council this, fastest: <decision>                  # every seat on haiku

# ── per-seat model control ─────────────────────────────────
council this, chairman on opus, everyone else sonnet: <decision>
council this, contrarian and domain specialist on opus, reviewers on haiku: <decision>

# ── the Expert seat ────────────────────────────────────────
council this, with expert: <niche-domain decision>     # force-seat a drafted specialist
council this, no expert: <pure judgment call>          # never seat one
council this, with research: <fact-sensitive decision> # Expert may verify against real sources
                                                       # ⚠ sends search queries off-machine — the one exception

# ── combos that earn their keep ────────────────────────────
council this, quick, all sonnet, no expert: <cheap second opinion>
council this, with research, chairman on opus: <highest-stakes technical call>
```

**Interactive flow** (anything without `quick`): you'll get the lineup veto → after the advisors respond, the option to cross-examine any of them → the option to state your own lean before the chairman rules. Answer or skip each — they're decision points, not paperwork.

**Standing config per project** — drop a `council.config.json` next to the code:

```json
{ "models": { "reviewers": "haiku" }, "expert": "always", "expert_research": "off" }
```

**Re-councilling:** run the same question again after acting on the verdict — the skill reads previous transcripts in the folder and won't re-tread settled ground.

## Interactive sessions (default in Code / Cowork)

The council is a session, not a vending machine. Three light checkpoints — say **`quick`** in the trigger to skip them all:

1. **Lineup veto** — see seats, models, and the Expert persona *before* anything spends usage.
2. **Cross-examination** — after the advisors respond, pick any of them and ask a follow-up. Your question goes to *that same advisor with its full context intact*, so it defends its actual position. Its answers enter the peer-review round.
3. **Your lean** — before the chairman rules, optionally state your own position. The verdict must engage with it head-on: if the council agrees, it says what you're still underweighting; if it disagrees, it names the strongest reason your lean fails.

## The report

Every run fills the shipped [`report-template.html`](report-template.html) — a self-contained interactive briefing, not a wall of text:

- **Three tabs** (Verdict / The Council / Peer Review) with keyboard shortcuts `1`–`3`
- **Position spectrum** — every advisor placed on the decision axis at a glance
- **Blind-vote tally bars** — who the anonymous review ranked strongest, and whose blind spot got flagged
- Collapsible advisor cards with per-advisor colors + model chips, cross-examination threads inline
- Distinct callouts: recommendation, the one-first-step, **Consult Before Acting** (red), unverified-claim flags (amber), `[verified]`/`[recalled]` highlighting in Expert responses
- **Automatic dark mode**, print/PDF stylesheet, copy-verdict button, zero external assets — works offline forever

*(Preview: open [`examples/firebase-to-supabase-migration.report.html`](examples/firebase-to-supabase-migration.report.html) in a browser.)*

## Choose the model for each council member

Three ways, highest precedence first:

1. **Inline, per run** — say it in the trigger:
   - `council this, chairman on opus, everyone else sonnet: …`
   - `council this, contrarian and domain specialist on opus, reviewers on haiku: …`
   - shortcuts: `run it all on opus` · `keep it light` (all sonnet) · `fastest` (all haiku)
2. **Per project** — drop a `council.config.json` in the project root; overrides your global default there.
3. **Global default** — edit [`~/.claude/skills/llm-council/council.config.json`](~/.claude/skills/llm-council/council.config.json) (pre-filled). This is your standing lineup everywhere.

Config schema — every key optional, `reviewers` covers all 5 reviewers:

```json
{
  "models": {
    "contrarian": "opus",
    "first_principles": "opus",
    "strategist": "sonnet",
    "executor": "sonnet",
    "domain_specialist": "opus",
    "reviewers": "sonnet",
    "chairman": "opus",
    "expert": "opus"
  },
  "expert": "auto",
  "expert_research": "off"
}
```

Valid values: `opus` · `sonnet` · `haiku` · `fable` · `default`. All are Claude models on your subscription — nothing routes to a paid external API. The council **echoes the resolved lineup before each run** so you can veto it before it spends usage.

## The Expert seat (automatic)

Beyond the five lenses, the council can seat a **sixth chair: The Expert** — and it's fully automated. During framing, the orchestrator asks: *does this verdict hinge on facts of a specialized field, or purely on judgment?* Judgment-only questions run the classic five. If field-facts could flip the verdict (auth migration mechanics, tax/legal structure, a niche market's norms), it:

1. **Drafts a bespoke persona from your question** — e.g. "a Postgres RLS security engineer who has run three Firebase migrations" — never a canned menu, and shows it in the lineup echo before spending anything.
2. **Enters peer review blind** — reviewers never know which response is "the expert," so it wins on merit, not title.
3. **Can optionally *verify* instead of recall.** With research enabled, The Expert alone may search the web / fetch docs / read your codebase, and must tag every claim `[verified: <source>]` or `[recalled]`. The chairman weights verified claims above recalled ones and says which load-bearing facts are which.

**Research is OFF by default** — it's the one thing that would send data (search-query text) off your machine, so it never turns on silently. Enable per run with `council this, with research: …` or standing via config.

Control it like everything else:

| Config | Values | Meaning |
|---|---|---|
| `"expert"` | `auto` (default) · `always` · `never` | Whether the seat gets filled |
| `"expert_research"` | `off` (default) · `on` | Whether The Expert may verify against external sources |
| `"models": { "expert": … }` | `opus` (default) · `sonnet` · `haiku` · `fable` | The Expert's model |

Inline: `with expert` · `no expert` · `with research`.

### How model selection actually works

The `SKILL.md` doesn't set any model — the **orchestrator** (the main agent running the skill) does, by passing a `model` parameter when it spawns each advisor as a sub-agent. So there are two independent layers:

- **Session / orchestrator model** — whatever you picked in the app (e.g. Opus 4.8). Runs the framing, anonymization, and report-writing. Only your model picker changes this.
- **Council-seat models** — per-sub-agent overrides, resolved from the precedence above and passed on each spawn, *independent* of your session model.

Because they're independent, **running on Opus 4.8 and asking for Sonnet advisors works**: the orchestration stays on Opus while the 11 council sub-agents run on Sonnet. (`keep it light` / `use sonnet` changes the council, not your top-level session.) Friendly names map to current versions — `sonnet`→Sonnet 5, `opus`→Opus 4.8, `haiku`→Haiku 4.5, `fable`→Fable 5. If a model isn't on your plan it falls back to `default` and notes it in the transcript footer.

## When to use

Good: pricing, positioning, architecture, migrations, pivots, "which of these N", "am I crazy". Skip: factual lookups, pure creation ("write me a tweet"), summaries, or validation-seeking when you already know the answer.

## Caveats — the honest list

1. **Persona diversity ≠ model diversity.** All advisors are Claude; they share a knowledge base and can share a wrong assumption. The structure catches reasoning gaps well and factual errors poorly. When facts are load-bearing, add `with research`.
2. **A full run is real usage** — 11–13 sub-agent calls against your plan limits (~2–4 minutes). Don't council trivia; that's what the trigger guards are for.
3. **Research mode is the one privacy exception.** It sends search-query text (derived from your question) off your machine. It is off by default, never turns on silently, and the lineup echo shows `(research on)` before anything spends.
4. **The context scan reads your files.** `CLAUDE.md`, `memory/`, referenced files go into sub-agent prompts (locally). It skips `.env`/keys/tokens by rule — but keep genuinely sensitive notes out of scanned folders.
5. **A confident verdict can still be wrong.** The chairman flags uncorroborated claims, but it can't catch what all six voices believe incorrectly. For high-stakes calls, read the transcript, not just the verdict.
6. **The chairman may overrule the majority** when a dissenter's reasoning is strongest. That's a feature — but it means the verdict isn't a vote count; check its stated reasoning.
7. **Claude.ai chat is not supported.** No true parallel sub-agents there — it degrades to one voice doing impressions. Use Code or Cowork.
8. **Files are written to your workspace** and the report auto-opens. Outputs match `council-report-*` / `council-transcript-*`; add those patterns to `.gitignore` in repos where you run it (this repo ships them).
9. **Model names are aliases** (`opus`, `sonnet`, `haiku`, `fable`) resolving to current versions; anything unavailable on your plan silently falls back to `default` and is noted in the report footer.
10. **Trigger phrases can misfire** in rare edge cases. When you definitely want a council, say `council this:` explicitly.

## Design decisions (and why)

The choices behind v2, so future contributors don't relitigate them blind:

| Decision | Choice | Why |
|---|---|---|
| Runtime | Subscription-only; never routes to external LLM APIs | Predictable cost was the point — the original app burns prepaid API credits per query |
| Expert research | **Off by default**, opt-in per run or config | Preserves "nothing leaves your machine" unless you explicitly trade it for verification |
| Expert seating | `auto` — the orchestrator decides per question | Zero user burden; seats only when field-facts could flip the verdict |
| Human escalation | *Consult Before Acting* included, **rare by design** | A council that says "see a professional" on every run trains you to ignore it |
| Name | Kept `llm-council` (`war-room` was considered) | Karpathy made it a searchable term; the honesty about lenses-vs-models lives in the docs instead |
| Interactivity | On by default; `quick` opt-out | A council should be interrogable; the escape hatch keeps automation/headless use possible |
| Report | Shipped template, tokens filled per run | A deterministic rich interface beats per-run design improvisation |
| Examples | Real runs, unedited | You should judge actual output, not marketing |
| Deferred | "Include me" blind mode, rebuttal rounds | Good ideas awaiting a real need — PRs welcome |

## Credit

Methodology: Andrej Karpathy. Original Claude Code adaptation: @olelehmann / @tenfoldmarc. v2 rework: LordAlex.

MIT.
