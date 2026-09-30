"""Near-duplicate removal. Exact duplicates by text_sha256; near-duplicates by MinHash-LSH over 5-word shingles.

Why: house-rules files are copied from a few viral templates. Without this step the keyness ranking
measures the templates, not the population. Threshold 0.8 Jaccard is deliberately loose; the report
lists cluster sizes so the analysis side can judge.

Usage: python dedup.py data/github.jsonl data/reddit.jsonl ...   -> writes <name>.dedup.jsonl + dedup_report.json
"""
import json, re, sys
from collections import Counter

def shingles(text, k=5):
    toks = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(toks[i:i+k]) for i in range(max(1, len(toks) - k + 1))}

def main(paths):
    try: from datasketch import MinHash, MinHashLSH
    except ImportError: sys.exit("pip install datasketch")
    report = {}
    for path in paths:
        recs = [json.loads(l) for l in open(path) if l.strip()]
        keep, seen_hash = [], set()
        lsh = MinHashLSH(threshold=0.8, num_perm=128); mh = {}
        cluster_of = {}; clusters = Counter()
        for r in recs:
            if r["text_sha256"] in seen_hash: cluster_of[r["doc_id"]] = "exact"; clusters["exact"] += 1; continue
            seen_hash.add(r["text_sha256"])
            m = MinHash(num_perm=128)
            for sh in shingles(r["text"]): m.update(sh.encode())
            near = lsh.query(m)
            if near:
                rep = near[0]; clusters[rep] += 1; cluster_of[r["doc_id"]] = rep; continue
            lsh.insert(r["doc_id"], m); mh[r["doc_id"]] = m; keep.append(r); clusters[r["doc_id"]] += 1
        out = path.replace(".jsonl", ".dedup.jsonl")
        with open(out, "w") as f:
            for r in keep: f.write(json.dumps(r, ensure_ascii=False) + "\n")
        big = sorted(((n, d) for d, n in clusters.items() if d != "exact" and n > 1), reverse=True)[:10]
        report[path] = {"input": len(recs), "kept": len(keep), "exact_dups": clusters.get("exact", 0),
                        "near_dups": len(recs) - len(keep) - clusters.get("exact", 0),
                        "largest_clusters": [{"rep_doc_id": d, "size": n} for n, d in big]}
        print(path, report[path]["input"], "->", report[path]["kept"], flush=True)
    json.dump(report, open("dedup_report.json", "w"), indent=2)

if __name__ == "__main__": main(sys.argv[1:])
