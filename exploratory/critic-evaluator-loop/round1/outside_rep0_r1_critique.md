# Design Document Review: Issues Found

Below are the errors found, checked against the attached sources (S1–S5), ranked by importance. Each entry gives the exact quote, the problem, the evidence, and a fix.

---

### 1. Stage 4's timeout fallback contradicts the document's own "no silent fallback" rule
**Quote:** *"If JEV times out, forward the request with the account's default model so the user is never blocked."* (Stage 4, implementation table)

**What's wrong:** This directly reinstates the exact behavior the "Errors and user overrides" section forbids.

**Evidence (internal contradiction):** *"If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select."* The doc even explicitly says an availability fallback "would be a visible exception to 'JEV selects every served call' and must be evaluated and accepted as such" — Stage 4 smuggles it in as a *required* behavior instead.

**Fix:** Remove the fallback line from Stage 4's required work, or explicitly mark it as the separately-evaluated "availability-oriented fallback" exception, gated behind its own acceptance criteria, not baked into the default policy.

---

### 2. "JEV never routes JEV's own calls" contradicts the test matrix requiring exactly that
**Quote A (Section 1):** *"JEV's own decision requests do not recursively route through JEV."*

**Quote B (Section 5, test matrix):** *"...and JEV's own decision requests, each of which must also be preceded by a JEV decision."*

**What's wrong:** These are mutually exclusive. B requires infinite recursion (a JEV decision needs a JEV decision needs a JEV decision...) that A explicitly rules out.

**Fix:** Pick one policy — either JEV calls are exempt and logged as an explicit coverage exclusion (per Section 1), or remove the recursive requirement from the test matrix and describe how JEV-call coverage is verified without routing them through JEV.

---

### 3. Token-cost formula double-counts subset token fields it explicitly says not to sum
**Quote A:** *"Cached-input and reasoning-output counts may be subsets of their corresponding totals; do not sum them again."*

**Quote B (Cheaper section):** *"Total model tokens per task = input + cached-input + output + reasoning-output tokens."*

**What's wrong:** B sums cached-input and reasoning-output on top of input/output, which is exactly the double-counting A warns against — cached-input tokens are a subset of input tokens, and reasoning-output tokens are a subset of output tokens.

**Fix:** Change the formula to `Total model tokens per task = input tokens + output tokens`, reporting cached-input/reasoning-output separately for provenance only.

---

### 4. Official Responses proxy claim is contradicted by its own README
**Quote:** *"The official Responses proxy already forwards all Codex inference paths, including WebSocket traffic, under the existing ChatGPT sign-in, so it can serve as the transport layer for stage 2."*

**Evidence (S2, responses-api-proxy/README.md):** The proxy "Reads the API key from stdin" (not ChatGPT sign-in), and "Accepts exactly `POST /v1/responses` (no query string)... For other requests, it responds with `403`." There is no WebSocket handling anywhere in the README, and it's designed to be run by a privileged user holding `OPENAI_API_KEY` — the opposite of "under the existing ChatGPT sign-in." The Sources section itself hedges this correctly ("not proof that this user needs a new key"), contradicting the confident claim in the body.

**Fix:** Rewrite the claim to state the proxy only forwards `POST /v1/responses` using an API key, has no WebSocket support, and cannot serve as a drop-in transport for a ChatGPT-authenticated desktop session without further work.

---

### 5. "Single upstream base URL" claim is contradicted by the cited source code
**Quote:** *"current public Codex source sends both ChatGPT-authenticated and API-key traffic to the same `https://api.openai.com/v1` endpoint; only the credential differs. A proxy design can therefore use a single upstream base URL."* (also repeated in the Sources list: *"a single default backend shared by ChatGPT and API authentication"*)

**Evidence (S2, model-provider-info/lib.rs, `to_api_provider`):**
```rust
let default_base_url = if matches!(auth_mode, Some(AuthMode::Chatgpt | ... )) {
    CHATGPT_CODEX_BASE_URL   // "https://chatgpt.com/backend-api/codex"
} else {
    "https://api.openai.com/v1"
};
```
ChatGPT-authenticated traffic and API-key traffic go to **different** default base URLs. This is the opposite of what's claimed.

**Fix:** State that Codex uses two different default endpoints depending on auth mode (`chatgpt.com/backend-api/codex` vs `api.openai.com/v1`), and that the router must map both correctly, not assume one shared upstream URL.

---

### 6. Stage 2's project-local config plan is explicitly disabled by Codex's own config-loading rules
**Quote:** *"put the router's `model_providers` entry in a project-local `.codex/config.toml` inside the test repository, so the user-level `~/.codex/config.toml` is never touched. [S1]"*

