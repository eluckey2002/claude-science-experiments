 JEV model routing: design and implementation plan

**Status: planning reset, 2026-09-28.** This document replaces the earlier design. The Python files are an experimental prototype; implementation is paused while the architecture and evaluation are settled.

## 1. Outcome and non-negotiable requirements

The goal is to spend less time and money on Codex work while maintaining task accuracy above 85%.

Before **every outbound Codex inference attempt**, consult JEV about which eligible model should serve that request, then use its selection. This covers the first request, requests following tool results, additional requests within a turn, resumed work, and subagent requests. Include model-backed compaction or summarization if the client makes those calls. A streaming response is one inference attempt, not one attempt per token. A WebSocket connection can carry many inference attempts; routing must happen for each creation message.

JEV's own decision requests do not recursively route through JEV. Tool execution, authentication, model discovery, and telemetry are not generation requests. Server-internal activity that cannot be observed or controlled must be named as a coverage limitation; “every call” must never quietly become “every call our prototype happens to see.”

The target user experience includes the **Codex desktop app already in use**. CLI is a convenient integration test surface, not a substitute for desktop delivery.

Authentication has two existing paths:

- JEV decisions use the working JEV key in the existing .env file.
- Codex continues to own its current ChatGPT sign-in, renewal, account selection, and model access. The router forwards that authenticated traffic to the same legitimate Codex service.

A separate generation API key is **not a design prerequisite**. Nor is successful forwarding of the existing sign-in established yet.

Implementation must include tests and separate measured verdicts for faster, cheaper, and accuracy above 85%. No deployment claim is permitted on the strength of a mock-server test.

## 2. What the current evidence establishes

| Evidence already obtained in this chat | What it proves | What it does not prove |
| --- | --- | --- |
| Live JEV model discovery and typed choice calls succeeded | The key and the JEV choice interface work | That JEV picks the right Codex model for real work |
| Five synthetic decisions had a reported median round trip of 329 ms | A small sample of routing overhead on this machine | Representative latency, a speedup, or accuracy |
| Twelve local tests passed against fake servers | Several prototype branches and field rewrites behave as asserted | Protocol fidelity, timely streaming, real task completion, or desktop coverage |
| One disposable CLI request reached the proxy and fake upstream with JEV's selected model | CLI traffic can reach this custom provider configuration | A complete authenticated Codex turn; that probe ended in protocol errors |
| Codex reported “Logged in using ChatGPT” | Existing Codex authentication is present | Need for a second key, or end-to-end compatibility through this proxy |

These are prior tool observations, not a newly rerun benchmark. The live sample used fictional fast/strong descriptions; it has no independently labeled accuracy ground truth.

Source review also complicates the upstream: current public Codex source selects different base URLs by auth mode — ChatGPT-mode credentials (Chatgpt, ChatgptAuthTokens, Headers, AgentIdentity, PersonalAccessToken) default to the ChatGPT backend endpoint, while other credentials default to `https://api.openai.com/v1`. A proxy design must map and preserve both upstream endpoints rather than assuming a single base URL. A public source branch is not proof that the installed desktop build behaves identically. [S2]

### Material prototype gaps

These findings are from reading the current code; no production fixes were made during this planning reset.

- **Wrong continuation identity:** eligibility uses the incoming model field. If the proxy served the previous response with another model, it has no record of that effective model. Pinning continuation to the incoming field may therefore pin to the wrong model.
- **Streaming is not proven:** the relay reads 8,192-byte blocks; the test only checks eventual receipt of a tiny response. It never proves the first event reaches the client before generation ends.
- **Incomplete protocol coverage:** only two HTTP paths are handled. WebSocket messages, request compression, compaction, cancellation, and other observed inference paths have not been qualified. Upstream URLs are formed by concatenation, without a verified ChatGPT path mapping.
- **Policy differs from the design:** low confidence is parsed but never used as a threshold; there is no retry identity, retry pinning, or explicit user-pin mechanism. Error fallback can serve a model JEV did not choose.
- **Weak routing context:** the last four text fragments and 4,000 characters can omit the objective, critical instructions, or an earlier tool dependency. Character count is not a complete model context-budget check.
- **Missing outcome accounting:** logs do not establish the model actually serving the response, complete generation usage, per-task cost, or routing coverage.

