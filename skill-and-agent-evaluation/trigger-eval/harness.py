"""Trigger-rate harness for skill descriptions.

Proxy measurement: presents a skill catalog (target + distractors) and a user
query to a judge model, asks which skills it would consult, and records
whether the target was selected. This approximates the product's skill-
selection step; it is not that code path, so absolute rates are a proxy and
only between-arm differences on the same catalog/queries are interpretable.
"""
import json, re, random

TARGET = "repo-rules-preflight"

DISTRACTORS = [
    "customize", "skill-creator", "self-awareness", "verify", "retro-triage",
    "loop-run-card", "agent-debrief", "propagate-source-of-truth",
    "corpus-librarian", "docs", "red-team-prompt", "finish-line",
    "session-harvest", "compute-env-setup", "remote-compute-ssh",
    "figure-style", "literature-review",
]

SELECTOR_TEMPLATE = """You are an AI assistant with access to a catalog of optional skills.
Each skill is a set of instructions you may load before working on a task.
You load a skill only when its description indicates it would help with the
user's request; loading an irrelevant skill wastes context.

AVAILABLE SKILLS
{catalog}

USER REQUEST
{query}

Which skills, if any, would you consult before starting this request?
Reply with a JSON array of skill names, e.g. ["skill-a"], or [] for none.
Reply with the JSON array only."""


def build_catalog(descriptions, target_description, seed=0):
    """descriptions: {name: description} from the live catalog."""
    names = [n for n in DISTRACTORS if n in descriptions]
    rows = [(TARGET, target_description)] + [(n, descriptions[n]) for n in names]
    rng = random.Random(seed)
    rng.shuffle(rows)
    return "\n\n".join("- {}: {}".format(n, d) for n, d in rows)


def build_requests(evalset, catalog, repeats=3, model=None):
    reqs, index = [], []
    for item in evalset:
        for r in range(repeats):
            reqs.append({
                "prompt": SELECTOR_TEMPLATE.format(catalog=catalog, query=item["query"]),
                "max_tokens": 200,
                **({"model": model} if model else {}),
            })
            index.append((item["id"], r, item["should_trigger"]))
    return reqs, index


def parse_selection(text):
    if text is None:
        return []
    m = re.search(r"\[.*?\]", text, re.S)
    if not m:
        return []
    try:
        vals = json.loads(m.group(0))
    except Exception:
        return re.findall(r"[a-z0-9][a-z0-9-]{3,}", m.group(0))
    return [str(v).strip() for v in vals if isinstance(v, str)]


def score(index, responses):
    rows = []
    for (qid, rep, should), resp in zip(index, responses):
        text = resp.get("text") if isinstance(resp, dict) else None
        err = resp.get("error") if isinstance(resp, dict) else "non-dict"
        sel = parse_selection(text)
        rows.append({
            "query_id": qid, "repeat": rep, "should_trigger": bool(should),
            "triggered": TARGET in sel, "n_selected": len(sel),
            "selected": sel, "error": err,
        })
    return rows
