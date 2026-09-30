# Instrument-failure register

A measuring instrument is the grader, test bank, proxy score, rating scheme or extractor that turns a run into a number.
This register records every study we looked at, including the ones whose instrument held, so that failures can be counted against a
denominator and the share caught late can be watched.

## Unit and entry rule
- One row in `studies.csv` per study: a comparison, an instrument check or a rating-scheme check.
- A study enters when its protocol exists or it has run. A design that has no protocol does not enter.
- A diagnostic run on an already-failed study (for example a resolution analysis of a bank that could not separate candidates) is evidence on that
  study's failure row, not a new study.
- Execution defects in a runner (a bug, a stale pin, a timeout misread) belong to loop-lab's scar ledger. This register is for the instrument.

## Files
- `studies.csv` : the denominator. One row per study.
- `failures.csv` : one row per failure found. A study can have several; a study with `HELD` or `NOT_CHECKED` has none.
- `failure_types.csv` : the plain-language types, what each is, and the cheapest early check.
- `check_register.py` : validates both tables and regenerates `summary.md`. Run `python measurement-validity/register/check_register.py --write`.
- `summary.md` : generated counts. No number in this README is typed; read them there.

## Fields that need a definition
- `instrument_status`: `FAILED`, `PARTLY_FAILED` (some of the readings were unusable), `HELD` (the instrument was checked and passed),
  `NOT_CHECKED` (used, never checked). `NOT_CHECKED` is not a pass.
- `spend`: `MODEL_CALLS` (we made them), `INHERITED` (someone else produced the data before we looked), `NONE`, `NOT_RECORDED`.
- `caught_when`: `BEFORE_SPEND` means before any model call for that study; `AFTER_SPEND` means after model calls were made or the data was inherited.
  The checker rejects `BEFORE_SPEND` on a study that already spent model calls.
- `cause_status`: `DIAGNOSED`, `MEASURED_NOT_EXPLAINED` (the failure is measured but the cause has not been traced), `INFERRED` (our reading of the data).
- `prevention_status`: `GUARDED` (a control now stops or flags it where it would happen), `PARTLY` (flagged in a report or written down, but nothing blocks a run), `NONE`.

## Reading the rate
- The number to drive down is the share of failures caught after spend. Finding more failures early is good; `summary.md` reports both.
- The seed rows are the studies we chose to examine, several of them because something already looked wrong. The share of studies with a failed
  instrument in the seed is therefore not a base rate for your work. It becomes one only once new studies enter at the moment their protocol exists.
- A week with few studies and no failures is not a trend. Compare weeks only when each has enough studies to count.

## Adding a row
1. Add the study to `studies.csv` when its protocol exists. Use `NOT_CHECKED` until something checks the instrument.
2. If a failure is found, set the study's status and add a row to `failures.csv` with its type, cause, prevention and when it was caught.
3. Use a label from `failure_types.csv`. Add a new type there first if none fits.
4. Run the checker. It must exit 0.
