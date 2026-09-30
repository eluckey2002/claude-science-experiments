# Review Findings

## 1. The "official Responses proxy" claim is fabricated and contradicts its own source

> "The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2. [S2]"

**What's wrong:** Every element of this sentence is contradicted by the cited README. The proxy (a) accepts **only** `POST /v1/responses` and returns `403` for everything else — not "all Codex inference paths"; (b) has no WebSocket handling at all; (c) authenticates with a raw `OPENAI_API_KEY` piped via stdin, not ChatGPT sign-in — the README explicitly frames it as being run by a privileged user "with access to `OPENAI_API_KEY`."

**Evidence:** S2 README: "Accepts exactly `POST /v1/responses`... For other requests, it responds with `403`," and "designed to be run by a privileged user with access to `OPENAI_API_KEY`."

**Fix:** Remove this sentence. If a proxy transport is wanted for stage 2, describe it accurately as an API-key-based, single-endpoint reference proxy that would need to be extended (WebSocket, ChatGPT auth, arbitrary paths) before it could serve this design — or drop it and build the transport qualification directly against Codex's real provider config.

## 2. Upstream base URL claim contradicts the cited source code

> "current public Codex source sends both ChatGPT-authenticated and API-key traffic to the same `https://api.openai.com/v1` endpoint; only the credential differs. A proxy design can therefore use a single upstream base URL."

**What's wrong:** `to_api_provider` picks `CHATGPT_CODEX_BASE_URL` ("`https://chatgpt.com/backend-api/codex`") for ChatGPT-mode auth (`Chatgpt`, `ChatgptAuthTokens`, `Headers`, `AgentIdentity`, `PersonalAccessToken`) and only falls back to `https://api.openai.com/v1` otherwise. These are two different hosts and paths, not one.

**Evidence:** S2 `lib.rs`: `let default_base_url = if matches!(auth_mode, Some(AuthMode::Chatgpt | ...)) { CHATGPT_CODEX_BASE_URL } else { "https://api.openai.com/v1" };`

**Fix:** State that ChatGPT-authenticated and API-key traffic use **different** upstream endpoints, and that the router must map/preserve both, not assume a single base URL.

## 3. Project-local config trick for stage 2 is invalid per Codex's own config rules

> "put the router's `model_providers` entry in a project-local `.codex/config.toml` inside the test repository, so the user-level `~/.codex/config.toml` is never touched. [S1]"

**What's wrong:** S1 explicitly lists `model_providers` (and `model_provider`) among the keys Codex **ignores** in project-local `.codex/config.toml`, printing a startup warning. This "reversible test configuration" would silently do nothing.

**Evidence:** S1 config-advanced: "Codex ignores the following keys in project-local `.codex/config.toml`... `model_provider`, `model_providers`... Set provider... keys in your user-level `~/.codex/config.toml`."

**Fix:** Either accept that the custom provider must go in user-level `~/.codex/config.toml` (with an explicit backup/restore procedure), or use `--profile`/`-c` overrides for the qualification run instead of a project-local file.

## 4. JEV billing claim contradicts the cited API schema

> "JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"

**What's wrong:** The OpenAPI schema explicitly states output tokens are free.

**Evidence:** S3 `Usage.output_tokens` description: "Output tokens are currently free of charge."

**Fix:** Change the formula to `cost = input_tokens × rate` and flag output tokens as free (subject to change), sourcing this from the API description rather than an assumption.

## 5. "Missing choice" premise contradicts the schema making choice mandatory

> "The typed choice response omits `choice` when no candidate is clearly preferred; treat a missing choice as a JEV failure. [S3]"

**What's wrong:** `ChoiceAnswer.required` includes `"choice"` — the field is never optional per the schema; there is no documented "no preference" omission behavior.

**Evidence:** S3 schema: `"required":["choice","confidence","probabilities","type"]` for `ChoiceAnswer`.

**Fix:** Drop the "omits choice" premise. Instead, define the failure condition from what the schema actually allows: e.g., a returned `choice` not present in the candidate ID set, or malformed/incomplete probabilities, or an HTTP/validation error — and validate against those.

## 6. Per-attempt token usage is attributed to the wrong telemetry event

> "If enabled, per-attempt token counts come from the `codex.api_request` event, which reports usage for each API request attempt. [S5]"

**What's wrong:** Per S5, `codex.api_request` carries "attempt, status/success, duration, and error details" — no token counts. Token counts are emitted on `codex.sse_event`, specifically "plus token counts on `response.completed`" (and via `turn.token_usage` metrics).

