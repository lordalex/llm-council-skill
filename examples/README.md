# Example output

A **real, unedited** run of the skill — nothing here was hand-written after the fact.

**Question councilled:** should a small SaaS (Firebase: Firestore + Auth + Cloud Functions; ~5k users; two devs, no ops team) migrate to Supabase (Postgres + RLS + Edge Functions) — now, later, or not at all?

**Run config:** every seat on `sonnet` (the `keep it light` inline override), decision type auto-classified as **technical/infra**, so the Domain Specialist was seated with the **Reliability & Security** lens.

## Files

| File | What it is |
|---|---|
| [`firebase-to-supabase-migration.transcript.md`](firebase-to-supabase-migration.transcript.md) | The full transcript: framed question, all 5 advisor responses, the anonymized peer-review round (with the A–E mapping revealed), and the chairman's synthesis. |
| [`firebase-to-supabase-migration.report.html`](firebase-to-supabase-migration.report.html) | The visual report the skill opens automatically. Download and open it in a browser — GitHub won't render HTML inline. |

## Worth noticing (what the process adds over "just ask once")

- **Five genuinely different verdicts** — Don't / Reframe the question / Migrate now / Migrate later-with-a-trigger / Migrate later-after-a-rehearsal — not five rephrasings of one answer.
- **The best insight came from the peer-review round, not any single advisor:** none of the five originally raised the "stay in one system" option (Cloud SQL / Firebase Data Connect) or weighed *Supabase's own* lock-in. The anonymized cross-review surfaced it.
- **The chairman overruled the raw vote**, siding with the minority "reframe" position because its reasoning was strongest — and **flagged a single-source factual claim** (the Firebase→Supabase auth hash compatibility bug) as *verify, don't trust*.

> Note: the sample decision is deliberately generic. This is a demonstration of the *process*, not infrastructure advice for your project.
