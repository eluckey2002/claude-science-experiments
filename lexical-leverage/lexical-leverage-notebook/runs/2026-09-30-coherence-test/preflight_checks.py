"""Preflight checks for the coherence test. One page per arm is generated first; these gates decide
whether the batch may proceed.  Usage:
  python preflight_checks.py ABSENT_PAGE.html MODERN_PAGE.html [--stop-absent end_turn --stop-modern end_turn --in-tok 85]
Exit 0 only if every gate passes.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from fingerprint_v2 import fingerprint_html

MUST = ["Coffee, made to order.", "Open every day on Albion Street.", "See the menu",
        "Mon\u2013Fri 7:00am\u20134:00pm", "Sat\u2013Sun 8:00am\u20133:00pm", "12 Albion Street", "\u00a9 Northside Roast"]
ITEMS = ["Espresso", "Flat white", "Filter coffee", "Cold brew", "Hot chocolate", "Almond croissant"]
LINKS = ["Menu", "Hours", "Find us"]

def visible(html):
    h = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))

def gates(html, stop="end_turn", absent_arm=False):
    v = visible(html); out = {}
    out["G1 fixed copy present verbatim"] = all(s in v for s in MUST)
    pos = [v.find(i) for i in ITEMS]
    out["G1 six menu items in order"] = all(p >= 0 for p in pos) and pos == sorted(pos)
    out["G1 three header links"] = all(l in v for l in LINKS)
    out["G2 at least six prices like $3.50"] = len(re.findall(r"\$\d+\.\d{2}\b", v)) >= 6
    out["G2 no exclamation marks in visible text"] = "!" not in v
    out["G3 not truncated (stop=end_turn, </html> present)"] = stop == "end_turn" and html.strip().lower().endswith("</html>")
    if absent_arm:
        out["M1 absent page body font is not system sans"] = fingerprint_html(html)["body_font_class"] != "system-sans"
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    pa, pm = Path(args[0]).read_text(), Path(args[1]).read_text()
    opt = lambda k, d: args[args.index(k) + 1] if k in args else d
    res = {"absent": gates(pa, opt("--stop-absent", "end_turn"), True), "modern": gates(pm, opt("--stop-modern", "end_turn"))}
    ok = True
    for arm, g in res.items():
        for name, passed in g.items():
            print(f"{arm:7s} {'PASS' if passed else 'FAIL'}  {name}"); ok &= passed
    print("in_tok (v2 logged 85 per page):", opt("--in-tok", "not given"))
    print("ALL GATES PASS" if ok else "STOP: a gate failed"); sys.exit(0 if ok else 1)
