# LLM Council Transcript

**Timestamp:** 2026-07-05 08:00:37
**Decision type:** technical / infrastructure → Domain Specialist seated as **Reliability & Security**
**Model lineup (inline override "keep it light"):** every seat on `sonnet` — Contrarian, First-Principles, Strategist, Executor, Domain Specialist, Reviewers ×5, Chairman.

---

## Original question

> council this: We run a small SaaS backend currently on Firebase (Firestore + Auth + Cloud Functions), ~5k users and growing steadily. We're weighing migrating to Supabase (Postgres + Row Level Security + Edge Functions) for relational queries and more predictable cost, versus staying on Firebase. We have no dedicated ops/DevOps team — just two full-stack developers. Should we migrate now, migrate later, or not at all?

## Framed question (given to all advisors)

> DECISION: Should a small SaaS company migrate its backend from Firebase to Supabase now, migrate later, or not at all?
>
> CONTEXT: Current stack Firebase (Firestore NoSQL, Firebase Auth, Cloud Functions). ~5,000 users, growing steadily. Two full-stack developers, NO dedicated ops/DevOps team. Motivation: relational queries (Postgres) + more predictable/lower cost. Target: Postgres + RLS + Edge Functions. Options: (a) migrate now, (b) migrate later once larger/better-resourced, (c) stay on Firebase.
>
> AT STAKE: Migrating a live production database + auth for 5k users with two devs and no ops carries real downtime/data-integrity risk and weeks of diverted eng time. Getting it wrong = data loss, auth breakage, stalled roadmap. Staying wrong = escalating cost and query pain that compounds with growth.

---

## Stage 1 — Advisor responses

### The Contrarian (`sonnet`)
"Migrate later once bigger" is the trap — bigger is worse, not better. Every input to migration difficulty gets strictly harder with scale: more write traffic = longer unsafe cutover window; more data = longer backfill; more features on Firestore's document model = more denormalized data to reshape (the actual hard part). "Better-resourced later" is unearned — no funding event, no headcount plan; "later" is a wish. Companies that defer infra migrations under growth do them under pain at 3x cost after an incident. Also unquestioned: will Postgres/RLS actually solve the problem? RLS with two devs writing their own policies is a minefield — silent data leaks from a missed policy are worse than a bad NoSQL query because invisible until a breach. Edge Functions aren't drop-in for Cloud Functions. This isn't "swap the database," it's "rewrite the backend," sized like a data migration. Fatal flaw: two devs, no ops, doing a live auth+data migration for money/convenience — not because Firebase is failing — means the risk-adjusted payoff is negative unless current pain is already acute.

### The First-Principles Thinker (`sonnet`)
What are we actually solving for? Not "Firebase vs Supabase." The stated pain is "relational queries and predictable cost" — two different problems in one trenchcoat, and migrating the entire backend is disproportionate to both. Relational queries: you don't need to move off Firebase — run Postgres as a read-side companion, sync the subset that needs joins/aggregation via Cloud Functions or CDC, and query that. Relational power without touching Auth or the write path, no cutover weekend — a two-week project, not two quarters. Predictable cost: almost never a migration problem, it's a query-pattern problem (N+1 reads, unbounded listeners, whole-collection fetches). Profile the actual cost drivers first; Supabase at the wrong access pattern gets expensive too. Real question nobody asked: is "we want relational queries" a genuine bottleneck, or main-character syndrome — two devs who'd rather work in Postgres? Legitimate preference, but name it as taste, not necessity. The decision isn't (a)/(b)/(c): add a reversible Postgres companion now, fix the cost driver now, defer the irreversible Auth+Firestore migration indefinitely — the companion may give 90% of the want at 5% of the risk.

### The Strategist (`sonnet`)
Six to twelve months out, "migrate now" looks different depending on whether you count cost paid vs cost accrued. The cost of staying isn't flat, it's compounding: every feature built on Firestore's document model becomes migration debt with interest. At 5k users you migrate a database; at 25k with three more surfaces built on Firestore's assumptions, you migrate a database AND re-architect half the data-access layer under load, with customers noticing downtime. "Migrate later once bigger" sounds cautious but guarantees the operation becomes higher-stakes; headcount grows slower than migration surface area. Underpriced upside: RLS+Postgres isn't just "better queries," it's an ops-load reduction — Firebase's rules DSL and Functions observability demand more bespoke tribal knowledge than a two-person team should carry; standard SQL/Postgres tooling and a hireable talent pool is the lower-maintenance path at year two. The real second-order risk is doing it now badly with no rollback plan. So it's not "now vs later" on the calendar, it's "before or after the data model ossifies." Do it now — but scope it as dual-write-and-verify over weeks, not a cutover weekend.

### The Executor (`sonnet`)
Two devs, no ops team, live production database — that's the whole decision. Migrate now: no. It requires dual-write/export scripts for every collection, a NoSQL-to-relational schema redesign, rewriting every Cloud Function as an Edge Function, re-implementing every Auth flow against Supabase Auth, writing and testing RLS policies so they don't leak, and a cutover+rollback plan. For two devs who own the roadmap, that's 6–10 weeks of near-total roadmap freeze minimum. No ops means when RLS breaks at 2am, one person fixes it alone. Stay forever: also no — the pain compounds. The only executable path is migrate later, but "later" needs a trigger not a vibe: pick a number (20k users, $X/month spend, or a third engineer). Until then do the cheap prep: stop adding Firestore collections that'll need joins, start a throwaway Supabase side-project so the team learns Postgres/RLS/Edge Functions, track actual monthly Firebase cost. Monday: write the trigger number down, open a free Supabase project for an internal tool. Anything more ambitious with this headcount is roadmap suicide.

