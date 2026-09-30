"""Shared helpers for all collectors: record construction, resumable JSONL output, error log."""
import hashlib, json, os, datetime, re

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def norm_ws(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()

def make_record(source, subsource, url, text, license_or_terms, meta):
    text = norm_ws(text)
    return {
        "doc_id": hashlib.sha256(f"{source}:{url}".encode()).hexdigest()[:24],
        "source": source, "subsource": subsource, "url": url,
        "retrieved_at": utcnow(), "text": text,
        "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "n_chars": len(text), "license_or_terms": license_or_terms, "meta": meta,
    }

class JsonlSink:
    """Append-only, resumable. Tracks doc_ids already on disk so re-runs skip them."""
    def __init__(self, path, err_path=None):
        self.path = path
        self.err_path = err_path or os.path.join(os.path.dirname(path) or ".", "errors.jsonl")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.seen = set()
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    try: self.seen.add(json.loads(line)["doc_id"])
                    except Exception: pass
        self.n_written = 0; self.n_skipped = 0; self.n_short = 0
    def write(self, rec):
        if rec["n_chars"] < 40:
            self.n_short += 1; self.error("too_short", rec["url"]); return False
        if rec["doc_id"] in self.seen:
            self.n_skipped += 1; return False
        with open(self.path, "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.seen.add(rec["doc_id"]); self.n_written += 1; return True
    def error(self, kind, url, detail=""):
        with open(self.err_path, "a") as f:
            f.write(json.dumps({"kind": kind, "url": url, "detail": str(detail)[:300], "at": utcnow()}) + "\n")
    def summary(self):
        return {"written": self.n_written, "skipped_existing": self.n_skipped, "too_short": self.n_short, "total_on_disk": len(self.seen)}
