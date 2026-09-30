# Task 01 — "simple" three-arm ablation

One task, three prompts. The functional requirement is **character-identical** across arms;
only the quality-adjective margin changes. Fixed model, fixed temperature, k=10 runs per arm.

---

## Arm A — vague

```
Write a Python function `parse_duration(text)` that converts a human-written duration
string into a number of seconds. Keep it simple.
```

## Arm B — absent

```
Write a Python function `parse_duration(text)` that converts a human-written duration
string into a number of seconds.
```

## Arm C — operationalized

```
Write a Python function `parse_duration(text)` that converts a human-written duration
string into a number of seconds. Constraints: one file, no third-party dependencies,
under 40 lines, standard library only, no CLI.
```

Note the researcher degree of freedom: Arm C encodes *one* reading of "simple" (small and
dependency-free). Other readings exist — "few branches", "obvious to read", "no edge cases".
If Arm C beats Arm A, that is evidence about this operationalization, not about the word.

---

## What is deliberately unstated

Neither arm says what to do about any of these. Every run has to decide, silently:

| # | Undecided | 
|---|---|
| D1 | which unit spellings are accepted (`s`/`sec`/`secs`/`seconds`, `m`/`min`, `h`/`hr`, `d`/`day`, `w`/`week`) |
| D2 | whether compound forms like `1h30m` work |
| D3 | whether whitespace between number and unit is allowed (`2 days`) |
| D4 | whether fractional values work (`1.5h`) |
| D5 | whether input is case-sensitive (`1H`) |
| D6 | what a bare number means (`90` → 90 seconds, or an error) |
| D7 | what invalid input does — raise, return `None`, or return `0` |
| D8 | whether negatives are accepted |
| D9 | return type — `int` or `float` |
| D10 | whether a third-party dependency is pulled in |
| D11 | how many files are created |
| D12 | whether tests are written unprompted |
| D13 | whether a CLI / `__main__` block is added |

D1–D9 are read off **by execution**, not inspection — run the produced function against the
probe inputs below and record what comes back. D10–D13 come from the file listing and the diff.
No LLM judge anywhere on the measurement path.

---

## Oracle — uncontested core (pass/fail)

Every defensible reading of the task agrees on these. Use them for functional correctness only.
Do **not** show them to the model; handing over the tests operationalizes the whole margin.

```python
CORE = [
    ("90s",    90),
    ("45m",    2700),
    ("2h",     7200),
    ("1d",     86400),
    ("1h30m",  5400),
]
```

## Probes — contested behaviour (fingerprint, not pass/fail)

Record the outcome of each: the returned value, or the exception type, or a crash.

```python
PROBES = ["90", "1.5h", "2 days", "1H", "abc", "-5m", "", "1h 30m", "3 weeks", "0s"]
```

Each run yields a 10-slot outcome vector. That vector is the run's decision fingerprint.

---

## Primary outcome — scatter, not accuracy

For each arm, over all run pairs *(i, j)* within the arm:

```
disagreement(arm) = mean over pairs of ( number of probe slots where fingerprint_i != fingerprint_j / 10 )
```

Report one number per arm with a bootstrap interval. **Prediction to record before running:**
`disagreement(A) >= disagreement(B) > disagreement(C)`, while core pass rate is roughly equal
across all three. If that holds, the cost of "simple" is invisible in correctness and visible
only in run-to-run divergence — each individual run looks fine and reports success.

If core pass rate also drops in A, that is a different and stronger finding; note it separately.

## Secondary (deterministic, cheap)

- core pass rate (0–5)
- lines of code
- third-party dependency count
- files created
- tests written unprompted (bool)
- CLI added (bool)

---

## What this run can and cannot claim

**Can:** whether the decision-fingerprint measurement works at all, and whether Arm C's explicit
constraints reduce scatter. That is instrumentation calibration, and it is the point of run 01.

**Cannot:** that the *word* "simple" caused the A-vs-B difference. Semantics-preserving rephrasing
alone moves LLM behaviour substantially, so A-vs-B needs a paraphrase control arm — k rephrasings
of Arm B that never touch the adjective — to establish a noise floor. Add it before claiming a
word effect; it is not needed to find out whether the fingerprint metric is measurable.