The code and tests are useful fixtures and experimental evidence. They should not dictate the final architecture. In particular, keeping every continuation on one forced candidate could satisfy “consult JEV” while eliminating useful routing; the benchmark must expose that behavior.

## 3. Architecture choice

**Preferred candidate: a local provider-boundary router that preserves Codex's existing authentication and protocol.** Adopt it only after the feasibility gates below pass.

    Codex runtime prepares an inference request
      → local router derives the decision state and eligible models
      → JEV selects one model
      → router forwards the compatible request to the Codex service
      → original response stream returns to Codex
      → repeat after the next tool result or other inference trigger

Codex documents custom provider URLs and the Responses protocol. That supports investigating this boundary; it does not certify transparent model switching inside a desktop session. [S1] The official Responses proxy example, by contrast, only accepts `POST /v1/responses` (returning 403 for any other path), authenticates via a raw `OPENAI_API_KEY` rather than the existing ChatGPT sign-in, and implements no WebSocket handling; it is not evidence that a ChatGPT-authenticated, WebSocket-capable transport already exists, and would need substantial rework before it could serve as the stage 2 transport layer. [S2]

| Approach | Decision |
| --- | --- |
| Provider-boundary router | Investigate first. It can act on each request without making the reasoning model call JEV as a tool. Must prove desktop coverage and continuation compatibility. |
| Routing inside Codex's inference loop | Alternative if changing only the request's model is unsafe. It could update model-specific prompt, capability, and context settings together. A CLI fork alone would not establish desktop support. |
| Session launcher, prompt hook, or agent instructions | Does not meet the requirement: it cannot guarantee JEV runs before every internal inference request. |

Do not build both architectures in parallel. If the provider boundary fails a gate, determine whether a supported runtime extension exists. If desktop has no usable insertion point, report that specific limitation and present the runtime option; do not disguise CLI-only delivery as completion.

### Request and decision contract

For each attempt, create a correlation identity linking session, turn, logical inference, and retry attempt. Construct JEV's decision state deterministically from:

- The active objective, latest relevant request, and important instructions.
- The latest tool results and the next required work.
- Required modalities, tools, output format, context budget, and reasoning settings.
- The model that actually served the preceding response, continuation constraints, and measured switching/cache costs.
- The eligible model menu, with verified capabilities and performance descriptions.

Keep the state bounded. If the extractor cannot preserve necessary context, include only models known to handle that uncertainty. Do not add a separate LLM summarization call solely to prepare every JEV request; that would add another cost and latency path requiring its own evaluation. Prompts and tool output are task data, not authority to modify the allowlist or routing policy.

Use JEV's typed choice interface. Validate the answer against the exact candidate IDs and response schema, including finite probabilities. The typed choice schema requires `choice`, `confidence`, `probabilities`, and `type` on every response; treat a returned `choice` outside the candidate ID set, or missing/malformed probabilities, as a JEV failure. [S3] Record confidence for analysis. JEV's documented schema currently marks output tokens as free of charge, so JEV cost per decision is input_tokens × the per-token rate; verify this against current billing terms before relying on it, since it is subject to change. [S3] Do not assume a confidence of 0.85 means 85% task accuracy, or choose an arbitrary confidence threshold and call it calibrated. [S3]

### Eligibility and continuity

Only models available to this signed-in Codex account can be candidates. Verify support for the complete request: tools and schemas, image/file content, output controls, context including instructions and tool definitions, reasoning parameters, and session state. A proxy must not silently strip information to make a cheaper model accept the request.

Treat model switching as a compatibility question, not just a JSON field edit. Codex may have prepared instructions, tool definitions, or budgets for its selected model. Test that all candidates in a switching group can safely consume that prepared request.

Track the **actual served model** against response IDs and request lineage. For opaque or model-bound state, constrain eligibility to the correct prior model unless switching is demonstrated safe. Still consult JEV. Record constrained decisions separately from choices among multiple candidates. Do not clear reasoning state or discard tool history to force a switch.

