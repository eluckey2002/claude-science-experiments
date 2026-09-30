# Protocol draft: does a vague design word lose leverage as the brief gets thicker?

Status: RUN 2026-09-28 as written (preflight passed; 30 pages). Results in results_thickness_v2.md. Supersedes the 2026-09-26 thin-vs-thick run
(retro_thin_thick_sonnet_run.md), which could not vary openness because the thin Bitcoin brief's default
already matched the spec.

## Question
Does "Make it modern." change fewer design decisions when the prompt already pins those decisions?

## Why coffee shop, not Bitcoin
Pilot evidence (fingerprints.csv, Sonnet 5, Northside Roast, k=3): absent arm gave Georgia 1 / Trebuchet MS 2;
"modern" gave Segoe UI 3/3. So on this brief the word has a known, measurable effect and the model's default
is NOT what the word produces. That is the gap the last run lacked.

## Design  (2 thickness x 3 arms x k=5 = 30 pages, Sonnet 5)
Thin brief (verbatim from the pilot):
  "Build a single-file landing page (HTML with embedded CSS, no external libraries) for a neighbourhood
   coffee shop called Northside Roast. Include a header, a hero, a short menu section, opening hours,
   and a footer. Return only the HTML."
Thick = the same brief preceded by a SHORT design spec (~15 lines) that pins, with values chosen to sit
away from where "modern" pulls:
  body font Lora (serif), heading font Playfair Display (serif), background #FAF6F0 (light cream),
  text #2B1D14, accent #7A4A2A (espresso), border radius 4px, no gradients, no animations,
  content max-width 1100px, static (non-sticky) header.
Arms appended before "Return only the HTML.":
  absent  - nothing
  neutral - "Write all copy in English."   (control for "any extra sentence")
  modern  - "Make it modern."

Not the user's 20 KB spec: the point is to pin the fingerprint properties, not to reproduce prompt length.
Length is a separate variable and can be added later as a third level.

## Pinned vs open properties (from fingerprint_v2.py)
Pinned by the thick spec: body_font, heading_font, bg / bg_lightness / dark_theme, accent / accent_hue,
                          max_radius_px, n_gradients, n_keyframes, container_px, sticky header.
Left open in both:        n_distinct_colors, n_sections, uses_backdrop_blur, layout choices, html_chars.

## Predictions (written before running)
P1  Thin: "modern" changes body_font class (serif/named -> system/named sans) in >=4/5 runs vs absent.
    (Replicates the pilot.)
P2  Thick: "modern" changes NO pinned property in >=4/5 runs. Leverage on pinned properties ~ 0.
P3  Thick: if the word has leverage left, it shows on OPEN properties (backdrop blur, colour count,
    section count, page size) - "leverage flows to what is left open". Exploratory; no threshold.
P4  Neutral arm differs from absent on nothing in either thickness. (Last run: thin-neutral moved the
    heading font to Sora 2/5 - if that recurs it is a finding about extra sentences, not about "modern".)
Dispersion, per cell: number of distinct values per property across the 5 runs. Expect thick-absent
to have lower dispersion than thin-absent on pinned properties (this is the openness manipulation itself).

## Manipulation check BEFORE the batch (the preflight the retro proposed)
Generate ONE page per cell (6 pages, ~$0.50). Proceed only if all hold:
  M1  thin-absent body_font is not a system/named sans  (the word has somewhere to go)
  M2  thick-absent honours the spec on body_font, heading_font, bg, accent  (the pins hold)
  M3  set max_tokens to 1.5x the longest of the six pages (last run truncated 10/15 at 16k)
If M1 or M2 fails: stop, report, redesign. Do not spend the remaining ~$3.

## Outcome table (what gets reported)
For each property x thickness: absent value distribution, modern value distribution, changed? (yes/no
by majority), dispersion(absent), dispersion(modern). Plus the M1-M3 results and per-cell token counts.

## Cost (Sonnet 5 list, $2 in / $10 out per M tokens)
Thin ~9k out, thick ~10k out (spec is short) -> ~$0.10/page -> 30 pages ~ $3, preflight ~ $0.50.
Batch API would halve it; not worth the latency at this size.

## Known limits
- k=5 gives majority-vote answers, not effect sizes. This is a screen for the thickness hypothesis,
  sized to decide whether a real run (k>=20, several words, several briefs) is worth designing.
- One word, one brief, one model. Nothing here generalises past that on its own.
- The pilot already hints that "modern" CONVERGES runs (3/3 same font in Haiku, Fable and Sonnet; Opus
  split 2-1 between system-ui and -apple-system) rather than scattering them -
  for design descriptors the word may carry a stable house meaning. That cuts against the dispersion
  framing and should be looked at directly once thin-vs-thick is settled.
