"""Collect posts (+ top comments) from subreddits where people brief web design or prompt site-builders.

Uses the official API through PRAW (read-only app credentials). ~100 req/min is enforced by PRAW.
Two subreddit groups are tagged in meta.is_brief so the analysis side can separate them:
  briefs   : people describing the site they want  (r/forhire, r/DesignJobs, r/web_design requests)
  prompting: people sharing prompts to site-building agents (r/ClaudeAI, r/cursor, r/ChatGPTCoding, r/lovable, r/v0)

Usage: REDDIT_CLIENT_ID=.. REDDIT_CLIENT_SECRET=.. REDDIT_USER_AGENT=.. python collect_reddit.py --out data/reddit.jsonl
"""
import argparse, os, sys, time
from common import make_record, JsonlSink

BRIEF_SUBS = ["web_design", "webdev", "UI_Design", "forhire", "DesignJobs", "smallbusiness", "Entrepreneur"]
PROMPT_SUBS = ["ClaudeAI", "cursor", "ChatGPTCoding", "lovable", "v0", "PromptEngineering", "webflow", "Wordpress"]
# Only keep posts whose title/body mentions a site/page/UI — this is a design-vocabulary corpus, not general chat.
KEYWORDS = ["website", "web site", "landing page", "homepage", "web design", "site design", "ui ", "ux ", "redesign", "portfolio site", "squarespace", "wordpress", "webflow", "figma"]
LISTINGS = ["new", "top", "hot"]
TOP_COMMENTS = 5

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    ap.add_argument("--per-listing", type=int, default=500); ap.add_argument("--time-filter", default="year")
    a = ap.parse_args()
    try: import praw
    except ImportError: sys.exit("pip install praw")
    for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"):
        if not os.environ.get(k): sys.exit(f"{k} not set")
    r = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                    user_agent=os.environ["REDDIT_USER_AGENT"], ratelimit_seconds=600)
    r.read_only = True
    sink = JsonlSink(a.out)
    for group, subs in (("brief", BRIEF_SUBS), ("prompting", PROMPT_SUBS)):
        for sub in subs:
            n0 = sink.n_written
            for listing in LISTINGS:
                try:
                    gen = getattr(r.subreddit(sub), listing)
                    posts = gen(limit=a.per_listing, time_filter=a.time_filter) if listing == "top" else gen(limit=a.per_listing)
                    for p in posts:
                        blob = f"{p.title}\n\n{p.selftext or ''}".lower()
                        if not any(k in blob for k in KEYWORDS): continue
                        try:
                            p.comments.replace_more(limit=0)
                            comments = [c.body for c in p.comments[:TOP_COMMENTS] if hasattr(c, "body")]
                        except Exception as e:
                            comments = []; sink.error("comments", p.url, e)
                        text = f"{p.title}\n\n{p.selftext or ''}" + ("".join("\n\n---\n\n" + c for c in comments))
                        url = f"https://www.reddit.com{p.permalink}"
                        rec = make_record("reddit", sub, url, text, "reddit-api-terms",
                                          {"post_id": p.id, "created_utc": int(p.created_utc), "score": p.score,
                                           "num_comments": p.num_comments, "is_brief": group == "brief", "listing": listing})
                        sink.write(rec)
                except Exception as e:
                    sink.error("listing", f"r/{sub}/{listing}", e); time.sleep(10)
            print(f"r/{sub}: +{sink.n_written - n0}", flush=True)
    print(sink.summary())

if __name__ == "__main__": main()
