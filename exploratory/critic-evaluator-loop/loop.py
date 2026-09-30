
import json, time
CRITIC = ("You are reviewing a design document before it is implemented. Find the errors: factual claims that are wrong, "
          "statements that contradict other parts of the document, and design flaws. For each issue give: the exact sentence (quoted), "
          "what is wrong, the evidence, and the fix. List at most 25 issues, most important first.")
def critic_prompt(doc, arm):
    if arm == 'outside':
        return (CRITIC + " The document's cited sources are attached after it; check the document's claims against them.\n\nDOCUMENT:\n<<<\n"
                + doc + "\n>>>\n\nCITED SOURCES:\n<<<\n" + SRC + "\n>>>")
    return CRITIC + " The cited sources are not available to you.\n\nDOCUMENT:\n<<<\n" + doc + "\n>>>"
def reviser_prompt(doc, critique):
    return ("Revise the design document by applying the critique. Accept points you judge correct and decline ones you judge wrong. "
            "Return only JSON: {\"edits\": [{\"old\": \"<exact text copied from the document, long enough to occur exactly once>\", \"new\": \"<replacement>\"}], "
            "\"declined\": [\"<short note>\"]}.\n\nDOCUMENT:\n<<<\n" + doc + "\n>>>\n\nCRITIQUE:\n<<<\n" + critique + "\n>>>")
def apply_edits(doc, edits):
    ok = bad = 0
    for e in edits:
        o, n = e.get('old',''), e.get('new','')
        if o and doc.count(o) == 1: doc = doc.replace(o, n); ok += 1
        else: bad += 1
    return doc, ok, bad
ARMS = ['reread','outside']; REPS = 3; ROUNDS = 3
cells = [(a, r) for a in ARMS for r in range(REPS)]
state = {c: seeded for c in cells}; log = []
for rnd in range(1, ROUNDS+1):
    t0 = time.time()
    crit = ask([critic_prompt(state[c], c[0]) for c in cells], max_tokens=10000)
    rev = ask([reviser_prompt(state[c], cr['text']) for c, cr in zip(cells, crit)], max_tokens=16000)
    new = {}
    for c, cr, rv in zip(cells, crit, rev):
        try: j = parse_json(rv['text']); edits = j.get('edits', []); dec = j.get('declined', [])
        except Exception as ex: edits, dec = [], [f'PARSE_FAIL {ex}']
        d2, ok, bad = apply_edits(state[c], edits); new[c] = (d2, ok, bad, len(dec), cr)
    det = ask([detect_prompt(new[c][4]['text'], KEY) for c in cells])
    ev = ask([eval_doc(new[c][0], KEY) for c in cells])
    for c, dt, e in zip(cells, det, ev):
        d2, ok, bad, ndec, cr = new[c]
        rec = dict(arm=c[0], rep=c[1], round=rnd, found=parse_json(dt['text'])['found'], verdicts=parse_json(e['text'])['verdicts'],
                   edits_applied=ok, edits_failed=bad, declined=ndec, doc_chars=len(d2), critique_chars=len(cr['text']),
                   critic_usage=cr.get('usage'))
        log.append(rec); state[c] = d2
        open(f'runs/{c[0]}_rep{c[1]}_r{rnd}_critique.md','w').write(cr['text']); open(f'runs/{c[0]}_rep{c[1]}_r{rnd}_doc.md','w').write(d2)
    json.dump(log, open('runs/log.json','w'), indent=1)
    print(f'round {rnd} done {time.time()-t0:.0f}s', flush=True)
