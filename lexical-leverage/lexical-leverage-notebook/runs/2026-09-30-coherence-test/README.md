# 2026-09-30 coherence test

Status: PRE-RUN. Protocol, frozen prompts and decision rule are written; no model call has been made.
Exploratory screen, no heavy pre-registration (same as the thickness run).

- protocol.md : question, design, predictions, decision rule, spend ladder, limits
- arms.json : the two frozen prompts and run settings (sha256 caf688f2f9c1df9fb70930050de1846ed0a94776eef3f57781e6d7d8791b2911)
- guide_lint.py : checks the guide pins no visual property
- preflight_checks.py : gates for the one-page-per-arm check
- decision_rule.py : the frozen outcome rule; back-tested on the thickness run's data
