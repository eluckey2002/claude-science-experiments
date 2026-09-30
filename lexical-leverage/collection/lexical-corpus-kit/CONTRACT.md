# Record contract (v1)

One JSON object per line (JSONL), UTF-8. Every field below is REQUIRED unless marked optional.

| field | type | meaning |
|---|---|---|
| `doc_id` | string | `sha256(source + ":" + url)[:24]` — stable across re-runs |
| `source` | string | one of `github`, `reddit`, `web` |
| `subsource` | string | github: filename kind (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `copilot-instructions.md`); reddit: subreddit; web: source key from web_sources.yaml |
| `url` | string | canonical URL of the document (github: html_url of the blob at the fetched sha) |
| `retrieved_at` | string | ISO-8601 UTC |
| `text` | string | the document body, plain text. github: raw file; reddit: title + selftext (+ top comments, separated by `\n\n---\n\n`); web: extracted main text |
| `text_sha256` | string | sha256 of `text` — used by dedup for exact duplicates |
| `n_chars` | int | len(text) |
| `license_or_terms` | string | github: repo `license.spdx_id` or `NOASSERTION`; reddit: `reddit-api-terms`; web: `robots-allowed` plus the source's stated terms if known |
| `meta` | object | source-specific extras (optional keys; never required by the analysis side): github `{repo, stars, path, sha, size}`; reddit `{post_id, created_utc, score, num_comments, is_brief}`; web `{title, fetched_status}` |

Rules
- `text` must be the document as retrieved. No summarisation, no translation, no cleanup beyond
  whitespace normalisation and (web only) boilerplate removal by trafilatura.
- Documents under 40 characters are dropped at collection time (not at analysis time), logged as `too_short`.
- A record must be reproducible: `url` + `meta.sha` (github) or `meta.post_id` (reddit) must be enough
  to re-fetch the same document.
- The analysis side reads ONLY: `doc_id, source, subsource, text, n_chars, license_or_terms`. Everything
  else is provenance for audit.
