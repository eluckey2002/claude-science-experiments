# Research portfolio map — `loop-lab` and `Map-Elites-2248`

Built 2026-09-21 from fresh clones of `LuckeyOrg/loop-lab` (139 commits, 2026-08-06 → 2026-09-20, 7,062 tracked files) and `eluckey2002/Map-Elites-2248` (238 commits, 2026-08-08 → 2026-09-18, 717 tracked files).

**Confidence labels used below:** `[verified]` = quoted from the file, grep-confirmed against source. `[read]` = from a document I read in full. `[extracted]` = from a machine summary of the document, not yet checked against the source. Nothing here was verified by re-running code.

---

## 1. What the two projects are

**`loop-lab`** asks one question repeatedly: *does added loop machinery produce measurable lift over a simpler control, on policies you can only score with judgment?* It contains a lab charter, an acceptance-rule framework, and ten studies. `studies/` holds 6,314 of the repo's 7,062 files — the studies are the repo.

**`Map-Elites-2248`** is game experimentation — a MAP-Elites archive over a 2248 solver — governed by an evidence ledger that decides what may be cited as accepted evidence. Experiments are registered protocols (`RESULT-00NN`) rather than arm comparisons.

The projects are methodologically continuous: both separate *what happened in a run* from *what may be claimed from it*, and both enforce that separation with machinery rather than intention.

---

## 2. The `loop-lab` studies

| Study | Question | Design | Outcome |
|---|---|---|---|
| `loop-census` | Where do the loop families come from? | 222 loops read out of 6,987 Claude Code transcripts, May–Aug 2026 `[verified]` | Descriptive. Source of the eight-family taxonomy. |
| `game-lab-random-control` | Does an adversarial loop beat blind random mutation? | 256 seeds, paired | Random best-of-five **met or exceeded** the loop in **162/256 (63.3%)** seeds `[verified]` |
| `osbrain-miscitation` | Does a policy revision from one counterexample generalize? | 136 mined cases, sealed holdout, dev/holdout disjoint `[verified]` | Naive baseline `v000` accuracy 0.500; candidate `v001` 0.933 `[verified]`. Surfaced and fixed an acceptance-rule defect (below). |
| `small-league` | Does a 3-Breaker/3-Refiner league beat a sequential single lineage at equal call budget? | 4 pilots, 24 sealed cases, 2 generations, 3 arms incl. zero-model-call random | League best **24 / 21 / 23 / 21**; control **16** in every pilot; random **11** in every pilot `[verified, all four]` |
| `small-league` retrospective | Were the dedup and discovery-count measures valid? | Read-only replay of 92 candidates, 3,450 candidate-challenge outcomes `[extracted]` | Recommended **withdrawing** the `HARMFUL_THIS_RUN` label and the discovery-count conclusions. 3 of 4 equal-vector groups later diverged `[extracted]` |
| `small-league-successor` | Is the league advantage *caused* by specialized roles, retained portfolios, or their interaction? | 2×2 (GG/GP/SG/SP), two artifacts, two blocks each, 192 calls, 428 receipts | **No factor positive with the same sign across artifacts and blocks.** Generation-two advanced the frontier in **3 of 16** arm-block comparisons `[read]` |
| `critic-evaluator-lab` | (predecessor two-arm comparison) | — | **INCONCLUSIVE** — seven controller defects, not the evidence `[extracted]` |
| `counterfactual-replay-study` | — | Designed | **Never run** `[extracted]` |
| `game-lab-random-control`, `user-research-naming`, `workflow-brainstorming`, `counterexample-lab-original` | — | — | Archived alongside the above |

### The acceptance-rule defect — found and fixed in-lab

`compare_metrics` vetoes any candidate whose false alarms exceed the champion's, and the champion starts as an always-PASS policy — which has zero false alarms **by construction**. A real policy at 0.933 accuracy therefore cannot beat a do-nothing champion at 0.500. This is logged as "acceptance-rule degenerate optimum — **FIXED in the lab**," with `net-gain` (`validated_catches - false_alarms`) added as the replacement rule `[verified]`.

Worth naming because it is the same failure family as the grader inversion found in `chat-archaeologist` last session, where abstention credit ranked a never-committing arm above one that was right 28/30 times. **Degenerate baselines winning under a plausible-looking acceptance rule is a recurring hazard in this portfolio, and the lab now has one documented instance of catching it.**

---

## 3. The `Map-Elites-2248` side

From `UNIVERSE.md` (a generated projection; evidence standing comes only from `EVIDENCE_LEDGER.md`) `[read]`:

- **Selection universe:** 6 levels × 12 seeds = 72 games — **11.3% of 53 shipped levels**
- **Representative holdout:** 12 levels × 24 seeds = 288 games
- **Ledger-admitted** (`RESULT-0017`, accepted): **20/25** occupied behavior cells
- **Verified but not ledger-admitted:** **23/25** occupied behavior cells
- **Generalization:** **0 of 3** representatives beat the champion on holdout — -1.48%, -33.21%, -32.74% holdout fitness
- **Declared frontier:** (1) admit or reject the latest artifact, (2) widen the selection universe before reading policy lift as generalization, (3) seek positive disjoint-holdout evidence before any champion change