### The Domain Specialist — Reliability & Security (`sonnet`)
Migrating live production auth AND a live production database at once, with two generalists and zero ops bench, is the single highest-risk combination here — re-sequence first. Auth is the landmine: Firebase Auth password hashes use a scrypt variant with a secret hash key not exported by default (request via the Admin SDK), with a modified-scrypt parameter format Supabase's importer has historically had compatibility bugs with. Get it slightly wrong and users silently can't log in — failed hash verification doesn't throw, it falls through to "wrong password." Test the full hash path against a copy of prod first; never big-bang auth — run dual-auth (verify Firebase first, fall back to migrated record, re-hash on login) for at least one full cycle. Data: Firestore's denormalized docs (arrays, maps, subcollections) don't map cleanly to tables — design the schema, don't script a 1:1 dump. RLS isn't Firestore rules with new syntax: a missing policy fails safe (no access), but forgetting to enable RLS on a table at all fails catastrophically OPEN to anyone with the anon key. Use dual-write + reconciliation + feature-flagged reads and a rehearsed rollback. Verdict: migrate later, only after a written runbook, hash-export test, and rollback rehearsal.

---

## Stage 2 — Peer review

**Anonymization mapping (revealed):** Response A = Strategist · B = Executor · C = Contrarian · D = Domain Specialist · E = First-Principles.

**Tally:** Strongest → E (First-Principles) 4 votes, D (Domain Specialist) 1 vote. Biggest blind spot → A (Strategist) 5 votes (unanimous).

- **Reviewer 1:** Strongest D (mechanism-level failure detail). Blind spot A (hand-waves execution as a footnote). Missed by all: nobody quantified current pain/cost at 5k vs 25k; Supabase scaling/lock-in symmetry; compliance/data-residency.
- **Reviewer 2:** Strongest E (questions the frame; reversible companion fits two-dev/no-ops). Blind spot A. Missed: Postgres-without-leaving-Firebase (Cloud SQL / Firebase Data Connect); Supabase exit-cost symmetry.
- **Reviewer 3:** Strongest E (reframes; challenges the premise). Blind spot A. Missed: Supabase maturity/vendor risk; reference-customer war stories; a staged pilot on a low-stakes in-production feature; compliance.
- **Reviewer 4:** Strongest E (most decision-useful; "main-character syndrome" challenge); D technically deepest. Blind spot A. Missed: quantify current pain; Supabase ops risks (connection pooling, single-region failover); a partial-migration unwind/exit plan.
- **Reviewer 5:** Strongest E (only one questioning the answer space). Blind spot A. Missed: Supabase's own operational risk + RLS as an ongoing tax; concrete cost comparison at 5k vs 25k; "what does being stuck with Supabase later look like."

---

## Stage 3 — Chairman synthesis (`sonnet`)

### Where the Council Agrees
Full big-bang migration now is off the table (two devs, no ops can't safely run a simultaneous live auth+data cutover — the one point with zero daylight). "Do nothing forever" is also rejected by everyone (debt compounds). Auth and data are different risk classes and should not move on the same timeline. Some version of incremental/reversible execution beats a cutover.

### Where the Council Clashes
1. **Is this even a database problem?** First-Principles' reframe (companion Postgres, never touch Auth/RLS-everywhere) vs. Strategist/Contrarian accepting Postgres as the destination and arguing only timing.
2. **Urgency vs. capacity.** Strategist optimizes total lifetime cost ("do it now"); Executor/Contrarian optimize probability of a catastrophic incident ("capacity is the binding constraint"). Every peer review flagged the pro-now case as under-defended.
3. **RLS as feature vs. tax.** Ops-load reduction (Strategist) vs. permanent easy-to-get-silently-wrong burden (Contrarian, Domain Specialist). Unresolved.

### Blind Spots the Council Caught
No one quantified the actual pain (no current cost/latency number). The "stay in one system" option (Cloud SQL / Firebase Data Connect) was invisible to all five advisors — only peer review surfaced it. Supabase's own exit cost and operational risk went unexamined. No one proposed a live low-stakes pilot or a reference-customer conversation. Compliance/data residency was missing throughout.

**Flag for verification (asserted by one advisor, corroborated by none):** the Domain Specialist's claim that Supabase's importer has had *specific compatibility bugs* with Firebase Auth's modified-scrypt hash format causing silent login failures. Plausible and consistent with how Firebase Auth's export works in general, but verify against current Supabase docs/changelog before treating it as fact.

### The Recommendation
Don't migrate now. Don't commit to a vague "later." Don't treat this as a two-option choice. The First-Principles reframe is the strongest reasoning (and every peer review independently ranked it highest). Stand up a Postgres companion (even boring Cloud SQL / Firebase Data Connect) fed by CDC/Cloud Functions to get relational queries in ~2 weeks with a fully reversible blast radius — production Auth and the write path never move. Treat "predictable cost" as a measurement problem first. Escalate to a full Auth+data migration only if the companion hits a real wall, a third engineer/ops capacity exists, and the auth-hash path has been tested end-to-end against a prod copy. This gives the Strategist's urgency without the execution risk every reviewer flagged.

### The One Thing to Do First
Before writing any migration code: pull the last three months of Firebase billing broken down by service (Firestore reads/writes, Functions invocations, bandwidth) and put a real number next to "predictable cost" — that number decides whether you need a companion database in two weeks or nothing at all.

---

*Generated by LLM Council v2 — runs on your Claude subscription. Methodology: Andrej Karpathy. This run: all seats on `sonnet` ("keep it light" override).*
