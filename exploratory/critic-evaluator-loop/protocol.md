# Critic–evaluator loop test on the JEV routing design — protocol (frozen before any critic run)

Date: 2026-09-29. Critic, reviser and graders: claude-sonnet-5.

## Question
Does a critic given outside information (the design's cited sources) drive a critique→revise loop to remove more flaws than a critic that only rereads the document?

## Test item
Your JEV model-routing design (original: pasted-text-2026-09-29T00-36-04.txt), with 12 planted flaws -> design_seeded.md.
- 6 external flaws: each contradicts a cited source (S1 Codex config docs, S2 openai/codex source + proxy README, S3 TypeSafe/JEV OpenAPI, S5 Codex telemetry docs). Internally consistent with the rest of the document, so rereading alone should not reveal them.
- 6 internal flaws: each contradicts another passage of the same document.
- S4 (ChatGPT billing help articles) is not in the source pack: help.openai.com served a bot-challenge page.
Answer key: answer_key.json.

## Arms (identical prompts except for the information given to the critic)
- Rereading: critic gets the document only.
- Outside information: critic gets the document + sources_pack.txt (~220k chars; S1, S2, S3, S5).
The reviser is the same in both arms: it gets the document + the critique, never the sources, and returns exact find/replace edits.

## Loop
3 rounds of critique -> revise; 3 independent repeats per arm. Each round's critic sees only the current document (no earlier critiques). The answer key never enters the loop.

## Measures (graded blind to arm, by a grader holding the answer key)
1. Found: did the round's critique identify each planted flaw (calibrated: 12/12 on a full synthetic critique, 0/12 on a topic-only critique, 6/6 on a half critique).
2. Remaining: after each revision, is each planted flaw still asserted (calibrated twice: 12/12 present on seeded, 0/12 on original).
Headline: flaws remaining after round 3, split external vs internal, per arm.

## Prediction (frozen)
- External flaws: outside-information arm removes clearly more than the rereading arm.
- Internal flaws: the two arms remove about the same number.
Falsified if the rereading arm matches the outside-information arm on external flaws (within 1 flaw on the mean of 6), or if the outside-information arm is clearly better on internal flaws too (the gain would then be about something other than the sources, e.g. a longer, more careful critique).
