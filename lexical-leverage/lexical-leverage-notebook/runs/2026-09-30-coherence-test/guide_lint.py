"""Fail if the guide text names anything the fingerprint extractor reads (or a style word).
Usage: python guide_lint.py arms.json
"""
import json, re, sys
WORDS = ("font typeface serif sans color colour hex palette dark light theme radius radii round corner gradient blur "
         "glass shadow animat transition hover spacing padding margin width grid flex layout sticky modern minimal "
         "clean elegant warm cozy bold style design visual look aesthetic pill").split()
PATTERN = r"\b(" + "|".join(WORDS) + r")\w*"
a = json.load(open(sys.argv[1]))["arms"]
guide = a["guide|absent"].split("\n\n")[0]
hits = sorted({m.group(0).lower() for m in re.finditer(PATTERN, guide, re.I)})
print("guide characters:", len(guide), "| forbidden terms found:", hits or "none")
# the two arms must differ only by the added sentence
x, y = a["guide|absent"], a["guide|modern"]
assert y.replace(" Make it modern.", "") == x, "arms differ by more than the sentence 'Make it modern.'"
sys.exit(1 if hits else 0)
