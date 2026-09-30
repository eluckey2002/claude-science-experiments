# lexical-corpus-kit — collection side of the word-effect study

Purpose: collect the text people write when instructing agents (house-rules files) and when
briefing web design (Reddit posts, design-brief pages), in ONE fixed record format, so the
analysis side can compute keyness rankings without caring where a document came from.

This kit is the **collection** half. It does no analysis. Its job ends when
`validate.py` passes on the output directory.

## Layout

    README.md          this file — the brief for the agent running the kit
    CONTRACT.md        the record format (the interface to the analysis side)
    record_schema.json machine-checkable version of CONTRACT.md
    collect_github.py  house-rules files via GitHub code search  (target corpus, coding)
    collect_reddit.py  posts + top comments from named subreddits (target corpus, design)
    collect_web.py     pages from an allow-listed set of URLs/sitemaps (target corpus, design)
    dedup.py           near-duplicate removal (MinHash) -> *.dedup.jsonl
    validate.py        contract + sanity checks; prints a handoff report
    requirements.txt

## Run order

    pip install -r requirements.txt
    export GITHUB_TOKEN=...                       # read-only PAT is enough
    python collect_github.py --out data/github.jsonl
    export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... REDDIT_USER_AGENT="lexical-corpus-kit/0.1 by <you>"
    python collect_reddit.py --out data/reddit.jsonl
    python collect_web.py --sources web_sources.yaml --out data/web.jsonl
    python dedup.py data/*.jsonl                  # writes data/*.dedup.jsonl + dedup_report.json
    python validate.py data/*.dedup.jsonl         # must print PASS before handoff

Every collector is resumable: re-running with the same --out appends only records whose
`doc_id` is not already present.

## Rules for the collecting agent

1. Never fabricate or "fill in" a record. If a fetch fails, log it in `errors.jsonl` and move on.
2. Respect rate limits and robots.txt exactly as coded; do not lower the sleep intervals.
3. Do not add sources not listed in `web_sources.yaml` without the owner's explicit OK,
   and never scrape sites whose terms prohibit it (Upwork, Fiverr, LinkedIn are excluded on purpose).
4. Do not edit CONTRACT.md or record_schema.json. If a source cannot fit the contract, stop and ask.
5. Stop conditions: GitHub — when every size band returns < 1000 results and has been fully paged,
   or 5,000 files, whichever first. Reddit — the date window in the config. Web — the source list.
6. Handoff = the `data/*.dedup.jsonl` files + `dedup_report.json` + the `validate.py` output, verbatim.
