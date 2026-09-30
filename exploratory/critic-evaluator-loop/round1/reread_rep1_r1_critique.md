# Design Review: Errors and Contradictions

## 1. Stage 4's timeout fallback violates the document's own "no silent fallback" policy

**Quote:** *"If JEV times out, forward the request with the account's default model so the user is never blocked."*

**What's wrong:** This directly contradicts the explicit error policy stated earlier: *"If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select."* The document even names this exact behavior as the thing being replaced: *"This replaces the prototype's silent default-model fallback."* Stage 4 quietly reintroduces the prototype flaw it claims to have eliminated, and it violates the top-level requirement that JEV be consulted before *every* outbound inference attempt.

**Evidence:** Both statements appear in the same document — one in "Errors and user overrides," the other in the Stage 4 table — with no reconciliation.

**Fix:** Remove the timeout auto-fallback from Stage 4, or explicitly redefine it as the "availability-oriented fallback" the document says "must be evaluated and accepted as such," with its own visible logging/labeling and its own gate before being enabled.

## 2. The accuracy threshold is stated three inconsistent ways

**Quote:** *"maintaining task accuracy at or above 85%"* (Section 1) vs. *"separate measured verdicts for faster, cheaper, and accuracy above 85%"* (also Section 1) vs. *"The user's hard requirement is accuracy strictly greater than 85%"* (Section 5).

**What's wrong:** "At or above 85%" (≥85%) and "above 85%" / "strictly greater than 85%" (>85%) are different acceptance criteria, and the first two appear in the same section. A task with measured accuracy of exactly 85% would pass under one wording and fail under another.

**Evidence:** All three phrasings are verbatim in the document as quoted.

**Fix:** Pick one threshold and one comparison operator, state it once in Section 1, and have every later section (statistical rule, release gate) reference that single definition rather than restating it.

## 3. The timing baseline contradicts the stated current default model

**Quote:** *"The latest user experience favors Astra over Sol; inventory and freeze the actual setting rather than hard-coding the prior Sol probe as the baseline."* vs. *"Use Sol at high effort as the timing baseline."*

**What's wrong:** Section 4 explicitly warns against hard-coding Sol as the baseline and says to freeze whatever the user's actual current setting is (implied to be Astra). Section 5's "Faster" methodology then hard-codes Sol anyway — precisely the mistake just warned against.

**Evidence:** Both sentences appear verbatim, one in Section 4, one in Section 5.

**Fix:** Delete the hard-coded "Sol at high effort" baseline; replace with "use the actual/current default model and effort inventoried in Stage 1," consistent with the Section 4 instruction.

## 4. Pilot sample size is given two contradictory values, and the document flags its own inconsistency without fixing it

**Quote:** *"Run a representative pilot of about 200 tasks..."* (Stage 5 table) vs. *"Start with a small pilot (approximately 20 tasks)... The earlier '200 tasks' was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power."* (Accuracy section)

**What's wrong:** The Stage 5 exit-gate table still instructs using ~200 tasks, while Section 5 explicitly disavows that number as unvalidated and substitutes ~20. As written, an implementer following the stage table and an implementer following the accuracy section would run different pilots.

**Evidence:** Both figures are verbatim in the document, with the second explicitly naming and rejecting the first.

**Fix:** Update the Stage 5 table to say "small pilot (~20 tasks, see Section 5 Accuracy for sizing rationale)" so the two sections agree.

## 5. The behavioral test matrix requires JEV decisions to recursively require JEV decisions

**Quote:** *"JEV's own decision requests do not recursively route through JEV."* (Section 1) vs. *"Include tools, subagents, retries, any separate inference endpoints, and JEV's own decision requests, each of which must also be preceded by a JEV decision."* (Behavioral test matrix, "Per-call coverage")

**What's wrong:** Section 1 explicitly carves JEV's own decision calls out of the "every call is routed by JEV" requirement. The test matrix then requires exactly the opposite — that JEV's own decision requests be preceded by a JEV decision — which is both a direct contradiction and a logical impossibility (infinite regress: which JEV call decides the model for the JEV call that decides...).

**Evidence:** Both clauses are verbatim.

