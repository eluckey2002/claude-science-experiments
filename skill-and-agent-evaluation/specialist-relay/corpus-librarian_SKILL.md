---
name: corpus-librarian
description: "Read a corpus once with one agent, then keep it addressable via host.send_message/host.collect for repeated follow-ups instead of spawning a fresh agent per question."
---

# Corpus librarian

One agent per question makes each agent read narrowly, for its own question only. Questions about how things connect cannot be answered that way, because the connections live in the files each agent skipped.

## When to use

Both conditions must hold:

1. The corpus fits inside a single agent's read.
2. At least one question is relational — about overlaps, contradictions, gaps, lineage, or internal consistency — rather than a lookup.

If every question is a factual lookup, this saves tokens and nothing else. If the corpus is too large to read whole, this is the wrong pattern: build an index first, which is a different job.

## Steps

1. Size the corpus before committing. File count and total bytes are enough — pull them from `host.artifacts()` metadata (`size_bytes`, result `count`) if the corpus is artifacts, or a plain directory listing if it's on disk.
2. Spawn one agent with `host.delegate({"name": "Librarian", "task": "<read-only brief>"})` (the `repl` tool; a plain blocking call is fine — it returns once the librarian finishes its read). Omit `profile` unless the corpus needs a narrower reader — an unset profile gets the full default agent. Brief: read thoroughly, questions are coming afterward, re-reading will not be cheap; ask for a short orientation (no more than 250 words) in the same task text. Do not reveal the questions — a librarian that knows the questions reads for them and stops being a librarian. Capture the `frame_id` from the result; every later step addresses that same frame.
3. Read the orientation from the delegate result: `result.get("response") or result.get("structured_output")` — a call with no `output_schema` lands its reply in `response`; a call with one lands it in `structured_output` instead. Check which key is actually populated on your first call rather than assuming; this confirms the librarian read the corpus and gives you a handle on what it found.
4. For each follow-up: `host.send_message(frame_id, question)` — this resumes the (already-completed) librarian with your question as its next input — then `host.collect([frame_id], timeout=120)` to retrieve the reply. `collect`'s timeout is bounded (platform default 30s if omitted) and a resumed run may not finish inside it — check the returned `status`; if it is still `"running"` rather than `"completed"`, the payload is a not-yet-finished descriptor, not the answer, so loop `host.collect([frame_id], timeout=...)` again rather than treating it as final. Send one question per round-trip rather than batching several into one message; batching means you can't react to answer N before framing question N+1, which defeats the point of keeping the librarian open. The librarian's conversation persists across this completed-then-resumed cycle, but its kernel variables do not — if a question depends on something it computed rather than something it read from the corpus, it may need to redo that computation.
5. When an answer matters, ask (via the same send_message/collect round-trip) whether it read that or inferred it.

## Do not

- Do not use this on a corpus you are actively editing. The librarian holds a snapshot and will not know about later changes.
- Do not stretch one librarian across unrelated bodies of material. Scope by corpus, not by task.
- Do not assume the saving is the point. The reason to do this is the answers you cannot get otherwise.

## Verification

Check whether the answers contain claims that span two or more files. If they do, the pattern earned its cost. If every answer sits inside a single file, the questions were lookups and a cold agent would have done as well — note that, and skip the librarian next time for that kind of question.