A retry gets another JEV consultation before another upstream inference attempt. Restrict it to the previous selected model when needed for continuity. Resuming an existing stream is not automatically a new generation request; classify it from the protocol.

### Errors and user overrides

The proposed initial policy follows the user's literal per-call requirement:

- A valid JEV choice is used, even if confidence is low; eligibility already excludes unsupported models.
- If JEV cannot return a valid choice within the bounded attempt policy, return a recoverable routing error before generation. No silent fallback to a model JEV did not select.
- An explicit user pin narrows the eligible set and still goes through JEV. A one-candidate decision remains visible as constrained routing.
- If no eligible model exists, reject the unsupported request before generation.

This replaces the prototype's silent default-model fallback. An availability-oriented fallback can be designed later, but it would be a visible exception to “JEV selects every served call” and must be evaluated and accepted as such.

### Transport and records

Preserve the transport the client actually uses. For SSE, prove incremental delivery, cancellation, error propagation, and usage capture. For WebSockets, route each response-creation message and preserve session semantics. Do not silently force a slower transport and compare it with an unrelated baseline.

Use explicit, verified mappings between local paths and the existing Codex upstream paths. Preserve required auth/account headers and renewal behavior. Keep credentials out of decision state, logs, persisted captures, and other destinations; do not export the user's auth store into a new credential workflow.

Record attempt identity, requested/selected/served model, eligible count, routing constraints, JEV and upstream timings, usage including cached input and reasoning output when exposed, completion/error status, and evaluation outcome. Unknown costs or identity fields remain unknown, not zero. If the upstream does not expose the served model, identify exactly which evidence supports only “requested model.”

### Required storage: tokens, confidence, and Codex log correlation

Every inference attempt must have a durable local record. Store **token usage counts**, not authentication tokens or raw token text. Use a local SQLite event store with a queryable per-attempt view and JSONL export for inspection. Keep it separate from Codex's own databases; read Codex records without modifying them. Schema versioning and the installed Codex version accompany the record.

| Field group | Required stored data |
| --- | --- |
| Router identity | Unique router call ID, logical inference ID where established, attempt number, event ID, UTC timestamps, monotonic durations, and status |
| Codex identity | Native thread/session ID, turn ID, and parent/child thread relationship for subagents; capture the actual source field and mapping method |
| Request identity | Upstream response ID, upstream request ID, and trace/span IDs where exposed; preserve the values without pretending all clients provide every identifier |
| JEV decision | Requested and returned JEV model/version, selected candidate, confidence score, full per-candidate probabilities, eligible candidates, constrained-choice reason, and routing-policy version |
| JEV tokens | Reported input tokens and output tokens separately, with source and completeness status |
| Codex model tokens | Reported input tokens, cached-input tokens, output tokens, reasoning-output tokens, and total tokens where exposed; preserve the provider's field semantics |
| Outcome | Requested/selected/served generation model, latency, completion or error, cancellation state, cost basis, estimated/measured cost, and task evaluation result when available |
| Source reference | Exact native event/row identity or rollout location used for the match, Codex version, correlation status, and any unresolved mismatch |

Cached-input and reasoning-output counts may be subsets of their corresponding totals; do not sum them again. Retain usage provenance so final response usage can be distinguished from cumulative session totals. A cancellation, missing final event, or unavailable usage field is recorded as incomplete/null, never as zero. Do not add cumulative Codex counters across events. Any derived per-call delta must state its source and be tested against resets and retries.

Record request receipt, the JEV result, upstream dispatch, and terminal status as separate events under the same call ID. Durably store the decision before forwarding the generation request. If that write fails, do not silently create an untraceable inference. Deduplicate repeated terminal/usage events, retain every retry attempt, and mark interrupted records after restart rather than inventing completion data. Log persistence overhead is part of the speed benchmark.

**JEV confidence is the confidence of the routing decision.** Keep it separate from task accuracy and from the correlation status used to describe whether two logs were matched. A one-candidate result must remain labeled constrained even if its confidence is 1.0.

