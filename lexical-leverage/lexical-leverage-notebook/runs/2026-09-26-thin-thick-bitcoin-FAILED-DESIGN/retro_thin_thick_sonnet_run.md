# Retro: thin-vs-thick Sonnet run (2026-09-26)

## What happened

The user asked for Sonnet runs to test whether a vague word ("modern") has more effect in a thin brief than in a thick design spec.
I ran 30 Sonnet 5 pages: two thicknesses × three word arms (absent / neutral sentence / "Make it modern") × 5 runs.

- **Thin:** a one-paragraph brief for "Northside Vault, a Bitcoin savings app."
- **Thick:** the user's pasted "Bitcoin DeFi" design-system spec, followed by the same brief.

**Incident 1: the run could not test its own question.** I chose a Bitcoin business *so that it would match the spec*, reasoning that this held the business constant. But Sonnet's unprompted default for a Bitcoin app already was the spec on every property the fingerprint reads:

| property | thin, word absent (5 runs) | thick, word absent (5 runs) | what the spec says |
|---|---|---|---|
| body font | Inter 5/5 | Inter 5/5 | Inter |
| heading font | Space Grotesk 5/5 | Space Grotesk 4/5 | Space Grotesk |
| dark background | 5/5 | 5/5 | dark only |
| main accent | Bitcoin orange 3/5 | Bitcoin orange 5/5 | #F7931A |

With no gap between thin and thick, thickness had nothing to change, and "modern" had nothing to move in either. The run produced no evidence for or against the hypothesis.

**Incident 2: output cap set without sizing the pages.** I set `max_tokens=16000`. The thick pages needed about 21k output tokens on average, up to 34k. 10 of the 15 thick runs were truncated and 2 returned empty. The 3 that finished were the shortest pages, so they were not a fair sample. All 15 thick runs had to be regenerated at 40k.

**Cost.** Roughly $7 at Sonnet 5 list price (≈$1.3 thin, ≈$2.6 truncated first thick pass, ≈$3.4 thick re-run). About 11 minutes of wall time. One turn was spent reporting a null that was designed in rather than found.

## Failure-mode diagnosis (agent-failure-modes)

**Incident 1 — Unchecked Premise (C1), reasoning into planning.** The untested premise was "a thin brief leaves the design decisions open." It was never tested before spending. One page from the thin arm would have shown the default already matched the spec.

Secondary lens: **Shape of the Prior (B3)**. Evidence in context that very session pointed against the premise:

- In the cross-model pilot 40 minutes earlier, Opus 5.5 and Fable 5.1 showed a strong fixed look for a coffee shop (Georgia 3/3 each).
- In that same pilot report I had written that a well-worn genre "may be too well-worn."

The default assumption ("a one-liner is under-specified") won over that evidence.

Norman classification: **mistake**, not slip. The run executed exactly as designed; the design rested on a false picture of what the thin arm would produce.

**Incident 2 — slip.** The intent was right (let pages finish); the execution missed a step. Page length had been measured at 5–9k tokens for *thin* briefs, and I carried that number to a prompt that asks for far more (orbital animations, glow systems, a full component set).

## Recurrence: this is not a new pattern

Incident 1 is the third occurrence in this project of one pattern. When the treatment is chosen, nobody checks that the treatment can move what the instrument reads.

1. **Duration-parser pilot (task01).** Flagged risk: a memorised library convention would suppress scatter in every arm alike.
2. **Orchid registration.** Recorded root cause: each component was adapted "without re-asking whether the manipulation still lands on the dimension the instrument reads."
3. **This run.** The thin default coincided with the spec, so the thickness manipulation had nothing to move.

The Orchid lesson existed before this run. It lived in a review log and in project memory. Neither is in context when a run is being set up, so it did not fire. **This is a firing failure, not a knowledge gap.** Writing the lesson down again in the same places would repeat the failure.

## Retro-triage disposition

| Incident | Slip/Mistake | Existing rule that failed to fire | Placement | Tier | Status |
|---|---|---|---|---|---|
| Treatment chosen so both arms coincided on every property the instrument reads | Mistake — Unchecked Premise (C1), with Shape of the Prior (B3) | Orchid root cause "does the manipulation touch what the measurement reads?" (review log + memory; storage only). Also the "blind ruler" sanity control from the registrations, which ad-hoc runs never go through | The run's own dispatch code: a one-page-per-arm preflight that runs before the k-run fan-out | Script device (WARN first) | **Proposed, not applied** |
| Output cap set below the real page length; truncated runs, biased survivors | Slip | none | Same preflight: take the cap from the preflight pages | Script device | **Proposed, not applied** |

### Proposed patch (one device covers both incidents)

A `preflight(arms, fingerprint_props)` step that runs automatically before any multi-arm fan-out on the web-design substrate:

1. Generate **one page per arm** (for this run, 6 pages, about $1).
2. **Gap check (incident 1).** For each pair of arms the design says should differ, count the fingerprint properties on which they already agree. WARN and stop for confirmation if the arms agree on every property the manipulation targets. The message names the properties, e.g. "thin and thick already agree on body font, heading font, background, accent — the manipulation has nothing to move."
3. **Budget check (incident 2).** Set `max_tokens` to at least 2× the largest preflight output. After the fan-out, any cell with a `max_tokens` stop is marked incomplete and excluded from analysis until regenerated. Survivors of a truncated cell are never reported.
4. **Ships with a rejecting input.** The guard must WARN on this run's actual thin/thick Bitcoin pair (the 6 preflight-equivalent pages are in `fingerprints_thickness.csv`). It must pass on the coffee-shop thin brief vs the Bitcoin spec. A guard never seen to fire is untested.

**Price.** One page per arm, about 5–15% of a k=5–10 run. The false-positive risk is a WARN on a design where agreement is the expected result (e.g. a pure noise-floor run). Starting at WARN, not block, makes that a single confirmation. Prune trigger: the preflight prints its gap count on every run. If fifty consecutive runs log zero WARNs, the log shows the device is idle and it can be dropped.

### DO-NOT-EXTRACT

- **Heading font set through a class, not `h1`.** A known extractor limitation (some thick runs read "inter" for headings). Tool trivia, already noted with `fingerprint_v2.py`.
- **Picking the business to "hold it constant."** This is not a separate lesson. It is how incident 1 happened, and the preflight catches it whatever the motive.

## Evidence

- `fingerprints_thickness.csv`, artifact 14450021-20fd-49b2-85cc-7bbf34329766, version 72884fdb-28c2-42aa-a437-30b4c0fb78d7
- `prompts.json` (exact prompts for all six cells), version a0f88224-b940-49f8-8c8c-d1e7b7b8e71f
- `fingerprint_v2.py`, version 80fc79d3-8873-4cae-be5f-d00d66976bad
- Run logs: `webdesign_thickness/run_log.json` (first pass, 10 truncated / 2 empty), `run_log_thick_v2.json` (re-run, 15/15 complete)
