# Review Findings

## 1. Stage 4 reintroduces the exact silent fallback the design forbids

> "If JEV times out, forward the request with the account's default model so the user is never blocked."

This directly contradicts the policy stated earlier in the same document:

> "If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select."

**Evidence:** Both statements are in the document itself (Section 3 "Errors and user overrides" vs. Section 4 Stage 4 row). Section 3 even anticipates this exact scenario and requires it to be "evaluated and accepted" as a deliberate exception — Stage 4 just does it unconditionally as an implementation detail, violating the non-negotiable "consult JEV before every outbound inference attempt" requirement from Section 1.

**Fix:** Remove the unconditional default-model fallback from Stage 4, or explicitly promote it to a named, evaluated exception per Section 3's own rule, with its own coverage-gap accounting.

## 2. The Responses-API-proxy claim is fabricated relative to S2

> "The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2. [S2]"

**Evidence:** S2's `responses-api-proxy/README.md` states it "only forwards `POST` requests to `/v1/responses`" and "Everything else is rejected with `403 Forbidden`" — no WebSocket support is mentioned anywhere. It also reads a **static `OPENAI_API_KEY` from stdin** and injects `Authorization: Bearer <key>`, explicitly stripping any incoming `Authorization` header ("All original request headers (except any incoming `Authorization`) are forwarded upstream") — it does not carry ChatGPT sign-in at all; it requires a separate API key, the very thing Section 1 says is "not a design prerequisite."

**Fix:** Correct the claim to state the proxy is a single-path (`POST /v1/responses`), API-key-authenticated HTTP forwarder with no WebSocket support, and drop it as a stage-2 transport candidate unless ChatGPT-auth forwarding is separately implemented.

## 3. Claimed single upstream base URL is contradicted by S2's own code

> "current public Codex source sends both ChatGPT-authenticated and API-key traffic to the same `https://api.openai.com/v1` endpoint; only the credential differs. A proxy design can therefore use a single upstream base URL."

**Evidence:** `model-provider-info/src/lib.rs` (`to_api_provider`) shows:
```rust
let default_base_url = if matches!(auth_mode, Some(AuthMode::Chatgpt | ...)) {
    CHATGPT_CODEX_BASE_URL   // "https://chatgpt.com/backend-api/codex"
} else {
    "https://api.openai.com/v1"
};
```
ChatGPT-authenticated traffic goes to a **different** base URL (`chatgpt.com/backend-api/codex`) than API-key traffic (`api.openai.com/v1`). The Sources section repeats this same error: "a single default backend shared by ChatGPT and API authentication."

**Fix:** State that base URL depends on auth mode; the router must handle two upstream endpoints (or dynamically select based on the auth mode in use), not assume one.

## 4. The stage-2 feasibility gate uses a config key Codex ignores at that scope

> "Repeat in the desktop surface using a reversible test configuration: put the router's `model_providers` entry in a project-local `.codex/config.toml` inside the test repository, so the user-level `~/.codex/config.toml` is never touched. [S1]"

**Evidence:** S1 (config-advanced and config-reference) both explicitly state: "Codex ignores the following keys in project-local `.codex/config.toml` and prints a startup warning when it sees them: `openai_base_url`, `chatgpt_base_url`, ..., `model_provider`, `model_providers`, ..." Setting `model_providers` at the project level will be silently ignored (with only a startup warning), so this "reversible test" would never actually route traffic through the custom provider — it would appear to run normally against the real backend while the team believes it's testing the router.

**Fix:** Use `~/.codex/config.toml` (or a `--profile`/`-c` override) for the `model_providers` entry, and treat "never touching user-level config" as incompatible with testing a custom provider — pick a different reversibility mechanism (e.g., a dedicated profile file, restored after the test).

## 5. JEV token-billing claim contradicts the cited API spec

> "JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"

**Evidence:** S3's `Usage` schema states for `output_tokens`: "Output tokens are currently free of charge." Input and output tokens are not billed at the same rate — output is free.

**Fix:** Cost per decision should be `input_tokens × rate` only (with output tokens tracked but not costed), pending confirmation of current pricing.

## 6. Claim about missing `choice` field contradicts the schema

