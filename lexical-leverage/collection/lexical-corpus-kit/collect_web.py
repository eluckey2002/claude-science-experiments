"""Fetch pages from allow-listed sources only, with robots.txt checked per host, and extract main text.

Usage: python collect_web.py --sources web_sources.yaml --out data/web.jsonl
Requires: requests, pyyaml, trafilatura. Sleeps >= 3 s between requests to the same host.
JS-rendered galleries (v0, Lovable) may yield little text with plain HTTP; if a source returns
mostly empty pages the script reports it and the owner decides whether to add a headless-browser adapter.
"""
import argparse, sys, time, urllib.robotparser as rp, urllib.parse as up, xml.etree.ElementTree as ET, requests
from common import make_record, JsonlSink

UA = "lexical-corpus-kit/0.1 (+research corpus; contact owner)"
MIN_GAP = 3.0
_last = {}; _robots = {}

def allowed(url):
    host = up.urlsplit(url).netloc
    if host not in _robots:
        r = rp.RobotFileParser(); r.set_url(f"https://{host}/robots.txt")
        try: r.read()
        except Exception: r = None
        _robots[host] = r
    r = _robots[host]
    return True if r is None else r.can_fetch(UA, url)

def polite_get(s, url):
    host = up.urlsplit(url).netloc
    gap = time.time() - _last.get(host, 0)
    if gap < MIN_GAP: time.sleep(MIN_GAP - gap)
    _last[host] = time.time()
    return s.get(url, timeout=30, headers={"User-Agent": UA})

def sitemap_urls(s, url):
    r = polite_get(s, url)
    if r.status_code != 200: return []
    root = ET.fromstring(r.content); ns = {"sm": root.tag.split("}")[0].strip("{")}
    if root.tag.endswith("sitemapindex"):
        out = []
        for loc in root.findall(".//sm:loc", ns): out += sitemap_urls(s, loc.text.strip())
        return out
    return [loc.text.strip() for loc in root.findall(".//sm:loc", ns)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sources", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try: import yaml, trafilatura
    except ImportError: sys.exit("pip install pyyaml trafilatura")
    cfg = yaml.safe_load(open(a.sources))["sources"]
    s = requests.Session(); sink = JsonlSink(a.out)
    for key, src in cfg.items():
        if src.get("kind") == "note" or not (src.get("urls") or src.get("sitemap")):
            print(f"[{key}] skipped ({src.get('note', 'no urls')})"); continue
        urls = sitemap_urls(s, src["sitemap"]) if src.get("kind") == "sitemap" else list(src["urls"])
        inc = src.get("include") or []
        urls = [u for u in urls if not inc or any(i in u for i in inc)][: src.get("max_pages", 200)]
        n0, empty = sink.n_written, 0
        for u in urls:
            if not allowed(u): sink.error("robots_disallow", u); continue
            try:
                r = polite_get(s, u)
                if r.status_code != 200: sink.error("http", u, r.status_code); continue
                text = trafilatura.extract(r.text, include_comments=False, include_tables=False) or ""
                title = trafilatura.extract_metadata(r.text).title if text else None
                if len(text) < 40: empty += 1
                rec = make_record("web", key, u, text, "robots-allowed; " + src.get("terms", "terms not recorded"),
                                  {"title": title, "fetched_status": r.status_code})
                sink.write(rec)
            except Exception as e: sink.error("fetch", u, e)
        print(f"[{key}] +{sink.n_written - n0} records, {empty} near-empty of {len(urls)} fetched", flush=True)
    print(sink.summary())

if __name__ == "__main__": main()
