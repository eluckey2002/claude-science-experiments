"""Decision rule for the coherence test, fixed before any page is generated.

Input: a fingerprints CSV (columns as written by tools/fingerprint_v2.py plus `arm`).
The four word-class indicators are the properties "Make it modern." moved in the thin
brief of runs/2026-09-28-thin-thick-coffee-v2 (chosen from that run, not from this one).

Usage: python decision_rule.py fingerprints.csv ABSENT_ARM MODERN_ARM [thick_col_value]
"""
import sys
import pandas as pd

INDICATORS = {
    "body font is system sans": lambda d: d["body_font_class"] == "system-sans",
    "backdrop blur present": lambda d: d["uses_backdrop_blur"].astype(str) == "True",
    "largest corner radius > 40px": lambda d: d["max_radius_px"] > 40,
    "two or more gradients": lambda d: d["n_gradients"] >= 2,
}
MOVE_MIN = 3      # modern arm must have >= 3 more runs in the word's class than the absent arm (of k=5)
HEADROOM_MAX = 2  # absent arm may already be in the word's class in at most 2 of 5 runs

def evaluate(df, absent, modern):
    a, m = df[df.arm == absent], df[df.arm == modern]
    rows = []
    for name, fn in INDICATORS.items():
        na, nm = int(fn(a).sum()), int(fn(m).sum())
        rows.append(dict(indicator=name, n_absent=na, n_modern=nm, k_absent=len(a), k_modern=len(m),
                         headroom=na <= HEADROOM_MAX, moved=(nm - na) >= MOVE_MIN))
    t = pd.DataFrame(rows)
    with_room = int(t.headroom.sum()); moved = int((t.moved & t.headroom).sum())
    if with_room < 3:
        verdict = "UNRESOLVED (fewer than 3 indicators had headroom in the absent arm)"
    elif moved >= 3:
        verdict = "READING 1 SUPPORTED (word keeps its recipe under a non-visual guide)"
    elif moved == 0:
        verdict = "READING 2 SUPPORTED (any guide silences the word, even one that pins nothing it touches)"
    else:
        verdict = "PARTIAL (word moves some of its recipe, not all; readings not separated)"
    return t, with_room, moved, verdict

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1]); t, w, mv, v = evaluate(df, sys.argv[2], sys.argv[3])
    print(t.to_string(index=False)); print(f"headroom on {w}/4, moved {mv}/4 -> {v}")