> "The typed choice response omits `choice` when no candidate is clearly preferred; treat a missing choice as a JEV failure. [S3]"

**Evidence:** S3's `ChoiceAnswer` schema lists `"required":["choice","confidence","probabilities","type"]` — `choice` is always required and cannot be omitted. Low confidence in an ambiguous case is expressed via `confidence`/`probabilities`, not by omitting `choice`.

**Fix:** Replace with the actual signal: treat a low `confidence` (or near-uniform `probabilities`) as the "not clearly preferred" case, not a missing field; reserve "JEV failure" for schema/validation errors or HTTP failures.

## 7. Direct contradiction on whether JEV's own calls are routed through JEV

Section 1: "JEV's own decision requests do not recursively route through JEV."

Section 5 (behavioral test matrix, "Per-call coverage" row): "Include tools, subagents, retries, any separate inference endpoints, **and JEV's own decision requests, each of which must also be preceded by a JEV decision.**"

**Evidence:** These are two flatly opposed rules within the same document — one exempts JEV's own calls to prevent infinite recursion, the other requires them to be preceded by a JEV decision (which would recurse).

**Fix:** Remove the test-matrix requirement for JEV's own decision calls, or rephrase it to something like "verify no infinite recursion occurs and JEV calls are correctly excluded from coverage counting," consistent with Section 1.

## 8. Baseline model contradiction: Sol vs. Astra

Section 4: "The latest user experience favors Astra over Sol; inventory and freeze the actual setting **rather than hard-coding the prior Sol probe as the baseline**."

Section 5 ("Faster"): "Use **Sol** at high effort as the timing baseline."

**Evidence:** Section 4 explicitly warns against exactly what Section 5 then does — hard-code Sol as the baseline instead of the user's actual (Astra) configuration.

**Fix:** Make the "Faster" baseline read "Use the frozen actual baseline model/effort from Stage 1 (currently Astra at high effort)," removing the hard-coded "Sol."

## 9. Accuracy threshold contradiction: ≥85% vs. >85%

Section 1: "maintaining task accuracy **at or above 85%**."

Section 5: "The user's hard requirement is accuracy **strictly greater than 85%**."

**Evidence:** These are different thresholds (a value of exactly 85% passes one and fails the other). This is a materially meaningful discrepancy for a pass/fail release gate.

**Fix:** Pick one exact wording of the user's requirement and use it consistently everywhere it's cited (goal statement, gate criteria, and statistical test description).

## 10. Token-count source misattributed to the wrong telemetry event

> "If enabled, per-attempt token counts come from the `codex.api_request` event, which reports usage for each API request attempt. [S5]"

**Evidence:** S5 lists event contents explicitly: `codex.api_request` covers "(attempt, status/success, duration, and error details)" — no tokens. Token counts are attributed to a different event: `codex.sse_event` "(stream event kind, success/failure, duration, **plus token counts on `response.completed`**)."

**Fix:** Correct the source to `codex.sse_event`'s `response.completed` payload, and re-check the downstream design (join keys, per-attempt view) that assumed `codex.api_request` carries usage.

## 11. Pilot size contradiction: 200 tasks vs. 20 tasks

Section 4, Stage 5: "Run a representative pilot of **about 200 tasks** to find instrumentation errors and calibrate model descriptions."

Section 5 ("Accuracy"): "Start with a small pilot (**approximately 20 tasks**)... The earlier '200 tasks' was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power."

**Evidence:** The document explicitly repudiates the "200 tasks" figure as unvalidated in one section while leaving it unchanged as the plan-of-record in the implementation stage table — an unresolved self-contradiction that will confuse whoever executes Stage 5.

**Fix:** Update the Stage 5 table row to match the corrected ~20-task pilot guidance (or explicitly reconcile the two numbers if they're meant to describe different things, e.g., pilot vs. final sample).

## 12. Sources section repeats the single-backend error independently

> "**S2:** ... a single default backend shared by ChatGPT and API authentication."

**Evidence:** Same issue as #3 — this citation gloss itself misstates what the linked `lib.rs` shows (two distinct base URLs by auth mode), so the error isn't confined to the body text; the source annotation itself needs correcting.

**Fix:** Reword the S2 annotation to note the auth-mode-dependent base URL split, matching the corrected body text from issue #3.