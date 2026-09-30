# Lexical leverage

**Question.** Does a single word in a prompt change what an agent produces or decides?

**Where it stands.** Pilots on web-page generation show 'modern' moving the body font and other properties, and a short style guide removing that effect. The pre-registered Orchid study ('simple') is designed and reviewed but no model calls have been made. The coherence test and the recipe-dictionary test are proposed, not run. The image-description stimulus set is built; its pilot has not run.

## Contents

- `lexical-leverage-notebook/` : running notebook (README, FINDINGS, QUESTIONS, per-run folders, tools)
- `modern-web-design/` : thick-brief pages
- `simple-ablation/` : pre-registrations and their reviews
- `literature/` : survey of published word-effect studies
- `collection/` : rule-file collector kit and repo inventory
- `image-description/` : 26-image stimulus set and key

## Experiments

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 2026-09-22 | Duration-parser task (task 01) | Designed, not run | 3 arms x 10 reps planned | Spec, probes and pre-registration written and audited; shelved because one task cannot support a claim about a word |
| 2026-09-26 | Four-arm Orchid pre-registration | Designed, not run | 30 tasks x 4 arms x 5 reps = 600 calls | Two independent reviewers: 'not fundable as written; fixable before first model call' |
| 2026-09-26 | Two-arm Orchid pre-registration | Designed, not run | 30 tasks x 2 arms x 5 reps = 300 calls | Round-1 reviewers: not fundable yet; fuzz probes seeded with Python's non-deterministic hash() |
| 2026-09-26 | Orchid dataset structure check | Ran | Sample rows vs 164 tasks | Prompt + hidden tests usable as the base for the arms |
| 2026-09-26 | Sonnet vs Haiku cost estimate | Ran | 30 completions | About $0.15-0.20 Sonnet vs $0.07-0.10 Haiku |
| 2026-09-26 | Coffee-shop landing page pilot | Ran | 2 arms x 3 runs = 6 pages | Without the word, runs disagreed on font, width, radius, header; with 'modern', all three agreed |
| 2026-09-26 | Cross-model extension | Ran | 4 models x 2 arms x 3 runs = 24 pages (~$2.60) | Body font moved from serif (Georgia, 8/12) to sans-serif in 12/12 'modern' runs on all four models |
| 2026-09-26 | Word-screen cost model, re-priced on measured tokens | Ran | 24 pages; extrapolated | Ten words across Sonnet/Opus/Fable about $6,900 list ($3,400 batch) |
| 2026-09-26 | Thin vs thick brief, Bitcoin app | Ran | 2 x 3 x 5 = 30 pages, Sonnet 5 (~$7) | Brief choice already matched the thick spec's defaults, so the manipulation had little room to act |
| 2026-09-26 | GitHub rule-file collector smoke test | Stopped | 2 attempts | Stopped by user; collection moved to Claude Code on your machine |
| 2026-09-27 | Thin vs thick brief, v2 (four conditions) | Ran | 4 conditions x 5 pages | Thin: blur 0/5 without 'modern', 5/5 with it. Thick: 0/5 both ways; the style guide suppresses the word |
| 2026-09-27 | Coherence test (content-only guide) and recipe-dictionary test | Designed, not run | Coherence: 12 pages (~$0.55); dictionary: 10 descriptors (~$6) | Coherence protocol, frozen prompts and decision rule written 2026-09-30 (notebook run folder 2026-09-30-coherence-test); no model calls yet. Recipe dictionary still proposed. |
| 2026-09-28 | Design fingerprint extraction pipeline | Built + tested | 14 regex-parsed properties | Used to score all pages above |
| 2026-09-28 | Vendor design-claim audit (Anthropic release pages) | Ran | 5 primary pages | Explicit design claims in Opus 4.5, narrowing afterwards, none by Opus 5.5 |
| 2026-09-28 | Stimulus set for 'describe in one word' study | Built | 26 images (11 originals, 11 light, 4 off-centre) | 260-call pilot proposed; waiting on model choice |
