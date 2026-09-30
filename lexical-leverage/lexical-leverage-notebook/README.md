# Lexical leverage — lab notebook

Which individual words in instructions to agents carry behavioural weight, and what that weight does.

Three files that point at each other, and nothing else:

- QUESTIONS.md — one line per question, with a status (open / running / answered -> finding) and where it came from.
- runs/<date>-<slug>/ — one folder per run: protocol written before the run, results, data, report.
- FINDINGS.md — one entry per finding, in a fixed shape: what we found / what it rests on / what it does not cover / next question.

New questions are made by copying a finding's "next question" line (and any others the run raised) into QUESTIONS.md, tagged with the run.
Heavy pre-registration is reserved for runs whose result would be cited outside; exploratory runs say so in their README.

tools/      fingerprint_v2.py (page fingerprint extractor), collector_kit.tar.gz (Claude Code collectors for the word corpus; unrun)
reference/  verbatim digest of the 2026-09-26 design session (corpus tiers, keyness, sizing, cost model, white-paper idea)