The intended join is:

    Codex thread → Codex turn → inference request/response
                               ↕ verified identifiers
                         router call + retry attempt
                               → JEV choice, confidence, probabilities, tokens
                               → served-model usage and outcome

Use native IDs observed in the request, response, or supported Codex telemetry. Verify which IDs are actually present at the chosen insertion point. A router-generated ID only links to Codex if a demonstrated mechanism records or maps it there; adding an arbitrary header is not sufficient evidence. Timestamps and model names are diagnostic aids, not exact join keys.

If an exact request-level join is unavailable through existing logs, investigate supported local telemetry or instrumentation at the inference boundary. Do not quietly reduce the requirement to session-level association. Report unmatched and ambiguous events explicitly, and block the “logs tied to Codex” acceptance claim until the controlled tests prove the relationship. Local telemetry export is an implementation option, not enabled by this plan. If enabled, per-attempt token counts come from the `codex.sse_event` event's `response.completed` payload (and the `turn.token_usage` metric), not from `codex.api_request`, which reports only attempt number, status, duration, and error details; whether the WebSocket-transport equivalent exposes token counts has not been confirmed and must be verified separately. [S5]

Read-only inspection on 2026-09-28 confirmed these native schema fields on this machine: logs_2.sqlite has logs.thread_id and process_uuid; state_5.sqlite has threads.id and rollout_path; thread_history_1.sqlite has thread_turns.thread_id/turn_id and thread_items.thread_id/turn_id/item_id/rollout_ordinal. This verifies that thread and turn identities exist. It does **not** yet verify per-inference IDs or their visibility at the proxy. These internal schemas are version-specific, so use a versioned reader and prefer a supported event export when it provides the required identities.

## 4. Implementation plan and exit gates

Proceed through these stages without asking the user to approve each routine step. At this planning stop, only documentation is being changed.

| Stage | Work | Required evidence before advancing |
| --- | --- | --- |
| 1. Observe the real integration surface | Inventory installed CLI and desktop versions, existing model access, provider settings, transport, inference paths, continuation representation, billing/usage fields, and exact identifiers linking requests to native logs. Use isolated tests with the existing sign-in. | A documented map of actual requests, native log identifiers, and settings. Unknown desktop behavior or missing per-request correlation is explicit. No new key is assumed. |
| 2. Prove transparent transport | Build or repair a temporary router that forwards requests unchanged, with JEV disabled only for this transport qualification. Complete a real tool loop and streamed final answer. Repeat in the desktop surface using a reversible test configuration: Codex ignores `model_provider`/`model_providers` keys in project-local `.codex/config.toml`, so the router's provider entry must instead go in the user-level `~/.codex/config.toml` (back up the existing file before the test and restore it afterward) or be supplied via a `-c`/`--profile` override for the qualification run. [S1] | Direct and proxied runs complete the same fixture; every relevant request is observed; response/tool semantics and authentication remain correct. The diagnostic mode is not claimed as the JEV use case. |
| 3. Prove safe model switching | Force known model choices in controlled fixtures before attributing anything to JEV. Test both switch directions, continuation, tool results, multimodal/large inputs, cancellation, retries, and concurrency. | Real task completion and correct request lineage for supported switching groups. No silent state loss. Quantified constraints if some calls must remain on their prior model. |
| 4. Add JEV and functional tests | Implement the decision contract, strict error policy, eligible candidate registry, durable token/confidence records, and native Codex log joins. Retain useful mock fixtures but qualify them against real traces. If JEV times out, apply the recoverable-routing-error policy from Section 3 rather than silently substituting a model; any availability-oriented fallback is the visible exception described there and must be separately evaluated and explicitly accepted before use. | Each served inference attempt has a persisted valid JEV decision, confidence and token fields, and a verified Codex log association; requested/effective model evidence agrees. All behavioral tests below pass. |
| 5. Pilot, then freeze evaluation | Run a representative pilot of approximately 20 tasks (per Section 5) to find instrumentation errors and calibrate model descriptions, then set the final held-out sample size by power analysis rather than assuming a fixed count. Separate pilot examples from final evaluation. Freeze router/version, baseline model and effort, task fixtures, oracles, budgets, billing method, and success thresholds. | A runnable, versioned evaluation with independently defined expected results and an achievable sample size. No tuning on the final held-out outcomes. |
| 6. Run the comparison and issue verdicts | Compare paired baseline and JEV runs, accounting for all calls, retries, cache effects, verification and repair. Inspect failures and constrained-call share. | Faster, cheaper, and >85% accuracy each have a PASS/FAIL/UNVERIFIED verdict with raw evidence. Do not enable the use case if any required verdict fails or remains unverified. |
| 7. Enable and retain rollback | Apply the validated desktop configuration, expose route status and a switch back to the original path, and retain outcome/usage records. | A desktop acceptance run proves coverage after activation. Restore original configuration if the gate fails. |

