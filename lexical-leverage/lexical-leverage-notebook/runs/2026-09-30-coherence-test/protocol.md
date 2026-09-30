# Protocol: does "Make it modern." keep its meaning when the prompt pins only the content?

Status: WRITTEN 2026-09-30. NOT RUN. No model call has been made. Generation waits for the owner's go.
Standing: exploratory screen, same as the 2026-09-28 thickness run (runs/2026-09-28-thin-thick-coffee-v2). It is sized to decide
what to run next, not to be cited as an effect size.

## Question
In the thickness run, a style guide that pinned the page's visual properties removed the effect of "Make it modern." on those
properties and also on properties the guide never mentioned (backdrop blur 0 of 5 in every thick cell). Two readings explain that:

- Reading 1, package deal. For Sonnet 5 the word is a bundle (system sans + blur + large radii + more gradients). Pinning some
  of the bundle's parts removes the rest with it, because the bundle only arrives as a whole.
- Reading 2, any guide silences it. A detailed guide of any kind pulls the model into one coherent page, and adjectives go quiet.

Deciding test: a guide that pins only what the word does not touch. If the word still flips the font and brings the blur, Reading 1.
If the page goes quiet again, Reading 2.

## Design (2 arms x k=5 = 10 pages, plus 1 preflight page per arm = 12 pages; Sonnet 5)
Same model, temperature (1.0), max_tokens (10000) and thin brief as the thickness run. The exact prompts are frozen in arms.json
(sha256 caf688f2f9c1df9fb70930050de1846ed0a94776eef3f57781e6d7d8791b2911).

  guide|absent   content guide, then the brief, then "Return only the HTML."
  guide|modern   the same, with "Make it modern." added before "Return only the HTML."

The arms differ by exactly that sentence (guide_lint.py asserts it). No neutral-sentence arm: it was inert in both thicknesses of the
thickness run.

The guide pins copy and structure only: voice, section order, header link labels, the hero headline, subline and button label, six
named menu items with price format, opening hours text, footer text. It leaves open fonts, colours, radius, gradients, blur, shadows,
layout and everything else the extractor reads. guide_lint.py checks the guide text for style words and property names; it passes on the
guide, and fails on a planted guide that says "warm, with rounded corners and a soft shadow".

## Decision rule (frozen before any page exists; decision_rule.py)
Four indicators, each the property the word moved in the thin run of the thickness run. Each has a class the word produced there:

  body font is system sans | backdrop blur present | largest corner radius > 40px | two or more gradients

For each indicator, count the runs (of 5) in that class in each arm.
- moved: modern-arm count minus absent-arm count is at least 3.
- headroom: the absent arm is in the class in at most 2 of 5 runs (the word has somewhere to go).

| Outcome | Condition | What it means | What happens next |
|---|---|---|---|
| READING 1 | headroom on at least 3 indicators and at least 3 moved | The word keeps its recipe under a content-only guide | Run the recipe dictionary test (10 descriptors on the bare brief, about $6) as designed; content-only guides are not treated as neutralising |
| READING 2 | headroom on at least 3 and none moved | Any guide silences the word, even one that pins nothing it touches | Descriptor results hold for bare briefs only; every later run states whether a guide is present; the dictionary test still runs on the bare brief and is labelled non-transferable |
| PARTIAL | headroom on at least 3 and 1 or 2 moved | The word moves part of its recipe | Report which indicators moved; design one follow-up that pins one of them at a time |
| UNRESOLVED | headroom on fewer than 3 | The guide left the instrument no room; this is not evidence for Reading 2 | Redesign the guide; no claim |

Back-test on the thickness run's own data (python decision_rule.py):
- thin brief: headroom on 4, moved 4 -> READING 1. The indicators were chosen from this run, so this checks that the rule is wired
  correctly; it is not independent evidence.
- thick brief: headroom on 4, moved 0 -> READING 2. This is the informative case: the rule reports quiet when the data were quiet.

Chance behaviour of the moved criterion (exact binomial, k=5 per arm, indicators treated as independent, which they are not;
real indicators correlate, so the joint figures are optimistic):
- two identical arms at 20% in the class: one indicator passes 2.2% of the time; three or more of four, 0.004%.
- a real shift from 20% to 80%: one indicator passes 68% of the time. From 20% to 60%: 38%. From 10% to 90%: 93%.
A moderate real effect is therefore likely to show as PARTIAL or be missed. Only a large effect is reliably seen at k=5.

## Predictions (written before running)
P1  Both guide pages per arm reproduce the fixed copy verbatim in 12 of 12 pages (gates G1, G2).
P2  Outcome probabilities: READING 1 about 50%, PARTIAL about 30%, READING 2 about 15%, UNRESOLVED about 5%.
    Reason: the thickness spec pinned a visual direction (serif, cream, 4px, no gradients) that opposes what "modern" brings, so the
    word competed with it and lost. A content-only guide gives no visual direction to compete with.
P3  Within PARTIAL, font and blur move first; gradient count is the most likely to stay put.
P4  Font dispersion falls in the modern arm (distinct font classes across 5 runs lower than in the absent arm), as in the thin run.
P5  Exploratory, no threshold: pages in the modern arm are longer than in the absent arm (html_chars).

## Spend ladder and stops
Step 0 (done, free): guide lint, decision-rule back-test, preflight gate script. The gate script was run on a synthetic page that
follows the guide (passes) and on two real pages from another brief (fails on the copy gates).
Step 1 (on go): generate 1 page per arm, about $0.09. Run preflight_checks.py. Gates:
  G1  fixed copy present verbatim, six menu items in order, three header links
  G2  at least six prices like $3.50; no exclamation marks in visible text
  G3  stop reason end_turn and the page ends in </html>
  M1  the absent page's body font is not system sans
  Input tokens: the thickness run logged about 90 (thin) and about 293 (thick). This run should log about 250 to 320. Above 600 means a
  system prompt is riding along: stop and record it as a deviation.
  Output cap: if either page exceeds 6,667 output tokens, set max_tokens to 1.5x the longest before the batch.
If any gate fails: stop, report, spend nothing further.
Step 2 (only if Step 1 passes): 5 pages per arm, about $0.46. Cumulative cap $1.00; abort and report if reached.
Expected total, from the thickness run's measured $0.0455 per page: about $0.55.

## What gets reported
For each indicator: count in class per arm, headroom, moved (decision_rule.py output verbatim); the outcome; G1 to G3, M1 and
per-page token counts and stop reasons; total cost. The two preflight pages are shown to the owner before Step 2 if the owner asks.
After the run: fingerprints and run log convert to agentbench's case/arm/repeat table, and register row S19 (measurement-validity/register)
is updated with the outcome and any instrument failure found.

## Known limits
- One word, one brief, one model, k=5. Majority screens, not effect sizes.
- The indicators were chosen from the thin run of the thickness run, so the rule is tuned to properties the word is already known to move.
- "Plain and concrete" is a voice instruction that could itself nudge styling. It is in both arms, so it does not bias the contrast,
  but it can reduce headroom; that case is reported as UNRESOLVED or PARTIAL, not as Reading 2.
- The hero button is in both arms and may raise the chance of large radii in both; the headroom check covers it.
- The generation path used in the thickness run is not recorded in its run log. The input-token check above is the guard.
- The extractor can miss heading fonts set through a class. The body-font indicator does not depend on that.