**Evidence (S1, Advanced Configuration):** *"Codex ignores the following keys in project-local `.codex/config.toml` and prints a startup warning when it sees them: `openai_base_url`, `chatgpt_base_url`, ... `model_provider`, `model_providers`, ... Set provider... keys in your user-level `~/.codex/config.toml`."*

**What's wrong:** The exact key the plan proposes to set (`model_providers`) is one of the keys Codex silently ignores (with only a startup warning) at the project level. The reversible-test-config approach as described will not route anything.

**Fix:** Use `~/.codex/config.toml` (with a backup/restore step for reversibility) or `--profile`/`-c` CLI overrides instead of a project-local `.codex/config.toml` for `model_providers`.

---

### 7. JEV cost formula bills tokens that the API says are free
**Quote:** *"JEV bills input and output tokens at the same per-token rate, so JEV cost per decision is (input + output tokens) × that rate. [S3]"*

**Evidence (S3, `Usage.output_tokens`):** *"Number of output tokens used to answer the questions. **Output tokens are currently free of charge.**"*

**Fix:** Cost per decision = `input_tokens × rate` only; output tokens should be recorded for observability but excluded from the cost calculation.

---

### 8. Claim about JEV omitting `choice` is not supported by the schema
**Quote:** *"The typed choice response omits `choice` when no candidate is clearly preferred; treat a missing choice as a JEV failure. [S3]"*

**Evidence (S3, `ChoiceAnswer`):** `required: ["choice","confidence","probabilities","type"]` — `choice` is always present in a valid response. Uncertainty is signaled through the `confidence` field, not by omitting `choice`.

**Fix:** Replace with: a JEV failure is a malformed/non-conforming response (missing required fields, schema violation, or non-200), not "missing choice." Use low `confidence` — not absence of `choice` — to flag uncertain selections per the declared confidence policy.

---

### 9. Internal contradiction over which model is the timing baseline
**Quote A (Section 4):** *"The latest user experience favors Astra over Sol; inventory and freeze the actual setting rather than hard-coding the prior Sol probe as the baseline."*

**Quote B (Section 5, Faster):** *"Use Sol at high effort as the timing baseline."*

**What's wrong:** Section 4 explicitly forbids hard-coding Sol as the baseline in favor of the account's actual current setting (Astra); Section 5 then hard-codes Sol anyway.

**Fix:** Make Section 5 reference "the frozen actual baseline model/effort from Stage 1" rather than naming Sol directly, or justify explicitly why Faster testing intentionally diverges from the Stage-1 baseline rule.

---

### 10. Per-attempt token counts are attributed to the wrong telemetry event
**Quote:** *"If enabled, per-attempt token counts come from the `codex.api_request` event, which reports usage for each API request attempt. [S5]"*

**Evidence (S5, Observability and telemetry — "What gets emitted"):** `codex.api_request` carries *"attempt, status/success, duration, and error details"* — no tokens. Token counts appear on `codex.sse_event`: *"stream event kind, success/failure, duration, **plus token counts on `response.completed`**."*

**Fix:** State that per-attempt token counts, when available via OTel, come from `codex.sse_event` on `response.completed` (or `turn.token_usage` metrics), not from `codex.api_request`.

---

### 11. Pilot sample size is inconsistent between the stage plan and the evaluation section
**Quote A (Stage 5 table):** *"Run a representative pilot of about 200 tasks to find instrumentation errors and calibrate model descriptions."*

**Quote B (Section 5, Accuracy):** *"Start with a small pilot (approximately 20 tasks)... The earlier '200 tasks' was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power."*

**What's wrong:** Section 5 explicitly disavows the 200-task figure as unvalidated, but the Stage 5 implementation table — which is meant to be the operative plan — still states "about 200 tasks" as the requirement, unreconciled.

**Fix:** Update the Stage 5 table to say "pilot size per Section 5's sizing rule (initially ~20 tasks, scaled for power)" rather than leaving a stale, contradicted number in the actionable plan.

---

## Summary of fixes needed before implementation
Items 1–3 are policy-breaking self-contradictions that would make the "consult JEV before every call" and cost-accounting guarantees unenforceable as written. Items 4–6 invalidate the specific technical mechanism proposed for transport and testing (the official proxy and project-local config approach), and must be redesigned before Stage 2 work begins. Items 7–8 will cause incorrect cost/error-handling logic if implemented as described. Items 9–11 are documentation inconsistencies that should be resolved so engineers don't implement contradictory instructions.