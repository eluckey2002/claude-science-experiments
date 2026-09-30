# Agent failure modes

**Question.** Can agent failures be named consistently enough to count, detect and prevent?

**Where it stands.** A 23-mode lexicon has been through two fresh-eyes audits. The inter-rater pilot (18 windows, kappa 0.486) contained one codable failure, so it tests the procedure, not the scheme. A literature survey found runtime detectors for 12 of the 23 modes.

## Contents

- `agent-failure-modes.json`, `lexicon-audit.md`, `audit.json`, `counter-audit.json`, `proposed-additions.json`
- `excerpts.json`, `ratings.json`, `rating-agreement.csv`, `pilot-report.md` : inter-rater pilot (one pasted access token in `excerpts.json` was redacted before commit)
- `detector-*`, `judge-layer.md`, `rules-files.md`, `failure-mode-rules.md` : detector survey and rule-file drafts

## Experiments

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 2026-09-21 | Fresh-eyes audit of the lexicon (v2.2) | Audit | 23 modes; 11 citations checked | Ten blocking defects, incl. confusable clusters with identical facets and 4 citation defects |
| 2026-09-21 | Counter-audit of proposed new codes | Audit | 10 proposed codes | About three net additions survive; 'computation error' rejected |
| 2026-09-21 | Inter-rater agreement pilot | Ran | 18 trace windows from 7 sessions | 17/18 agreement, kappa 0.486; only 1 window held a codable failure, so the pilot sets up the method rather than measuring the scheme |
| 2026-09-21 | Detector-coverage literature survey | Ran | 74 queries -> 509 records -> 327 screened | 12 of 23 modes have something wireable to a runtime detector; 11 have none |
| 2026-09-21 | Prevention-shortlist filter and CLAUDE.md rule drafts | Built | 10 rules; v1 then v2 (938 words) | v2 has trigger + reframe + rationale; not yet tried on real traces |
