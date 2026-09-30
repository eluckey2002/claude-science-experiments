#!/usr/bin/env python3
"""Re-derive every load-bearing claim in a claims manifest from primary sources.

Usage:  python3 verify_claims.py claims.json --repo /path/to/loop-lab

Exit 0 only when every MEASURED claim recomputes to its recorded value and every
QUOTED claim is found verbatim in a source file whose sha256 matches the record.
ARGUED claims are reported as UNVERIFIABLE by construction and never pass or fail.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_namespace(repo: Path) -> dict:
    import pandas as pd
    succ = repo / "studies/small-league-successor"
    m = pd.read_csv(succ / "CANDIDATE-SEALED-MATRIX.csv")
    banks = {}
    for task in (4, 5):
        if task == 4:
            banks[4] = json.loads((succ / "runs/task4-block-01/sealed-evaluation.json").read_text())
        else:
            d = succ / "task5-release-waves/sealed"
            banks[5] = [json.loads(p.read_text()) for p in sorted(d.glob("task5-case-*.json"))]

    def cols(task):
        return [f"task{task}-case-{i:02d}" for i in range(1, 25)]

    def pool(task):
        return m[m.task == task]

    def rate(task):
        P = pool(task)[cols(task)].astype(bool)
        return P.mean(axis=0)

    def discriminating(task, lo=0.10, hi=0.90):
        r = rate(task)
        return [c for c in r.index if lo <= r[c] <= hi]

    def constant_cases(task):
        r = rate(task)
        return [c for c in r.index if r[c] in (0.0, 1.0)]

    def distinct_behaviours(task):
        P = pool(task)[cols(task)].astype(bool)
        return int(P.apply(tuple, axis=1).nunique())

    def outcomes(task):
        return {c["id"]: c["expected"].get("outcome") for c in banks[task]}

    def constant_policy_ceiling(task):
        keys = [json.dumps(c["expected"], sort_keys=True) for c in banks[task]]
        return max(keys.count(k) for k in set(keys))

    def descriptor_fidelity(task):
        from itertools import combinations
        sub = pool(task)
        sig = sub[cols(task)].astype(bool).apply(tuple, axis=1)
        vec = sub["vector"].astype(str)
        tt = tf = ft = 0
        for a, b in combinations(list(sub.index), 2):
            ce, be = vec[a] == vec[b], sig[a] == sig[b]
            if ce and be:
                tt += 1
            elif ce:
                tf += 1
            elif be:
                ft += 1
        return {"p_behaviour_given_class": round(tt / (tt + tf), 3) if tt + tf else None,
                "p_class_given_behaviour": round(tt / (tt + ft), 3) if tt + ft else None}

    def max_within_descriptor_spread(task):
        sub = pool(task)
        g = sub.groupby("vector")["sealedPassed"]
        return int((g.max() - g.min()).max())

    def sign_consistent_contrasts():
        """Per measure, contrasts keeping one non-zero sign across ALL four blocks."""
        out = []
        for measure in ("finalist", "best_of_6", "union_of_6"):
            per = {}
            for task in (4, 5):
                for block in (1, 2):
                    g = m[(m.task == task) & (m.block == block)]
                    val = {}
                    for arm in ("GG", "GP", "SG", "SP"):
                        a = g[g.arm == arm]
                        P = a[cols(task)].astype(bool)
                        if measure == "finalist":
                            val[arm] = int(a[a.selectedFinal].sealedPassed.iloc[0])
                        elif measure == "best_of_6":
                            val[arm] = int(a.sealedPassed.max())
                        else:
                            val[arm] = int(P.any(axis=0).sum())
                    per[(task, block)] = {
                        "role_SG_GG": val["SG"] - val["GG"], "role_SP_GP": val["SP"] - val["GP"],
                        "state_GP_GG": val["GP"] - val["GG"], "state_SP_SG": val["SP"] - val["SG"],
                        "interaction": (val["SP"] - val["SG"]) - (val["GP"] - val["GG"])}
            for name in next(iter(per.values())):
                s = [per[k][name] for k in per]
                if all(x > 0 for x in s) or all(x < 0 for x in s):
                    out.append((measure, name, s))
        return out

    def union_vs_finalist_max_gap():
        gaps = []
        for task in (4, 5):
            for block in (1, 2):
                for arm in ("GG", "GP", "SG", "SP"):
                    a = m[(m.task == task) & (m.block == block) & (m.arm == arm)]
                    fin = int(a[a.selectedFinal].sealedPassed.iloc[0])
                    uni = int(a[cols(task)].astype(bool).any(axis=0).sum())
                    gaps.append(uni - fin)
        return max(gaps)

    def diagnostic_saturation(task):
        """How many candidates scored a perfect non-sealed diagnostic rate, and
        the sealed range those candidates actually span."""
        sub = pool(task)
        perfect = sub[sub.diagnosticPassed == sub.diagnosticTotal]
        return {"n_candidates": int(len(sub)), "n_perfect_diagnostic": int(len(perfect)),
                "sealed_min": int(perfect.sealedPassed.min()),
                "sealed_max": int(perfect.sealedPassed.max())}

    def diagnostic_predicts_sealed(task):
        """Spearman rank correlation of the non-sealed proxy against sealed outcome."""
        sub = pool(task)
        r = (sub.diagnosticPassed / sub.diagnosticTotal).corr(sub.sealedPassed, method="spearman")
        return round(float(r), 3)

    def discriminating_in_band(task, lo, hi):
        sub = pool(task)
        band = sub[(sub.sealedPassed >= lo) & (sub.sealedPassed <= hi)]
        r = band[cols(task)].astype(bool).mean(axis=0)
        return len([c for c in r.index if 0.10 <= r[c] <= 0.90])

    return {"m": m, "banks": banks, "cols": cols, "pool": pool, "rate": rate,
            "diagnostic_saturation": diagnostic_saturation,
            "diagnostic_predicts_sealed": diagnostic_predicts_sealed,
            "discriminating_in_band": discriminating_in_band,
            "discriminating": discriminating, "constant_cases": constant_cases,
            "distinct_behaviours": distinct_behaviours, "outcomes": outcomes,
            "constant_policy_ceiling": constant_policy_ceiling,
            "descriptor_fidelity": descriptor_fidelity,
            "max_within_descriptor_spread": max_within_descriptor_spread,
            "sign_consistent_contrasts": sign_consistent_contrasts,
            "union_vs_finalist_max_gap": union_vs_finalist_max_gap,
            "len": len, "sorted": sorted, "set": set, "all": all, "any": any, "int": int,
            "__builtins__": {}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--repo", required=True, help="path to a loop-lab checkout")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    claims = json.loads(Path(args.manifest).read_text())["claims"]
    ns = build_namespace(repo)

    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    width = max(len(c["id"]) for c in claims)
    for c in claims:
        cid, kind = c["id"], c["type"]
        if kind == "ARGUED":
            status, detail = "UNVERIFIABLE", "argued claim - requires independent judgement"
        elif kind == "QUOTED":
            src = repo / c["source"]
            if not src.exists():
                status, detail = "FAIL", f"source missing: {c['source']}"
            elif sha256(src) != c["source_sha256"]:
                status, detail = "FAIL", f"source sha256 changed: {c['source']}"
            elif c["quote"] not in src.read_text():
                status, detail = "FAIL", "quote not found verbatim in source"
            else:
                status, detail = "PASS", f"verbatim in {c['source']}"
        elif kind == "MEASURED":
            try:
                # ns is passed as globals, not locals: a generator expression
                # resolves free names against globals only.
                got = eval(c["expression"], ns, {})  # noqa: S307
            except Exception as exc:
                status, detail = "FAIL", f"{type(exc).__name__}: {exc}"
            else:
                if got == c["expected"]:
                    status, detail = "PASS", f"recomputed {got!r}"
                else:
                    status, detail = "FAIL", f"expected {c['expected']!r}, recomputed {got!r}"
        else:
            status, detail = "FAIL", f"unknown claim type {kind!r}"
        counts[status] += 1
        print(f"{status:<13} {cid:<{width}}  {detail}")

    print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, "
          f"{counts['UNVERIFIABLE']} unverifiable (argued)")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
