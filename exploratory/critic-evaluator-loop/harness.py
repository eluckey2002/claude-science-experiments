
import json, re
MODEL = host.reasoning_model()
def parse_json(t):
    m = re.search(r'\{.*\}', t, flags=re.S); return json.loads(m.group(0))
def key_block(key):
    return "\n".join(f"- {k['id']}: {k['flaw']}" for k in key)
def eval_doc(doc, key):
    p = ("You are grading a design document against a fixed list of known flaws. For EACH flaw id, decide whether that flawed claim "
         "is still asserted anywhere in the document ('present'), or has been removed or corrected so the document no longer asserts it ('absent'). "
         "Judge only these listed flaws; ignore everything else.\n\nKNOWN FLAWS:\n"+key_block(key)+
         "\n\nDOCUMENT:\n<<<\n"+doc+"\n>>>\n\nReturn only JSON: {\"verdicts\": {\"<id>\": \"present\"|\"absent\", ...}, \"notes\": {\"<id>\": \"<=20 words\"}}")
    return p
def detect_prompt(critique, key):
    return ("Below is a critique of a design document, and a list of known flaws planted in that document. For EACH flaw id, decide whether the critique "
            "identifies it: it must point at the flawed claim and say it is wrong or inconsistent (the right reason, or a compatible one). "
            "Merely mentioning the topic does not count.\n\nKNOWN FLAWS:\n"+key_block(key)+"\n\nCRITIQUE:\n<<<\n"+critique+"\n>>>\n\n"
            "Return only JSON: {\"found\": {\"<id>\": true|false, ...}}")