**Evidence:** S5: "`codex.api_request` (attempt, status/success, duration, and error details)" vs "`codex.sse_event` (stream event kind, success/failure, duration, plus token counts on `response.completed`)."

**Fix:** Correct the source to `codex.sse_event`'s `response.completed` payload (and/or the `turn.token_usage` metric), and re-verify the WebSocket-transport equivalent (`codex.websocket_event`) separately, since it is not stated to carry token counts either.

## 7. Stage 4's timeout fallback directly contradicts the declared no-silent-fallback policy

> "If JEV times out, forward the request with the account's default model so the user is never blocked."

**What's wrong:** This directly contradicts the policy fixed earlier in the same document: "If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select." It also contradicts: "An availability-oriented fallback can be designed later, but it would be a visible exception... and must be evaluated and accepted as such" — Stage 4 just enacts it without that evaluation.

**Evidence:** Section 3 "Errors and user overrides" vs. Section 4 Stage 4 row.

**Fix:** Remove the silent-fallback sentence from Stage 4, or explicitly mark it as the "visible exception" the policy says must be separately evaluated and accepted, with logging that flags it as unrouted.

## 8. Token-total formula double-counts tokens the document itself warns against summing

> "Total model tokens per task = input + cached-input + output + reasoning-output tokens."

**What's wrong:** This contradicts the explicit earlier instruction that cached-input and reasoning-output are subsets of input/output and must not be summed again: "Cached-input and reasoning-output counts may be subsets of their corresponding totals; do not sum them again." Adding cached-input to input (and reasoning-output to output) double-counts tokens, inflating cost figures.

**Evidence:** Section "Required storage" vs. Section "Cheaper."

**Fix:** Change the formula to `Total = input + output` (or `= total`, if the provider directly reports a total field), with cached-input and reasoning-output reported only as informational breakdowns of those totals.

## 9. Accuracy threshold is stated inconsistently (≥85% vs. >85%)

> "maintaining task accuracy at or above 85%."

...contradicts:

> "The user's hard requirement is accuracy **strictly greater than 85%**."

**What's wrong:** Section 1 sets the non-negotiable requirement as "at or above 85%" (≥85%), while Section 5 later restates the "hard requirement" as "strictly greater than 85%" (>85%). These are different thresholds (85.0% exactly passes one and fails the other).

**Fix:** Pick one canonical threshold and use it everywhere; if the intent is ≥85%, correct Section 5's "strictly greater than" language; if it's >85%, correct Section 1.

## 10. Timing baseline model contradicts the stage-1 instruction to use the actual current setting

> "Use Sol at high effort as the timing baseline."

...contradicts:

> "The latest user experience favors Astra over Sol; inventory and freeze the actual setting rather than hard-coding the prior Sol probe as the baseline."

**What's wrong:** Section 4 explicitly warns against hard-coding the old Sol probe as baseline and says to freeze whatever the user's actual current model/effort is. Section 5 then hard-codes "Sol at high effort" as the timing baseline, exactly the mistake Section 4 warns against.

**Fix:** Make Section 5 reference "the frozen actual baseline model/effort from Stage 1," not a named model, and delete the specific "Sol at high effort" instruction (or update it consistently if Sol truly is confirmed current).

## 11. Pilot sample size is given as two different numbers without reconciling the stage table

> "Run a representative pilot of about 200 tasks to find instrumentation errors and calibrate model descriptions."

...contradicts:

> "Start with a small pilot (approximately 20 tasks)... The earlier “200 tasks” was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power."

**What's wrong:** Section 5 explicitly disavows the "200 tasks" figure as unvalidated, but Stage 5 of the implementation table (Section 4) still specifies "about 200 tasks" as the required pilot size, without being updated to match the correction.

**Fix:** Update the Stage 5 table entry to say "≈20-task pilot per Section 5, with final sample size set by power analysis," so the plan and the evaluation section agree.

## 12. "No API key" premise conflicts with relying on an API-key-only proxy as transport

> "A separate generation API key is **not a design prerequisite**."

**What's wrong:** This is presented as an open design property, but Section 3 simultaneously proposes using "the official Responses proxy" as the stage-2 transport layer — a tool that (per S2) fundamentally requires an `OPENAI_API_KEY`. If that proxy is actually adopted, the "not a prerequisite" framing is false; the document doesn't reconcile the two.

**Evidence:** Section 1 vs. Section 3's reliance on S2's proxy (see Issue 1).

**Fix:** Once Issue 1 is corrected (dropping or accurately re-scoping the proxy proposal), re-confirm whether any remaining proposed transport requires an API key, and make Section 1's claim conditional on that outcome rather than asserted unconditionally.