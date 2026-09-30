# Skill and agent evaluation

**Question.** Do changes to skill text or agent configuration change behaviour, and can we measure that at small sample sizes?

**Where it stands.** Trigger evaluation of the repo-rules-preflight description reached n=50 (45/48 vs 42/48, within noise). Fresh-eyes audits of the corpus-librarian skill ran three rounds; the auditor prompt and relay gate were patched.

## Contents

- `trigger-eval/` : eval set, harness, runs and report
- `specialist-relay/` : skill under audit, audit output and retro

## Experiments

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 2026-09-20 | repo-rules-preflight description trigger eval, n=20 | Ran | 20 queries x 3 repeats | Unresolved: 2 discordant queries (p=0.50) |
| 2026-09-20 | repo-rules-preflight description trigger eval, n=50 | Ran | 50 queries x 3 repeats | Reworded description 45/48 vs original 42/48: fixed 3, broke none; within noise at this n. Judge repeat variance near zero |
| 2026-09-26 | Fresh-eyes audits of corpus-librarian skill, rounds 1-3 | Ran | 3 sub-agent audits | Rounds 1-2 found real defects, fixed; round 3 was a false positive from a depth-capped auditor |
| 2026-09-26 | Auditor prompt and relay-gate patches | Built | 1 profile edit, 1 skill publish | Live; depth-capped claims now reported as unverifiable |
