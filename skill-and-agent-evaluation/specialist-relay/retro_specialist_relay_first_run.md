# Retro: first specialist-relay run (corpus-librarian audit)

## What happened

Ran `specialist-relay` Phase 1 (fresh-eyes audit) against the `corpus-librarian`
skill, three rounds, as the first genuine multi-agent (`host.delegate`) test in
this project.

| Round | Verdict | Outcome |
|---|---|---|
| 1 | Blocking | Real defect: "the channel" mechanism was never defined. Fixed — named `host.delegate`/`host.send_message`/`host.collect`. |
| 2 | Blocking | Real defects: missing `profile` example; no `timeout`/status-check on the retrieval call. Fixed. |
| 3 | Blocking (false positive) | Auditor (a depth-capped leaf sub-agent) tested `host.delegate`/`host.collect` directly, got a root-only denial and a generic `AttributeError`, and generalized its own restricted frame's method surface into "these don't exist on the platform." Verified false by direct root-frame use earlier in the same session. Not applied. |

Final published `corpus-librarian`: artifact `1cb920b9-c990-4f69-9eab-925f081656ca`, v3.

## Failure-mode diagnosis (agent-failure-modes)

Round 3's auditor: **B1 — Shape of the Data** (reasoning stage) — reasoned only
over what was in hand (its own frame's method list) and assumed nothing
important was missing (that a root frame might have more). Secondary lens:
**C1 — Unchecked Premise** — the untested assumption underneath an otherwise
real check was "my frame's capabilities ≡ the platform's/target frame's
capabilities." Norman classification: **mistake**, not slip — the test
execution was flawless; the world-model it was built on was false.

## Retro-triage disposition

| Incident | Slip/Mistake | Existing rule that failed to fire | Placement | Tier | Status |
|---|---|---|---|---|---|
| Auditor generalized its own frame's API-access denial into a platform-wide nonexistence claim | Mistake (B1) | `FRESH_EYES_AUDITOR`'s "check against source" rule fired but had no frame-depth caveat | `FRESH_EYES_AUDITOR` system prompt + `specialist-relay` Phase 1 gate | Warning device (amend existing lines, no new pattern) | **Applied** |

### Patches applied

1. **`FRESH_EYES_AUDITOR` system prompt** — amended the "check against source"
   bullet with an exception: claims about orchestration primitives
   (`host.delegate`, `host.collect`, `host.send_message`, ...) cannot be
   self-verified by a sub-agent, because its own frame may be depth-capped
   relative to the frame that will actually run the audited document. The
   auditor now reports these as "unverifiable from this frame — needs
   dispatcher confirmation" rather than asserting nonexistence.

2. **`specialist-relay` SKILL.md, Phase 1 "The gate"** — amended to add: an
   item the auditor flags as "unverifiable from this frame" is not
   self-resolving; the dispatcher checks it against the session's own
   evidence before accepting it as a gate-stopping defect.

### DO-NOT-EXTRACT (no mechanism, first occurrence)

- Round 1 reviewer: blocking-list not ordered to match its own stated
  `breaks_at` values — low severity, single occurrence, habit-tier.
- Round 3 reviewer: `deviations: ["none"]` despite substituting an indirect
  source for a signature claim — low severity, single occurrence, habit-tier.

## Why this matters going forward

Any skill whose correctness depends on orchestration primitives
(`host.delegate`/`host.collect`/`host.send_message`/`host.children`) cannot
have those specific claims verified by dispatching a plain sub-agent auditor —
the auditor may be structurally incapable of accessing the primitive it's
being asked to check. Verification of that class of claim has to happen at
the dispatcher (root) level, or be explicitly deferred to it.
