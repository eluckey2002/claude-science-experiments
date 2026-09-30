"""Collect agent house-rules files from GitHub via the REST code-search API.

Constraints this script is built around (do not remove):
  * Code search returns at most 1,000 results per query -> we partition by file-size bands.
  * REST code search requires a search TERM, not just qualifiers -> we use a few very common
    English words as terms; the union covers nearly every non-trivial file.
  * Authenticated code search: ~10 requests/min. We sleep on X-RateLimit headers.
  * The REST index only covers repos with recent activity and files < 384 KB. Coverage is
    partial by construction; say so in any write-up.

Usage: GITHUB_TOKEN=... python collect_github.py --out data/github.jsonl [--max-files 5000]
"""
import argparse, base64, os, sys, time, requests
from common import make_record, JsonlSink

API = "https://api.github.com"
KINDS = {
    "CLAUDE.md": "filename:CLAUDE.md",
    "AGENTS.md": "filename:AGENTS.md",
    ".cursorrules": "filename:.cursorrules",
    "copilot-instructions.md": "filename:copilot-instructions.md path:.github",
}
TERMS = ["the", "use", "you", "code", "file", "always", "never"]
SIZE_BANDS = ["200..800", "801..1600", "1601..3000", "3001..6000", "6001..12000", "12001..30000", ">30000"]

def session():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    if not tok: sys.exit("GITHUB_TOKEN (or GITHUB_PAT) not set")
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                      "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "lexical-corpus-kit/0.1"})
    return s

def get(s, url, **kw):
    for attempt in range(6):
        r = s.get(url, timeout=60, **kw)
        if r.status_code in (403, 429) and r.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(5, reset - int(time.time()) + 2)
            print(f"  rate limit; sleeping {wait}s", flush=True); time.sleep(wait); continue
        if r.status_code in (403, 429):   # secondary rate limit
            wait = int(r.headers.get("Retry-After", 60)); print(f"  secondary limit; sleeping {wait}s", flush=True)
            time.sleep(wait); continue
        if r.status_code >= 500: time.sleep(5 * (attempt + 1)); continue
        return r
    return r

def search(s, q, page):
    r = get(s, f"{API}/search/code", params={"q": q, "per_page": 100, "page": page})
    time.sleep(6.5)  # stay under 10/min for code search
    if r.status_code == 422: return None, r.text[:200]
    if r.status_code != 200: return None, f"{r.status_code} {r.text[:200]}"
    return r.json(), None

def fetch_blob(s, repo, path, sha):
    r = get(s, f"{API}/repos/{repo}/contents/{path}", params={"ref": sha})
    if r.status_code != 200: return None, f"{r.status_code}"
    j = r.json()
    if j.get("encoding") != "base64": return None, "not base64"
    return base64.b64decode(j["content"]).decode("utf-8", errors="replace"), None

_repo_cache = {}
def repo_info(s, repo):
    if repo in _repo_cache: return _repo_cache[repo]
    r = get(s, f"{API}/repos/{repo}")
    info = {"stars": None, "license": "NOASSERTION"}
    if r.status_code == 200:
        j = r.json(); info = {"stars": j.get("stargazers_count"), "license": (j.get("license") or {}).get("spdx_id") or "NOASSERTION"}
    _repo_cache[repo] = info; return info

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--max-files", type=int, default=5000)
    ap.add_argument("--kinds", default=",".join(KINDS)); ap.add_argument("--terms", default=",".join(TERMS))
    a = ap.parse_args()
    s = session(); sink = JsonlSink(a.out)
    seen_blobs = set()
    for kind in a.kinds.split(","):
        base = KINDS[kind]
        for band in SIZE_BANDS:
            for term in a.terms.split(","):
                q = f"{term} {base} size:{band}"
                page, total = 1, None
                while True:
                    j, err = search(s, q, page)
                    if err: sink.error("search", q, err); break
                    total = total or j.get("total_count", 0)
                    if page == 1: print(f"[{kind}] size:{band} term={term!r} total={total}", flush=True)
                    items = j.get("items", [])
                    if not items: break
                    for it in items:
                        repo = it["repository"]["full_name"]; path = it["path"]; sha = it["sha"]
                        if sha in seen_blobs: continue
                        seen_blobs.add(sha)
                        html_url = it["html_url"]
                        text, ferr = fetch_blob(s, repo, path, sha)
                        time.sleep(0.8)
                        if ferr: sink.error("blob", html_url, ferr); continue
                        info = repo_info(s, repo)
                        rec = make_record("github", kind, html_url, text, info["license"],
                                          {"repo": repo, "stars": info["stars"], "path": path, "sha": sha, "size": it.get("size")})
                        sink.write(rec)
                        if sink.n_written >= a.max_files: print(sink.summary()); return
                    if page * 100 >= min(total, 1000): break
                    page += 1
    print(sink.summary())

if __name__ == "__main__": main()