For stage 1, “baseline” means the user's actual Codex workflow and its selected model/effort, not a conveniently expensive artificial baseline. The latest user experience favors Astra over Sol; inventory and freeze the actual setting rather than hard-coding the prior Sol probe as the baseline.

Auth compatibility failure must be narrowed to its actual cause: provider support, URL mapping, header handling, account/model access, or transport. The absence of an API key does not establish any of those failures.

## 5. Tests and evaluation

### Behavioral test matrix

| Area | Required oracle |
| --- | --- |
| Per-call coverage | A controlled multi-step run emits independently counted inference attempts; each served attempt maps to a preceding JEV decision. Include tools, subagents, retries, any separate inference endpoints, and JEV's own decision requests, each of which must also be preceded by a JEV decision. |
| Model selection | A controlled choice is visible in the upstream request and, where available, the returned model identity. Test switching after new tool evidence and selection of each candidate. |
| Streaming | The client receives the first event before the delayed final event. Test long streams, cancellation, disconnects, and accurate completion detection. Eventual receipt alone fails this test. |
| Continuity | Switch A to B, continue from B's response while the client still requests A, and verify that state is associated with B. Exercise opaque state, resumed sessions, duplicate attempts, and interleaved sessions. |
| Capabilities | Incompatible candidates cannot be selected; complete token/context budgets and tool/format requirements are respected. No silent parameter deletion. |
| JEV failure | Timeout, malformed output, unauthorized ID, and API errors cannot generate an unselected-model call. Low confidence follows the declared policy. |
| Credential and protocol handling | Legitimate Codex auth works; secrets do not enter the JEV body or logs; body encoding, URLs, headers, model lists, and unsupported inference paths behave as specified. |
| Desktop acceptance | The actual installed desktop client completes a multi-call task through the router with matching coverage evidence. CLI success cannot substitute. |
| Token and confidence persistence | Known JEV probabilities/confidence and usage survive restart unchanged. Model input/output/cached/reasoning counts retain their source semantics. Repeated terminal events do not double-count; incomplete/cancelled streams have explicit missing usage. A storage failure before dispatch prevents an unrecorded call. |
| Codex log reconciliation | Run simultaneous threads with identical prompts, multiple turns, subagents, retries, and a cancelled stream. Every served inference attempt matches exactly one router attempt record through verified native identities, with its related Codex events. No cross-thread matches or timestamp-only joins; unmatched events are reported. Aggregate disjoint model usage agrees with the corresponding Codex scope, while JEV usage is accounted for separately. |

Tests written with the implementation are necessary but not independent evidence that the design is complete. Final verification must include an independent review or an independently prepared oracle, plus real client integration.

### Accuracy

The principal accuracy metric is **successful completed tasks / all assigned held-out tasks**, with task success defined before execution. JEV's confidence and agreement with an invented “fast/strong” label are secondary diagnostics.

Use executable task checks where possible: known expected answers, repository fixture tests, and explicit requirements. For subjective tasks, use a fixed rubric with blind independent adjudication. Count routing errors and unfinished tasks as failures. Show numerator, denominator, a binomial confidence interval, and paired quality difference from baseline.

