# Claude Science Experiments

Experiments, tests and tools from work in Claude Science, organised by research program.

| Program | Question | Entries |
|---|---|---|
| [Measurement validity](measurement-validity/README.md) | Can the instruments we use to compare agents tell a real difference from a grader quirk, noise, or a test too easy to separate anyone? | 29 |
| [Lexical leverage](lexical-leverage/README.md) | Does a single word in a prompt change what an agent produces or decides? | 15 |
| [Agent failure modes](agent-failure-modes/README.md) | Can agent failures be named consistently enough to count, detect and prevent? | 5 |
| [Skill and agent evaluation](skill-and-agent-evaluation/README.md) | Do changes to skill text or agent configuration change behaviour, and can we measure that at small sample sizes? | 4 |
| [Exploratory](exploratory/README.md) | Anything that does not yet belong to a research program. | 3 |

## Layout

- One folder per research program. Each has a `README.md` with its question, where it stands, contents and an experiments table.
- `exploratory/` holds anything without a program. Move it into a program when a second experiment asks the same question.
- `experiments_ledger.csv` lists every entry with its program, status, scale and result. Status values: Ran, Ran (re-analysis), Audit, Built, Designed not run, Stopped.
- `measurement-validity/register/` is the instrument-failure register; its checker regenerates `summary.md`.
- `docs/` holds cross-program notes: `research-portfolio-map.md` and the 2026-09-30 experiment list.

## Conventions

- Keep one copy of each file. Files that were identical to something inside a tarball were dropped in favour of the extracted copy.
- Never commit secrets. Scan before pushing.
- Pre-register before any run whose result will back a general claim. 2248-challenge's own rules apply to work inside that repo.
