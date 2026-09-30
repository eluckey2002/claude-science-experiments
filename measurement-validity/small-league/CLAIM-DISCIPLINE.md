# Claim discipline

How to hand claims to a reader — human or agent — so they can be trusted without
trusting the author. Written 2026-09-20 after a session in which five of the
author's claims were wrong.

Prose rules don't produce confidence; a checker does. So this document ships with
`claims.json` (a manifest) and `verify_claims.py` (a verifier that re-derives
every claim from primary sources). The rules below exist to explain the manifest,
not to substitute for it.

---

## 1. Three kinds of claim, and what each is worth

Every load-bearing statement is exactly one of these, and it is labelled.

| Type | Means | Verification | Reader's job |
|---|---|---|---|
| **MEASURED** | Computed from named inputs by a recorded expression | Re-run the expression; compare to the recorded value | None, unless it fails |
| **QUOTED** | Present verbatim in a named source file | Substring match against a file whose sha256 matches the record | None, unless it fails |
| **ARGUED** | The author's inference | **None possible** | All of it |

The point of the split is that it changes where attention goes. A reader who has
to audit every sentence at the same intensity will audit none of them well. With
the split, `verify_claims.py` disposes of the first two kinds mechanically and the
reader spends their judgement on the third — which in practice is a handful of
statements, not a document.

**Failing to label is the defect.** Presenting an inference in the same voice as a
measurement is what forces the reader to audit everything.

---

## 2. The rules

**These are the author's obligations, not the reader's checklist.** Nobody should
be reading a report while auditing whether R1 was followed — that would be a worse
burden than the one the labelling was meant to remove. They are written down so
the obligation is explicit and so a future session inherits it, not so it can be
policed from the outside. What the reader gets is `verify_claims.py` and a short
list of open questions; everything below is upstream of that.

Each rule is stated with the real failure it would have caught. The failures are
from one session; the rules are not hypothetical.

### R1. Never assert from a machine summary — least of all an absence

**Failure it catches.** Two of five. `RESEARCH-BRIEF.md` was read through a
side-model summary that reported "power analysis: not stated numerically." That
became the claim "the brief declares a power analysis and never provides one,"
which was repeated across four messages and written into a saved artifact. The
brief in fact says *"Before using causal-effect language, ... set the required
block count from a documented power or precision analysis"* — a precondition for
a claim the study deliberately never made.

**Rule.** A summary is a pointer to where to read, never a source. Any claim about
what a document says, and every claim about what it *omits*, comes from the
primary text. A summary's silence is evidence the summarizer didn't surface
something, not evidence of absence.

### R2. Make the sentence say what the code tested

**Failure it catches.** The claim "no contrast has a consistent sign under any of
the three measures" — where the code had grouped by measure and checked across
*blocks*, while the sentence also reads as across *measures*. Several contrasts do
agree across measures within a single block. Both readings were in the same
sentence; only one had been computed.

**Rule.** When a claim is a quantifier — no, all, every, only, none — the code
computes that exact quantifier and the sentence quotes its output. Do not
paraphrase a predicate you tested into a predicate you didn't.

### R3. Never recommend an instrument in the message that invents it

**Failure it catches.** "The descriptor vector is the higher-resolution signal you
already record" — proposed as a recommendation and written into an artifact, then
refuted an hour later by a single cell that measured it. The two partitions
cross-cut: P(same behaviour | same descriptor) = 0.60 and 0.32,
P(same descriptor | same behaviour) = 0.14 and 0.08.

**Rule.** Validate a proposed measure before recommending it, in the same turn.
The validation is usually one computation; the retraction is never that cheap.

### R4. Describe past actions by quoting the record

**Failure it catches.** "Nothing beyond the file census was ever read" — the cell
record showed all eleven documents had been read into memory before the
summarization step was interrupted.

**Rule.** Don't characterize your own prior actions from memory. Read the
execution record and quote it.

**What none of these are.** They are scope errors, not effort errors. "Be more
careful" would have prevented none of them.

---

## 3. Running the verifier

```sh
python3 verify_claims.py claims.json --repo /path/to/loop-lab
```

