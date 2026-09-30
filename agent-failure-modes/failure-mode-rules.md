# Failure-mode rules

Ten failure modes from the agent-failure-mode lexicon v2.5, selected because the agent
can recognise each from its own trace (`detectability: trace-visible`) and correct it by
changing what it does next (`intervention: reframe-sufficient`). Modes needing an
external oracle or a tool are deliberately absent — a reframe is the wrong intervention
shape for those.

Each entry has a trigger and a reframe. The trigger is what to watch for; the reframe is
what to do when it fires. Reframe text is verbatim from the lexicon, so it stays
greppable against the source.

These are the agent's obligations. Nothing here asks the reader to audit compliance; the
markers exist so an intervention can be found later, not so anyone has to police them.

## Marker protocol

On applying a reframe, emit one line before continuing:

    🔻⟦FM:CODE⟧ was: <what I was about to do> → now: <what I did instead>

Both halves are required. A marker without the pair is a claim about internal state and
is itself a Process Misreport. Extract with `⟦FM:([A-D]\d)⟧`; the code maps to
`mode_code` and `intervention.reframe_code` in the lexicon's telemetry event schema.

Markers record catches, never misses — they fire only when the agent noticed. They make
an intervention findable in a trace. They do not support counting how often a mode
occurred.

## Framing

### No Questions Asked (A4)

**Fires when:** Guesses on ambiguity instead of asking.

**Reframe:** If a load-bearing requirement is ambiguous, ask one targeted question before proceeding — don't guess silently.

*Why: a wrong assumption costs more downstream than a question costs now.*

## Reasoning

### First Suspect (B4)

**Fires when:** Locks on hypothesis #1, skips the rest.

**Reframe:** Generate at least two more hypotheses before committing, and name what would disprove your leading one.

*Why: the first hypothesis is the one anchoring did the most work on.*

### Sunk Path (B5)

**Fires when:** The objective and constraints are intact and the actions vary, but a plan already shown to be failing is retained across them. If the actions are near-identical, this is D1.

**Reframe:** Ignore effort already spent. Judge this approach only on its remaining cost to succeed. Backtracking is allowed.

*Why: effort already spent is not evidence the approach will work.*

## Verification
Ask these in order. A fabricated check reads as real to every rule below it, so
Process Misreport comes first.

### Process Misreport (C7)

**Fires when:** A verification act is absent from the trace AND the agent asserts one occurred, or work was partially covered AND reported as complete. Ask this before C2: if no check occurred and none was claimed, it is C2, not C7.

**Reframe:** Claim only actions that appear in your own trace. If you did not run the check, say you did not run it; if you covered part of the input, say which part and why.

*Why: an asserted check that did not happen invalidates every test that trusts it.*

### Sailing (C2)

**Fires when:** No verification act appears anywhere in the trace, and the agent does not claim one occurred. If a check was attempted, however shallow, this is not C2; if none occurred but one was asserted, this is C7.

**Reframe:** Before returning, run an explicit check: re-derive, test, or verify. Do not finish on the first pass alone.

*Why: a first pass that looks right is the most common shape of a wrong answer.*

### Skating (C3)

**Fires when:** A verification act appears but never executes the artifact under test — it inspects, describes, or reasons about it instead. If the artifact was actually run, this is not C3.

**Reframe:** Aim your check at where this would actually break — edge cases, boundaries, the hard step — not the easy parts.

*Why: reading an artifact and executing it fail in different places.*

### Spot-Check (C4)

**Fires when:** The artifact is executed, but on exactly one case. If coverage extends past a single case, this is not C4.

**Reframe:** Test multiple cases, including adversarial ones. Don't generalize correctness from a single success.

*Why: one passing case is consistent with almost any defect.*

## Execution

### Spinning (D1)

**Fires when:** The objective and constraints are intact and the action is near-identical across steps — repetition without progress. If the actions vary, this is B5.

**Reframe:** If the last step produced no new progress, stop and change approach — don't repeat it.

*Why: a step that produced nothing will produce nothing again.*

### Drift (D2)

**Fires when:** The original objective is no longer what is being pursued — a self-generated sub-goal has displaced it. Ask this first: if the objective is still intact, the failure is one of D3, D1 or B5, not D2.

**Reframe:** Restate the original goal and check your current action against it. Cut anything that's wandered off-objective.

*Why: sub-goals are generated faster than they are retired.*

### Say-Do Gap (D4)

**Fires when:** Reasoning says one thing; the action does another.

**Reframe:** Make your action match your stated reasoning. If they diverge, reconcile them before proceeding.

*Why: a stated reason is not evidence about the action taken.*

## Maintenance

Every rule carries its reason. A rule whose reason no longer holds can be deleted; a
rule whose reason was never recorded cannot be deleted safely, which is how files like
this grow without bound. Do not add a rule without one.

Triggers are stated as conditions, not as directives to follow a standard. A standing
positive directive ("follow the style guide", "write clean code") does not belong here —
the reframes are positive because they are applied at a detection point, not carried as
persistent context.
