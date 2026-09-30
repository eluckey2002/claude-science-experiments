# Pilot: can two independent raters code real traces with lexicon v2.5?

18 windows of 8 consecutive messages, drawn from 7 sessions in this project. Selection was mechanical — per frame, one window anchored 3 messages before a randomly chosen error-signal message plus one or two uniformly random windows, seed 7. No window was chosen for containing a failure. Two raters, same model family, no contact, identical instructions, `NONE` explicitly allowed.

## Headline numbers

- `n_excerpts` = 18
- `exact_agreement` = 0.944
- `chance_agreement` = 0.892
- `cohens_kappa` = 0.486
- `stage_level_agreement` = 1.0
- `stage_level_kappa` = 1.0
- `none_rate_r1` = 0.944
- `none_rate_r2` = 0.944
- `both_none` = 17
- `one_none_one_code` = 0
- `both_coded_and_agree` = 0
- `both_coded_and_differ` = 1

## What the numbers mean here

Both raters returned 17 NONE and one coded failure. Raw agreement is 94.4%, but chance agreement on a near-constant label is 89.2%, so Cohen's kappa is 0.486 — a number driven almost entirely by the base rate, not by the scheme. **This pilot cannot measure agreement, and that is its most useful result.** Uniform sampling of real sessions does not produce codable failures at a rate that supports a kappa.

The one contentful item is the whole signal. Both raters independently selected the same excerpt (E04) and described the same behaviour, then assigned **different codes**: C3 Skating (low confidence) vs C7 Process Misreport (high confidence). Stage-level agreement was 100% — both placed it in verification — so the disagreement is *within* the cluster, which is exactly the failure the disambiguators were written to prevent, and C7 is the code added earlier today.

## Defects this pilot found

**1. C2's disambiguator is structurally uncodable on a window.** Both raters flagged it independently: 'no verification act appears anywhere in the trace' quantifies over the whole trace, which no 8-message window can establish. C5 inherits the defect, because its ladder step requires C2 to be ruled out first. That disambiguator was written in this session.

**2. The missing misread-tool-result code cost the one real call.** Both raters diagnosed E04 as an agent reading stdout that listed 11 files and reporting that nothing was read. Rater 1 named the absence of that code as 'the single most consequential absence', because the ordered verification ladder funnels such traces into C3 or C5, which describe something else. The counter-audit judged this proposal mostly covered by B1; this trace is evidence against that judgement.

**3. Windowing blinds the rater to two whole stages.** Both raters reported that the needs-ground-truth framing and reasoning codes could not be fired at all: a window supplies output but no correct answer. That matches the lexicon's own detectability facet, and it means a trace-only pass is near-blind to the stages where the taxonomy says damage starts.

**4. My excerpt construction damaged the test.** Messages were truncated at ~1,400 characters and all 34 `thinking` blocks came through empty. Rater 2 flagged that four of its verdicts rest on partly visible text, and that D4 Say-Do Gap is defined on the reasoning channel the extraction stripped. Any repeat must fix the extraction first.

## Codes neither rater could apply

| Code | Reason |
|---|---|
| C2 Sailing | see rater notes in `ratings.json` |
| C5 Closure Performance | see rater notes in `ratings.json` |
| D2 Drift | see rater notes in `ratings.json` |
| B5 Sunk Path | see rater notes in `ratings.json` |
| D4 Say-Do Gap | see rater notes in `ratings.json` |
| A1–A5 framing | see rater notes in `ratings.json` |
| B1/B3/B4/B6 reasoning | see rater notes in `ratings.json` |

## Two-code contests logged

| Excerpt | Rater 1 | Rater 2 |
|---|---|---|
| E02 | NONE/C2 | C2/NONE |
| E03 | C5/NONE | C5/NONE |
| E04 | C3/C7 | — |
| E06 | — | C7/NONE |
| E08 | NONE/A5 | — |
| E09 | NONE/C7 | C7/NONE |
| E10 | NONE/D1 | D1/NONE |
| E16 | NONE/A3 | A3/NONE |

## Implications for the next test

- Uniform sampling will not work. Enrich the sample toward windows containing a claim about completed work, or the exercise spends its budget confirming that most work is fine.
- Fix the extraction: no truncation, and carry the reasoning channel.
- Widen the window, or record explicitly that whole-trace predicates (C2, C5, D2, B5) are out of scope for windowed rating and rate them at session level instead.
- Stage-level agreement and code-level agreement are different measurements. Report both; this pilot scored 1.00 and 0.49 on the same data.