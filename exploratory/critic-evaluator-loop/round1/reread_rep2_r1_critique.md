Reviewed the document for internal contradictions and unsupported factual claims. Findings below, most important first.

---

**1. JEV's own decisions are required to be routed through JEV, creating infinite regress**

> "JEV's own decision requests do not recursively route through JEV."

versus the behavioral test oracle:

> "Include tools, subagents, retries, any separate inference endpoints, and JEV's own decision requests, each of which must also be preceded by a JEV decision."

**What's wrong:** Section 1 explicitly carves JEV's own decision calls out of the routing requirement (necessarily — otherwise every JEV call would need a preceding JEV call, forever). The Per-call-coverage test in Section 5 demands the opposite: that JEV decision requests themselves be "preceded by a JEV decision." Taken literally this is not just an inconsistency but a logical impossibility.
**Evidence:** Direct textual contradiction between Section 1's stated exemption and the Section 5 oracle.
**Fix:** Remove "and JEV's own decision requests" from the Per-call-coverage oracle, and instead add a test asserting that JEV decision calls are *excluded* from the routed-attempt count, matching Section 1.

**2. Stage 4 reintroduces the exact silent fallback the design explicitly bans**

> "If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select."

versus:

> "If JEV times out, forward the request with the account's default model so the user is never blocked."

**What's wrong:** A JEV timeout is a case of "cannot return a valid choice within the bounded attempt policy." The stated policy requires a routing error in that case; Stage 4 instead specifies exactly the "silent fallback to a model JEV did not select" that the document bans elsewhere, and that it separately says "must be evaluated and accepted as such" before being introduced. The test matrix reinforces the ban: "Timeout, malformed output, unauthorized ID, and API errors cannot generate an unselected-model call."
**Evidence:** Section 3 "Errors and user overrides," the JEV-failure row of the test matrix, and Stage 4's implementation instruction all conflict.
**Fix:** Delete the timeout-fallback sentence from Stage 4, or explicitly flag it as the separately-evaluated "availability-oriented fallback exception" mentioned in Section 3, gated behind its own approval and a distinguishing log field.

**3. Cost formula double-counts token subsets the document says not to sum**

> "Cached-input and reasoning-output counts may be subsets of their corresponding totals; do not sum them again."

versus:

> "Total model tokens per task = input + cached-input + output + reasoning-output tokens."

**What's wrong:** The storage section states cached-input tokens are already inside the input-token total and reasoning-output tokens are already inside the output-token total, and forbids re-summing them. The Cheaper section's formula does exactly that, inflating "total model tokens" (and any derived dollar estimate) by double-counting two fields.
**Evidence:** Direct contradiction between the "Required storage" section and the "Cheaper" section's formula.
**Fix:** Use `total = input + output` (already inclusive), or if a cost-model needs cached/reasoning tokens broken out at different rates, compute `cost = (input - cached_input)×rate_in + cached_input×rate_cached + (output - reasoning_output)×rate_out + reasoning_output×rate_reasoning` — never add the subset counts on top of the totals containing them.

**4. Accuracy pass/fail boundary is stated two different ways**

> "maintaining task accuracy at or above 85%"

versus:

> "The user's hard requirement is accuracy strictly greater than 85%."

**What's wrong:** "At or above 85%" (≥85%) and "strictly greater than 85%" (>85%) disagree at exactly 85.0%, which matters for a binary release gate.
**Evidence:** Section 1 vs. Section 5 "Accuracy."
**Fix:** State one boundary condition consistently in both places, and make sure the "lower 95% CI bound exceeds 85%" release rule references the same boundary.

**5. Timing baseline contradicts the explicit instruction not to hard-code it**

> "The latest user experience favors Astra over Sol; inventory and freeze the actual setting rather than hard-coding the prior Sol probe as the baseline."

versus:

> "Use Sol at high effort as the timing baseline."

**What's wrong:** Section 4 explicitly forbids hard-coding Sol as the baseline and says to freeze whatever the user's actual current setting is (stated to now be Astra). Section 5's "Faster" methodology does precisely what was forbidden.
**Evidence:** Section 4 vs. Section 5 "Faster."
**Fix:** Replace "Use Sol at high effort as the timing baseline" with "Use the frozen actual-workflow baseline model/effort established in Stage 1."

