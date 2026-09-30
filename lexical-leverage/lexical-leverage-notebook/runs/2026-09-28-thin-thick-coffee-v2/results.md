# Results: thickness test v2 (Sonnet 5, coffee shop, 2x3xk=5, 2026-09-28)

Protocol: protocol_thickness_v2_DRAFT.md (predictions written before running). Preflight M1-M3 passed.
30 pages, 0 errors, 0 truncations, 135,460 output tokens, $1.37 at list.

## Predictions vs outcome
P1 thin: "modern" changes body font class in >=4/5 runs.        HELD. absent: Georgia 3, Trebuchet 1, Segoe 1 -> modern: Segoe UI 5/5.
P2 thick: "modern" changes no pinned property in >=4/5 runs.     HELD. Of the ten PINNED properties, 9 were 5/5 unchanged and accent was 4/5 (one run used the text colour #2b1d14 as accent). Of the ten properties CHARTED in the report (which swaps section count in for keyframes/accent hue), 8 were 5/5 unchanged: accent 4/5 and section count 4/5 (one run added a 4th section).
P3 thick: leftover leverage shows on OPEN properties.            NOT SUPPORTED. Only page size moved (10.0k -> 11.3k chars, +13%); one run added a 4th section; colour count and backdrop blur unchanged (blur 0/5 in every thick cell).
P4 neutral arm inert.                                             HELD. thin-neutral fonts (Georgia 3, Trebuchet 2) sit inside the absent distribution; thick-neutral identical to thick-absent on every pinned property.

## What "modern" did in the THIN brief (absent -> modern, k=5 each)
body/heading font   Georgia 3 / Trebuchet 1 / Segoe 1  ->  Segoe UI 5/5
backdrop blur       0/5                                 ->  5/5
max radius          30px x4, 10px x1                    ->  50px x3, pill x2
gradient count      1 x4, 2 x1                          ->  1..6 (median 3)
container width     900-1100 mixed                      ->  1100 x4, 1140 x1
dark theme          0/5                                 ->  1/5
page size           8.1k +- 1.4k chars                  ->  11.7k +- 2.8k  (+44%)
Six of ten measured properties moved.

## What "modern" did in the THICK brief
Two single-run deviations (accent colour once, section count once), page size +13%. Zero of ten moved by majority, on either property set.

## Dispersion (distinct values across 5 runs)
thin  body font: absent 3, neutral 2, modern 1   - the word CONVERGED the font, it did not scatter it.
thin  gradients: absent 2, neutral 2, modern 4   - and scattered the gradient count.
thick: every pinned property has dispersion 1 in every arm.

## Reading
1. The thickness hypothesis held on this brief: the word's leverage is large when the properties it acts on are open
   and ~zero when they are pinned. The spec did not just block the pinned properties - it also blocked the word's
   effects on properties the spec never mentioned (backdrop blur, page structure). Leverage did not flow; it vanished.
2. For Sonnet 5 on this brief, "modern" behaves like a commitment word with a house meaning (system sans + blur +
   larger radii + more gradients), not like an open adjective. It reduced font dispersion. This is the second time the
   pilot pattern has appeared and it now has k=5 behind it.
3. Neutral extra sentence: inert. The earlier Sora/Trebuchet shifts were within-arm noise.

## Limits
One word, one brief, one model, k=5. Majority-vote answers, not effect sizes. The thick spec pinned exactly the
properties the instrument reads, which is the strongest version of the manipulation; a spec that pins some and
leaves others open is the next natural step, as is a word without a house meaning (e.g. "professional", "clean").