The user's hard requirement is accuracy **strictly greater than 85%**. Proposed stronger release evidence: also require the lower one-sided 95% confidence bound to exceed 85%, and no observed task-success decline against baseline. These are design recommendations, not claims that the user requested those exact statistical rules. Critical failures must be shown individually.

Start with a small pilot (approximately 20 tasks), then choose the held-out sample size for the desired confidence and workload coverage. The earlier “200 tasks” was an unvalidated planning number, not an existing corpus or a proof of adequate statistical power. Synthetic fixtures can qualify mechanics; their results must not be represented as proven accuracy on the user's production workload.

### Faster

Measure time from task submission to a verified usable result, including JEV, network/queue time, tools, verification, and in-budget repair. Use the frozen actual baseline model and effort identified in Stage 1 (not a hard-coded prior probe) as the timing baseline. Keep identical task conditions and randomly interleave baseline and routed runs; isolate workspace state and declare warm/cold-cache handling.

Report total task time, median, p95, failure rate, timeouts, and paired uncertainty. All failed runs remain in the report; do not remove slow failures. Proposed release rule: lower paired median end-to-end time with uncertainty supporting improvement, no p95 regression, and no measured success-rate decline. The measurement is task completion speed, not JEV's classification speed.

### Cheaper

Use the billing model of the existing account:

- If usage draws paid credits or charges, compare the actual attributable amount, plus JEV charges and all retries/repairs. Report total cost and cost per successful task. Total model tokens per task = input tokens + output tokens (cached-input and reasoning-output tokens are subsets of those totals, reported separately, and must not be added again).
- If the same fixed subscription covers both runs with no additional Codex charge, routing may conserve allowance but does not itself reduce the subscription bill. Added JEV spend must still be counted.
- Report allowance/resource savings separately. API-equivalent dollar estimates are explicitly estimates; they cannot establish actual cash savings or justify requiring an API key.
- Shared account-wide usage snapshots are not per-task billing evidence when other activity is running. If attribution is unavailable, mark the corresponding money verdict UNVERIFIED.

Thus the final table may honestly say “less allowance used, cash savings unverified.” That would not satisfy a promised money-saving verdict. Codex's documented allowance/credit behavior supports making this distinction. [S4]

### Overall decision

No current faster/cheaper/accuracy verdict passes. Functional correctness alone cannot promote the router. If a benchmark fails, retain the evidence and revise a named hypothesis; do not move the threshold or choose a new baseline after seeing the result.

## 6. Deliverable and working agreement

The next implementation deliverable is an authenticated, transparent path through the user's real Codex setup with protocol and coverage evidence. JEV selection is added after that foundation and controlled model switching work.

Only genuine scope choices or hard external blockers return to the user. Routine coding, fixtures, investigation, and repairs stay agent-owned. Report measured results at meaningful milestones rather than repeatedly asking whether to do the already-agreed next step.

Existing prototype source and tests remain unchanged during this planning turn. No routing has been enabled by this plan.

## Sources

Sources were reviewed on 2026-09-28. Public source at main can differ from the installed build; pin the relevant version during feasibility work.

- **S1:** [Codex advanced configuration](https://developers.openai.com/codex/config-advanced/) and [configuration reference](https://developers.openai.com/codex/config-reference/) — custom provider URL, Responses protocol, and transport/configuration controls.
- **S2:** [OpenAI Codex model-provider source](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs) — a single default backend shared by ChatGPT and API authentication. The [official Responses proxy example](https://github.com/openai/codex/blob/main/codex-rs/responses-api-proxy/README.md) demonstrates a general Responses proxy for Codex traffic, not proof that this user needs a new key.
- **S3:** [TypeSafe OpenAPI](https://api.typesafe.ai/openapi.json) — typed choice, confidence/probabilities, authentication, and usage fields.
- **S4:** [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) and [credits for flexible usage](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans) — included usage and additional credit accounting.
- **S5:** [Codex observability and telemetry](https://developers.openai.com/codex/config-advanced/#observability-and-telemetry) — conversation metadata, request/stream events, and token counts on response completion. Exact per-request correlation still requires installed-client evidence.