Exit 0 only when every MEASURED claim recomputes to its recorded value and every
QUOTED claim is found verbatim in a source whose sha256 matches. ARGUED claims
report `UNVERIFIABLE` and never pass or fail — they are surfaced so a reader can
see exactly how many judgement calls a document is asking them to accept.

Current state of this session's claims:

```
27 passed, 0 failed, 1 unverifiable (argued)
```

28 claims: 21 measured, 6 quoted, 1 argued. The single argued row is an open
question, not an assertion.

The verifier caught one defect in itself on first run: MEASURED expressions were
evaluated with the data namespace passed as `locals`, so a generator expression
inside a claim could not resolve its free names. Two claims failed with
`NameError` rather than silently passing. That is the intended behaviour — a claim
that cannot be evaluated is a failure, not a pass.

A tamper check is worth running once to see it work: append a byte to any quoted
source file and its claims fail with `source sha256 changed`.

---

## 4. R5: an argued claim is a failure to run a test

**The rule that matters most, added after the first draft of this document was
rejected for exactly this reason.**

The first version of this manifest labelled three claims ARGUED and handed them to
the reader as "UNVERIFIABLE — requires independent judgement." That is not a
mechanism. It verifies the claims that were never in doubt (numbers computed by
code recompute; of course they do) and transfers the doubtful ones to the reader
with a label attached. Two of the three were testable from columns already present
in the data.

**Rule.** Before labelling a claim ARGUED, state the test that would falsify it and
whether that test was run. If the data to run it is in hand, run it — an ARGUED
label over testable data is a failure to do the work, not an honest disclosure. If
it genuinely cannot be tested, state it as a **question**, not a claim, and name
the test that would settle it.

What happened when that rule was applied to the three:

**`proxy-transfer` → MEASURED, supported.** The non-sealed qualification proxy was
saturated and carried no rank information about sealed standing. On Task 4, 38 of
48 candidates scored a perfect diagnostic rate while their sealed scores spanned
8 to 17; Spearman correlation between diagnostic rate and sealed passes was
**+0.050**. On Task 5, 45 of 48 were perfect on diagnostics, sealed range 19–23,
Spearman **−0.029**. Qualification passed because the proxy said every candidate
was equally good, and the proxy was right about nothing. This is the mechanism of
the failure, and it was a measurement the whole time.

**`extremes-not-band` → MEASURED, and it refined the claim rather than confirming
it.** Restricting to the comparison band leaves the *same* two discriminating cases
as the full pool, and the band is 46 of 48 candidates. There was no
extremes-versus-band gap in the candidate population; the original framing
conflated "the probes sat at the extremes" with "resolution was only measured at
the extremes." The prescription survives — probes spanning the candidate range
would have reported two discriminating cases and flagged the bank — but the
diagnosis as first written was wrong.

**`mechanism` → downgraded to a question.** *Would specialized roles and retained
portfolios differ on a task whose discriminating cases test search quality rather
than validation-error enumeration?* Not testable without a new bank, so it is
stated as the question it is. The falsifying test is a 2×2 on a bank whose
discriminating cases test search quality. Until that runs, no position is warranted
either way — including the one previously asserted here.

Result: **one open question instead of three judgement calls**, and the question
carries the test that would answer it.

---

## 5. What this mechanism does NOT give you

- **It does not make a measured claim relevant.** A claim can recompute exactly and
  still answer a question nobody asked.
- **It does not check that the expression measures what the statement says.**
  `len(discriminating(4))` returning 2 is verified; that "discriminating" is the
  right operationalization of resolution is an argued choice embedded in the
  verifier's own helpers.
- **It does not verify the ARGUED row**, which is why R5 exists: the goal is to
  drive that count toward zero by testing, not to grow it with honest labels.
  Every one of this session's interpretation failures lived in that category.
- **It does not cover claims absent from the manifest.** A document can make
  twenty claims and register five. Coverage is the author's discretion, and that
  is the weakest joint in this design.
- **It executes expressions from the manifest**, so the manifest is part of what a
  reviewer reads, not an input they can accept unexamined.
