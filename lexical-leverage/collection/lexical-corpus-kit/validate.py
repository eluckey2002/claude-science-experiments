"""Handoff gate. Checks every record against record_schema.json and prints a report the analysis side reads first.

PASS requires: schema-valid records, no duplicate doc_ids, no exact-duplicate texts, and no single
subsource > 70% of a file (a concentration check against one viral source swamping the corpus).
Usage: python validate.py data/*.dedup.jsonl
"""
import json, sys, os, statistics
from collections import Counter

def main(paths):
    try: import jsonschema
    except ImportError: sys.exit("pip install jsonschema")
    schema = json.load(open(os.path.join(os.path.dirname(__file__), "record_schema.json")))
    v = jsonschema.Draft202012Validator(schema)
    ok_all = True; report = {}
    for p in paths:
        recs = [json.loads(l) for l in open(p) if l.strip()]
        errs = [(i, e.message) for i, r in enumerate(recs) for e in v.iter_errors(r)]
        ids = Counter(r["doc_id"] for r in recs); hashes = Counter(r["text_sha256"] for r in recs)
        subs = Counter(r["subsource"] for r in recs)
        top_share = (subs.most_common(1)[0][1] / len(recs)) if recs else 0
        chars = [r["n_chars"] for r in recs]
        words = sum(len(r["text"].split()) for r in recs)
        ok = not errs and max(ids.values(), default=0) <= 1 and max(hashes.values(), default=0) <= 1 and top_share <= 0.7 and len(recs) > 0
        ok_all &= ok
        report[p] = {"status": "PASS" if ok else "FAIL", "records": len(recs), "approx_words": words,
                     "schema_errors": len(errs), "first_errors": errs[:3],
                     "dup_doc_ids": sum(1 for n in ids.values() if n > 1), "dup_texts": sum(1 for n in hashes.values() if n > 1),
                     "subsource_counts": dict(subs), "top_subsource_share": round(top_share, 3),
                     "n_chars_median": statistics.median(chars) if chars else 0,
                     "sources": dict(Counter(r["source"] for r in recs))}
    print(json.dumps(report, indent=2)); print("PASS" if ok_all else "FAIL")
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__": main(sys.argv[1:])