The ledger carries 17 record headings with statuses `accepted` 46, `superseded` 8, `provisional` 3, `open` 3, `narrowed` 1 `[verified]`. There are 16 experiment directories, `RESULT-0020`–`0038` with gaps; every one has both `report.md` and `protocol.md`.

---

## 4. The through-line

Read together, the two projects keep producing **the same shape of result**: the elaborate mechanism achieves its proximate goal and fails to demonstrate lift on held-out evidence.

- Random mutation met or exceeded the adversarial loop in 63.3% of 256 seeds.
- The league's sealed advantage is real in the archived runs, but the successor study could not identify specialized roles or portfolio retention as its cause.
- Generation two advanced the frontier in 3 of 16 arm-block comparisons — adaptation is real, cumulative evolution is not demonstrated.
- MAP-Elites fills 23 of 25 behavior cells, and 0 of 3 elites beat the champion on holdout.

**This is a coherent research position, not a run of bad luck.** Stated positively: *across four independent attempts, added search and role machinery has produced diversity and first-generation adaptation, but no reproducible generalization advantage over cheap controls — and the measurement apparatus is what keeps establishing that.* Most work in this area never builds the control arm that would let it find this out.

The open question the portfolio is circling is therefore not "does my loop work" but **"under what conditions does elaboration ever pay, and is my design able to see it if it does?"** That second clause is the gap below.

---

## 5. Structural gaps

### 5.1 A declared power analysis that isn't there — the highest-value gap

`RESEARCH-BRIEF.md` states that block count is "set from a documented power or precision analysis" `[extracted]`, and no analysis or number appears. Meanwhile the realized design measures **contrasts of 0, ±1 sealed cases out of 24, with two blocks per artifact**.

`RESULTS.md` handles this honestly — "no p-values, confidence intervals, or composite supported/harmful label are warranted" — but the honesty is downstream of a design that can only detect very large effects. If specialization's true effect is +1 or +2 cases out of 24, this design will not distinguish it from zero, and no amount of reporting discipline repairs that after the fact.

**What would close it:** for a 24-case binary bank, compute the detectable difference at the achieved block count, and the block count needed for effects of +1, +2, +3 cases. That is arithmetic, needs no new runs, and converts "not warranted" into "this design can see effects of size X and larger." It would also tell you whether the four blocks already spent were enough to rule anything out, or only enough to fail to find it.

### 5.2 The 2248 evidence-standing gap

Your best artifact (23/25 cells) is not citable, and the citable one (20/25) is not your best. This is your own rule working correctly — but it is listed as frontier item 1 and nothing downstream can use the better artifact until it is resolved. Separately, disposition lines in the 16 experiment reports are not machine-consistent: mechanical extraction coded only 8 of 16, with formats ranging from `**Outcome:** INCONCLUSIVE` to prose. A one-line normalized disposition field per record would make the ledger queryable.

### 5.3 A wording discrepancy between two of your own docs

`studies/README.md` reports that random "beat the adversarial loop 63.3% of the time." `game-lab-random-control/PROVENANCE.md` and `small-league/PROTOCOL.md` both say random "met or exceeded" the loop in 162/256 seeds `[verified]`. Ties are folded into wins in the summary headline. The direction of the finding is unaffected; the stated claim is stronger than the source supports. Given how carefully the rest of the portfolio distinguishes claim tiers, this looks like summary drift rather than intent.

---

## 6. Where a collaboration would pay, ranked

1. **Detectability analysis of the small-league design** (§5.1). No new runs, closes a declared gap, and tells you whether to spend on more blocks or change the outcome measure. This is the one I'd do first.
2. **A sharper outcome measure than sealed pass-count-of-24.** Pass counts saturate — Task 5 arms all landed at 21–22/24, so the bank has almost no resolving power left at the top. Per-case difficulty weighting or a harder bank recovers discrimination without more calls.
3. **Pooled re-analysis across studies.** Four studies now share a structure (treatment vs control vs random-control, sealed bank, committed finalist). Pooled, they may support a statement about *elaboration in general* that no single study can make alone — while respecting that blocks within a study are not independent samples.
4. **Normalize the 2248 dispositions** (§5.2) so the ledger can be queried rather than read.

---

## Provenance

- Clones: `LuckeyOrg/loop-lab` @ `main`, `eluckey2002/Map-Elites-2248` @ `main`, fetched 2026-09-21. loop-lab checked out with `.claude/` paths excluded (2 files; the sandbox refuses to create that directory) — 7,062 of 7,062 tracked files present.
- Read in full: `small-league-successor/RESULTS.md`, `2248/UNIVERSE.md`.
- Machine-summarized: `LAB-CHARTER.md`, `README.md`, `studies/README.md`, `small-league/PROTOCOL.md`, `PROTOCOL-AMENDMENT-001.md`, `analysis/retrospective-001/REPORT.md`, `pilot-001/LIMITATIONS.md`, `successor/RESEARCH-BRIEF.md`, `LOOP-DESIGN.md`, `PRACTICAL-PROTOCOL.md`, `PORTFOLIO-GEOMETRY-AUDIT.md`.
- Grep-verified: every number labelled `[verified]`.
- **Not done:** no code executed, no receipt chain checked, no number re-derived. `pilot-001/LIMITATIONS.md` records a known unrepaired inconsistency — `STATE.json` last receipt 63 against a chain ending at 65 `[extracted]` — so receipt bookkeeping has at least one logged discrepancy of its own.
