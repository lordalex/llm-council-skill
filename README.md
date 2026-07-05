# LLM Council — v2 (subscription-native)

A Claude Code skill. Run any high-stakes decision through 5 AI advisors who argue, peer-review each other anonymously, and hand you a verdict — **entirely on your Claude subscription**. No API keys, no OpenRouter, nothing leaves your machine.

Based on [Andrej Karpathy's LLM Council](https://x.com/karpathy/status/1962263486196867115); this v2 is a rework of the community skill by [@tenfoldmarc](https://github.com/tenfoldmarc/llm-council-skill).

## Why v2

| | tenfoldmarc v1 | this v2 |
|---|---|---|
| Runs on | Claude subscription (sub-agents) | Claude subscription (sub-agents) |
| Model diversity | all one model | mix of `opus`/`sonnet` per role, in-family only (stays on subscription) |
| Advisor panel | fixed, marketing-flavored | 4 fixed + 1 **domain-adaptive** seat (technical / product / strategic) |
| Technical decisions | weak (no eng lens) | Reliability & Security lens auto-added for technical calls |
| Secrets | scans "any relevant file" | explicitly skips `.env` / keys / tokens |
| Honesty | sold as full "council" | states plainly that same-family advisors share blind spots — verify facts |

The one honest caveat, kept front-and-center: Karpathy's council gets its power from *genuinely different models* catching each other's factual errors. Every advisor here is Claude, so the diversity comes from the **thinking lenses**, not the models. Great for judgment calls with tradeoffs; not a fact-checker.

## Install

```bash
# from this folder
mkdir -p ~/.claude/skills/llm-council
cp SKILL.md ~/.claude/skills/llm-council/SKILL.md
```

Then restart Claude Code. (Already installed if you set this up via the assistant.)

## Use

Trigger it with your question:

- `council this` · `run the council` · `pressure-test this` · `stress-test this` · `war room this` · `debate this`

```
council this: should we migrate this service off Firebase onto Supabase, or stay put? Context is in CLAUDE.md.
```

You get a visual `council-report-[timestamp].html` (opens automatically) and a full `council-transcript-[timestamp].md`.

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
    "chairman": "opus"
  }
}
```

Valid values: `opus` · `sonnet` · `haiku` · `fable` · `default`. All are Claude models on your subscription — nothing routes to a paid external API. The council **echoes the resolved lineup before each run** so you can veto it before it spends usage.

## When to use

Good: pricing, positioning, architecture, migrations, pivots, "which of these N", "am I crazy". Skip: factual lookups, pure creation ("write me a tweet"), summaries, or validation-seeking when you already know the answer.

## Credit

Methodology: Andrej Karpathy. Original Claude Code adaptation: @olelehmann / @tenfoldmarc. v2 rework: LordAlex.

MIT.
