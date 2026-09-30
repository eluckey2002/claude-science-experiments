# Questions

Format: status | question | from | -> where it went
Statuses: OPEN, RUNNING, ANSWERED, PARKED (designed, not run), RETIRED

## Design-descriptor track (web pages)
ANSWERED | Does a vague design word change the page less when the brief already pins the decisions it would touch? | 2026-09-26 session, thickness hypothesis | -> F3 (runs/2026-09-28-thin-thick-coffee-v2)
ANSWERED | Does "Make it modern" change a one-line coffee-shop page, and does the model's default differ by model? | user's web-design example | -> F1 (runs/2026-09-26-modern-pilot-4-models)
OPEN | Does a descriptor WITHOUT a built-in recipe ("professional", "clean", "minimal") scatter results, or converge on its own recipe? | F3 next question | 
OPEN | Do Opus 5.5 and Fable 5.1 carry the same recipe for "modern" as Sonnet 5, or different ones? | F1 (Opus split 2-1), F3 | 
OPEN | Does the recipe depend on the business? (coffee shop pulled serif, Bitcoin app pulled Inter + dark) | F2, F3 | 
OPEN | If a style guide pins only some properties, does the word act on the rest, or still go silent? | F3 (P3 not supported) | 
OPEN | Do extra irrelevant sentences ever matter? (neutral arm inert in v2; moved a heading font 2/5 in the failed Bitcoin run) | F2, F3 | 
OPEN | White paper: how strong is each model's "house default", and does it change across generations? Metrics: brief sensitivity, identifiability, checklist rate. ~10 briefs x 5 runs x models, ~$100. | 2026-09-26 session | 

## Code track
PARKED | Does "keep it simple" cause silent, incompatible run-to-run decisions on things the prompt never specified? Three arms (present / absent / operationalized) on 30 Orchid tasks, ~$10 per word per model. | original hypothesis | runner + agentbench adapter not built
RETIRED | Same question on one hand-built duration-parser task (task01). | original hypothesis | one task cannot support a claim about a word; memorised-convention risk

## Word selection
PARKED | Which words do people actually write in agent instruction files (CLAUDE.md, .cursorrules, copilot-instructions), ranked against ordinary text? | "simple" was a folklore pick | collector kit written (tools/collector_kit.tar.gz), never produced a record; ceiling: says what people WRITE, not what MATTERS
OPEN | Does a word's leverage depend on where it sits — system prompt, task brief, tool description, repo rules file? | 2026-09-26 session | not designed