**Fix:** Remove "and JEV's own decision requests, each of which must also be preceded by a JEV decision" from the coverage oracle; JEV's own calls should instead be tested for *fixed, out-of-band routing* (e.g., always the JEV key/model), not for JEV-decision coverage.

## 6. The "cheaper" cost formula double-counts tokens the document says not to double-count

**Quote:** *"Cached-input and reasoning-output counts may be subsets of their corresponding totals; do not sum them again."* (Required storage section) vs. *"Total model tokens per task = input + cached-input + output + reasoning-output tokens."* (Cheaper section)

**What's wrong:** If cached-input tokens are a subset of input tokens and reasoning-output tokens are a subset of output tokens (as stated), then the formula `input + cached-input + output + reasoning-output` counts those subset tokens twice, inflating the token total and corrupting the per-task cost figure the "cheaper" verdict depends on.

**Evidence:** Both statements are verbatim, in the same document, about the same fields.

**Fix:** Define the formula from provider-reported totals only (`input_total + output_total`, or whatever the upstream's non-overlapping total field is), and report cached/reasoning subsets separately as breakdowns, not additive terms.

## 7. The claim that the official Responses proxy already forwards all inference paths (including WebSocket) is unsupported by its own citation and pre-empts an unproven gate

**Quote:** *"The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2. [S2]"*

**What's wrong:** The Sources section's own description of S2 says only that the proxy example *"demonstrates a general Responses proxy for Codex traffic, not proof that this user needs a new key"* — nothing about covering "all" inference paths or WebSocket specifically. This also contradicts the document's own caution elsewhere (*"A public source branch is not proof that the installed desktop build behaves identically"*) and the prototype-gap finding that WebSocket handling is unqualified. It effectively asserts the outcome of Stage 2 ("prove transparent transport") before that gate has been run.

**Evidence:** Compare the Section 3 sentence to the S2 bullet in Sources, and to the "Incomplete protocol coverage" bullet in Section 2.

**Fix:** Downgrade to "the official proxy is a candidate transport to investigate in Stage 2; it has not been confirmed to cover WebSocket or all inference paths for this installed build," and remove the "so it can serve as the transport layer" conclusion until Stage 2 evidence exists.

## 8. The "single upstream endpoint, only credential differs" simplification is undercut by the same source's mention of a dedicated auth-translation proxy

**Quote:** *"current public Codex source sends both ChatGPT-authenticated and API-key traffic to the same `https://api.openai.com/v1` endpoint; only the credential differs. A proxy design can therefore use a single upstream base URL."*

**What's wrong:** If ChatGPT-session auth and API-key auth were truly interchangeable modulo one header swap, there would be little reason for OpenAI to ship a separate "Responses API proxy" (cited as S2 in the very same paragraph) whose purpose is exactly to bridge ChatGPT auth into the Responses API. The existence of that dedicated proxy suggests real translation is needed, not a trivial credential swap — undermining the confidence with which "a single upstream base URL" is proposed as a design conclusion.

**Evidence:** S2's own two parts (model-provider source vs. responses-api-proxy) are in tension with the simplified claim drawn from them.

**Fix:** State this as a hypothesis to be confirmed in Stage 1/2 ("appears to share an endpoint; verify whether ChatGPT-session auth is accepted directly or requires the proxy's translation step"), not as an established fact supporting the architecture choice.

## 9. The JEV token-billing claim is stated as settled fact without verification, and is a substantive assumption the cost model depends on

**Quote:** *"JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"*

**What's wrong:** LLM-style APIs typically bill input and output tokens at different (often several-fold different) rates, so this "same rate" claim is a strong, checkable, and commonly-false assumption. Since the whole "cheaper" verdict depends on correctly accounting for JEV's own cost, an incorrect equal-rate assumption would systematically bias that verdict.

**Evidence:** The claim is presented as a flat fact ("bills... at the same per-token rate") rather than as something confirmed against the live S3 schema; general pricing practice for input vs. output tokens contradicts the "same rate" premise.

**Fix:** Pull the actual per-token input/output rates from the S3 API response used for billing, verify whether they're equal, and compute JEV cost as `input_tokens × input_rate + output_tokens × output_rate` rather than assuming a single shared rate.