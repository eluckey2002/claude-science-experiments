# Design Document Review — Issues Found

## 1. Timeout fallback contradicts the core "no silent fallback" requirement
**Quote:** "If JEV times out, forward the request with the account's default model so the user is never blocked."

**What's wrong:** This is exactly the behavior the document repeatedly forbids elsewhere.

**Evidence:** Section 3 states plainly: "If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. **No silent fallback to a model JEV did not select.**" The Behavioral test matrix reinforces this: "Timeout, malformed output, unauthorized ID, and API errors cannot generate an unselected-model call." Stage 4's own fallback is a silent, unselected-model call triggered by exactly the timeout case those passages address.

**Fix:** Remove the Stage 4 default-model fallback, or explicitly reclassify it (as Section 3 anticipates for availability fallbacks) as "a visible exception to 'JEV selects every served call'" that must itself be evaluated and accepted — not silently shipped as a blocking-avoidance measure.

---

## 2. JEV's own decision requests can't simultaneously be exempt from and require JEV routing
**Quote:** "JEV's own decision requests do not recursively route through JEV."

**What's wrong:** This directly contradicts the Behavioral test matrix's coverage oracle.

**Evidence:** The "Per-call coverage" row requires: "Include tools, subagents, retries, any separate inference endpoints, **and JEV's own decision requests, each of which must also be preceded by a JEV decision.**" If JEV's decision calls must themselves be preceded by a JEV decision, that decision call would need a preceding decision too — infinite recursion — which is precisely what the Section 1 exemption exists to prevent.

**Fix:** Remove "and JEV's own decision requests" from the coverage oracle, or restate it as "JEV's own decision requests are explicitly excluded from coverage counting, and the test must confirm no recursive JEV call is made for them."

---

## 3. Token-total formula double-counts subset fields the document says not to sum
**Quote:** "Total model tokens per task = input + cached-input + output + reasoning-output tokens."

**What's wrong:** This formula sums fields that are elsewhere explicitly labeled as subsets of other fields in the same formula.

**Evidence:** The "Required storage" section states: "Cached-input and reasoning-output counts **may be subsets of their corresponding totals; do not sum them again.**" If cached-input is a subset of input and reasoning-output is a subset of output, then `input + cached-input + output + reasoning-output` double-counts those tokens, inflating the cost figures used in the "Cheaper" verdict.

**Fix:** Define total tokens as `input + output` only, with cached-input and reasoning-output reported as informational subsets, consistent with the storage section's own rule.

---

## 4. Accuracy bar stated two different ways
**Quote:** "maintaining task accuracy at or above 85%" (Section 1)

**What's wrong:** Contradicted by Section 5's restatement of the same requirement.

**Evidence:** Section 5 says: "The user's hard requirement is accuracy **strictly greater than 85%**." "At or above 85%" (≥85%) and "strictly greater than 85%" (>85%) are different thresholds — a measured 85.0% passes one and fails the other.

**Fix:** Pick one canonical threshold and use it verbatim in both places; if there's genuine ambiguity in what the user asked for, flag that explicitly rather than stating two different numbers as both being "the requirement."

---

## 5. Pilot size given as both 200 and 20, with the document contradicting its own table
**Quote (Stage 5 exit-gate table):** "Run a representative pilot of about 200 tasks to find instrumentation errors and calibrate model descriptions."

**What's wrong:** Section 5 explicitly repudiates this same number a page later, but the table entry is never corrected.

**Evidence:** Section 5 states: "Start with a small pilot (approximately 20 tasks)... The earlier '200 tasks' was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power." The document identifies the 200-task figure as wrong but leaves it standing as the literal exit-gate requirement in the Stage 5 table.

**Fix:** Edit the Stage 5 table to say "small pilot (~20 tasks) to surface instrumentation errors, followed by a separately sized held-out evaluation," removing the stale "200" figure.

---

## 6. Timing baseline model contradicts the explicit instruction not to hard-code it
**Quote:** "Use Sol at high effort as the timing baseline."

**What's wrong:** This hard-codes exactly the model the document says must not be hard-coded.

**Evidence:** Section 4 states: "The latest user experience favors Astra over Sol; inventory and freeze the actual setting **rather than hard-coding the prior Sol probe as the baseline**," and defines baseline as "the user's actual Codex workflow and its selected model/effort, not a conveniently expensive artificial baseline." The "Faster" section's own baseline choice violates that rule outright.

**Fix:** Replace "Use Sol at high effort" with "use the frozen actual baseline model/effort determined in Stage 1/5," consistent with the rest of the document.

---

## 7. Overclaim that the official Responses proxy already handles all paths, including WebSocket
**Quote:** "The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2."

**What's wrong:** This asserts as settled fact something the document elsewhere treats as unverified, and it isn't supported by the source's own description.

**Evidence:** The Material Prototype Gaps section says: "only two HTTP paths are handled. **WebSocket messages**, request compression, compaction, cancellation, and other observed inference paths **have not been qualified**." The Sources list describes S2 only as demonstrating "a general Responses proxy for Codex traffic, not proof that this user needs a new key" — no claim about WebSocket completeness. Stage 2's exit gate still requires *proving* transparent transport, which would be redundant if this claim were already established.

**Fix:** Downgrade to "the official proxy example is a candidate transport layer to evaluate in Stage 2; its WebSocket and full-path coverage is unverified and must be confirmed by the feasibility gate, not assumed from source review."

---

## 8. JEV per-token billing-rate claim sourced to a schema spec, not a pricing source
**Quote:** "JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"

**What's wrong:** S3 ("TypeSafe OpenAPI") is described in the Sources list purely as covering "typed choice, confidence/probabilities, authentication, and usage fields" — an interface/schema document, not a pricing document. Asserting an equal input/output billing rate as fact on that basis is unsupported.

**Evidence:** No pricing information is listed among what S3 covers anywhere else in the document.

**Fix:** Either cite an actual pricing source for this claim or mark the per-token-rate assumption as unverified and require confirming it against actual JEV billing before using it in cost calculations.

---

## 9. Specific telemetry event name asserted beyond what the cited source supports
**Quote:** "If enabled, per-attempt token counts come from the `codex.api_request` event, which reports usage for each API request attempt. [S5]"

**What's wrong:** The Sources list describes S5 only generically: "conversation metadata, request/stream events, and token counts on response completion. Exact per-request correlation still requires installed-client evidence." No specific event name is corroborated by that description, and the document elsewhere insists such internal schema details are version-specific and must be re-verified, not assumed.

**Evidence:** Compare with: "These internal schemas are version-specific, so use a versioned reader and prefer a supported event export when it provides the required identities" — the specific event-name claim skips that same caution.

**Fix:** State the event name as a hypothesis to confirm against the installed client's actual telemetry output, not as an established fact.