**6. Pilot size is specified two different ways, and the stage gate was never updated**

> "Run a representative pilot of about 200 tasks to find instrumentation errors and calibrate model descriptions." (Stage 5 exit-gate table)

versus:

> "Start with a small pilot (approximately 20 tasks)... The earlier "200 tasks" was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power." (Accuracy section)

**What's wrong:** The document itself flags 200 as unvalidated, but the Stage 5 table — which actually gates advancement — still requires "about 200 tasks," leaving it unclear which number governs whether the project can proceed.
**Evidence:** Section 4 Stage 5 table vs. Section 5 "Accuracy."
**Fix:** Update the Stage 5 table to "~20-task pilot for instrumentation/calibration, then a separately sized held-out evaluation," matching the Accuracy section.

**7. Overclaim that the official Responses proxy already covers "all" paths including WebSocket**

> "The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2. [S2]"

**What's wrong:** The Sources list describes S2's proxy example only as "a general Responses proxy for Codex traffic, not proof that this user needs a new key" — no claim about covering all paths or WebSocket. This also contradicts the document's own repeated caution elsewhere that WebSocket coverage, compaction, cancellation, etc. "have not been qualified" and that public source doesn't certify installed-build behavior.
**Evidence:** Sources section's own S2 description vs. the body text's confident claim; internal tension with the "Incomplete protocol coverage" gap.
**Fix:** Soften to describe only what the example actually demonstrates (HTTP forwarding under ChatGPT auth), and require Stage 2/3 to explicitly test WebSocket coverage before depending on it.

**8. JEV per-token billing symmetry stated as fact without hedging**

> "JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"

**What's wrong:** This feeds directly into the "cheaper" verdict but asserts an unusual billing structure as settled; most token-billed APIs price input and output differently (often output costs more). If the true rates differ, this formula silently misstates JEV's contribution to cost, without any flag that it's an assumption.
**Evidence:** Presented as unqualified fact in a section that elsewhere insists on separating estimates from verified numbers ("API-equivalent dollar estimates are explicitly estimates").
**Fix:** Store `input_rate` and `output_rate` separately, confirm them against JEV's actual pricing documentation, and only use a single combined rate if explicitly confirmed symmetric.

**9. `codex.api_request` event described with more certainty than the surrounding hedge or the source list supports**

> "It does not yet verify per-inference IDs or their visibility at the proxy." ... "If enabled, per-attempt token counts come from the `codex.api_request` event, which reports usage for each API request attempt. [S5]"

**What's wrong:** The document explicitly says per-inference visibility at the proxy is *not yet verified*, then in the very next paragraph confidently names a specific event and grain of usage detail — exactly the granularity just called unverified. The Sources section's own paraphrase of S5 is more hedged ("Exact per-request correlation still requires installed-client evidence").
**Evidence:** Adjacent paragraphs conflict in confidence level; Sources list vs. body text mismatch.
**Fix:** Rephrase as a hypothesis to confirm in Stage 1 ("S5 describes a `codex.api_request` event reportedly carrying per-request usage; must be confirmed against the installed client before being relied on"), not as an established mechanism.

**10. WebSocket treated as a confirmed Codex transport without supporting evidence**

> "A WebSocket connection can carry many inference attempts; routing must happen for each creation message."

**What's wrong:** WebSocket is built into the routing requirements, storage schema, and test matrix as if already established, but neither cited source (S1: custom provider URLs/Responses protocol; S2: shared HTTP backend) describes WebSocket as part of Codex's inference transport. If Codex doesn't actually use WebSocket for inference, several requirements are designed around a nonexistent transport.
**Evidence:** No source in the Sources list supports a WebSocket inference path; contrasts with the otherwise careful "not yet qualified" framing used for other unverified protocol claims.
**Fix:** Mark WebSocket support as an open question for Stage 1's protocol inventory rather than a given, and don't finalize storage/test requirements around it until confirmed.