# Findings

Shape of every entry: what we found / what it rests on / what it does not cover / next question.

## F3 — "Modern" only matters when the brief leaves room for it; and it is a recipe, not a vague word (2026-09-28)
What we found: Ask Sonnet 5 for a coffee-shop page five times and you get roughly the same page five times, with the font wobbling (Georgia 3, Trebuchet 1, Segoe 1). Add "Make it modern." and you get a different page five times, identical to each other: system font 5/5, frosted blur 5/5, rounder corners, more gradients, +44% longer. Put a short style guide in front (fonts, colours, radius, gradients pinned) and the word changes nothing — not the pinned properties, and not the unpinned ones either (blur stayed 0/5). A neutral extra sentence changed nothing in either case.
Rests on: runs/2026-09-28-thin-thick-coffee-v2. One word, one brief, one model, 2 thicknesses x 3 arms x 5 runs = 30 pages, predictions written first, one-page-per-cell preflight passed, $1.37.
Does not cover: other descriptors, other models, other businesses, style guides that pin only some properties. Majority-vote answers, not effect sizes. The expected "dozens of variations" from a vague brief did not appear: the model's default on this brief is already narrow.
Next question: does a descriptor without a built-in recipe ("professional", "clean") scatter results, or converge on its own recipe?

## F2 — For a Bitcoin brief, Sonnet's default already IS a typical crypto design spec (2026-09-26, from a failed run)
What we found: A one-paragraph Bitcoin-savings-app brief produced Inter + Space Grotesk on a near-black background in 5/5 runs — the same choices the user's 20 KB design-system spec dictates. Thin and thick pages were indistinguishable on every measured property, so the run could not test the thickness hypothesis.
Rests on: runs/2026-09-26-thin-thick-bitcoin-FAILED-DESIGN, 30 pages, Sonnet 5.
Does not cover: whether this holds for other models or other crypto briefs. The neutral arm moved a heading font to Sora in 2/5 thin runs; not replicated in F3.
Next question: (led to F3's design) pick a brief whose default differs from the spec.

## F1 — "Modern" flips the body font in every model, and each model has its own default (2026-09-26, exploratory)
What we found: On the coffee-shop brief, adding "Make it modern." moved the body font from a serif or named sans to a system sans in every model tried. Defaults differed: Opus 5.5 and Fable 5.1 chose Georgia 3/3; Sonnet 5 scattered (Georgia 1, Trebuchet 2); Haiku 4.5 scattered (apple-system, Segoe, Georgia). Under "modern", Haiku, Fable and Sonnet each converged 3/3 on one font; Opus split 2-1.
Rests on: runs/2026-09-26-modern-pilot-4-models, 6 pages per model, no protocol written first. Prices and token sizes measured in cost_model.csv.
Does not cover: anything beyond font/background-level properties at k=3. Hints, not findings.
Next question: does the effect survive a thick brief? (-> F2, F3)
