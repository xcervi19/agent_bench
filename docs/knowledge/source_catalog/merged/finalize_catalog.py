#!/usr/bin/env python3
"""Analyst finalization pass over the multi-agent merge.

Re-reads raw agents/*/catalog.json to compute agent-level canonical names
(robust to per-agent row duplication), resolves entity-name conflicts, cleans
machine-noise notes, and emits the FINAL curated artifacts:

  - catalog_final.json          one clean record per domain (full catalog)
  - ../../../../source_whitelist.json   #29 deliverable (accepted, domain-keyed)
  - finalize_report.json        summary stats

No LLM calls; deterministic. Run after merge_catalogs.py.
"""
import json
import glob
import os
import re
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS_GLOB = os.path.join(HERE, "..", "agents", "*", "catalog.json")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
WHITELIST_OUT = os.path.join(REPO_ROOT, "source_whitelist.json")

STATUS_RANK = {"empty": 0, "unverified": 1, "proposed": 2}
NOISE_RE = re.compile(
    r"(crosscheck|review batch|Geo target slot|proposed retained|_\d{3}_)", re.I
)


def norm_domain(d):
    if not d:
        return None
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = re.sub(r"^www\.", "", d)
    return d.rstrip("/") or None


def strongest(statuses):
    return max(statuses, key=lambda s: STATUS_RANK.get(s, 0)) if statuses else "empty"


def clean_notes(notes):
    out = []
    seen = set()
    for n in notes:
        body = re.sub(r"^\[[^\]]+\]\s*", "", n).strip()
        if not body or NOISE_RE.search(body):
            continue
        key = body.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(body)
    return out[:3]


def main():
    paths = sorted(glob.glob(AGENTS_GLOB))
    # domain -> aggregate
    dom = defaultdict(lambda: {
        "agent_names": defaultdict(set),   # raw entity -> set(agents)
        "agents": set(),
        "statuses": [],
        "proposed_agents": set(),
        "signals": set(),
        "categories": Counter(),
        "types": Counter(),
        "countries": set(),
        "notes": [],
    })

    for p in paths:
        agent = os.path.basename(os.path.dirname(p))
        with open(p) as f:
            data = json.load(f)
        for e in data.get("entries", []):
            d = norm_domain(e.get("domain"))
            if not d:
                continue  # whitelist requires a domain
            g = dom[d]
            g["agents"].add(agent)
            ent = (e.get("entity") or "").strip()
            if ent:
                g["agent_names"][ent].add(agent)
            st = e.get("status") or "empty"
            g["statuses"].append(st)
            if st == "proposed":
                g["proposed_agents"].add(agent)
            for s in (e.get("signals") or []):
                g["signals"].add(s)
            if e.get("category"):
                g["categories"][e["category"]] += 1
            if e.get("type"):
                g["types"][e["type"]] += 1
            if e.get("country"):
                g["countries"].add(e["country"])
            if e.get("notes"):
                g["notes"].append(e["notes"])

    final = []
    for d, g in dom.items():
        # canonical entity = most agents agree; tie -> shortest clean name
        canon = None
        if g["agent_names"]:
            canon = sorted(
                g["agent_names"].items(),
                key=lambda kv: (-len(kv[1]), len(kv[0]), kv[0]),
            )[0][0]
        proposed_votes = len(g["proposed_agents"])
        accepted = proposed_votes >= 2
        variants = sorted(g["agent_names"].keys())
        rec = {
            "entity": canon,
            "domain": d,
            "type": g["types"].most_common(1)[0][0] if g["types"] else None,
            "category": g["categories"].most_common(1)[0][0] if g["categories"] else None,
            "countries": sorted(g["countries"]),
            "signals": sorted(g["signals"]),
            "status": "accepted" if accepted else strongest(g["statuses"]),
            "agreement_count": len(g["agents"]),
            "proposed_votes": proposed_votes,
            "agent_sources": sorted(g["agents"]),
            "name_variants": variants if len(variants) > 1 else [],
            "notes": clean_notes(g["notes"]),
        }
        final.append(rec)

    final.sort(key=lambda r: (-r["agreement_count"], -r["proposed_votes"], r["domain"]))

    # #29 whitelist = accepted, real domain, official/data_feed/social
    whitelist = []
    for r in final:
        if r["status"] != "accepted":
            continue
        if r["type"] not in ("official", "data_feed", "social"):
            continue
        whitelist.append({
            "entity": r["entity"],
            "domain": r["domain"],
            "type": r["type"],
            "category": r["category"],
            "notes": (r["notes"][0] if r["notes"] else ""),
            "agreement_count": r["agreement_count"],
        })

    report = {
        "agents": [os.path.basename(os.path.dirname(p)) for p in paths],
        "unique_domains": len(final),
        "accepted": sum(1 for r in final if r["status"] == "accepted"),
        "whitelist_size": len(whitelist),
        "resolved_name_conflicts": sum(1 for r in final if r["name_variants"]),
    }

    with open(os.path.join(HERE, "catalog_final.json"), "w") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    with open(WHITELIST_OUT, "w") as f:
        json.dump(whitelist, f, indent=2, ensure_ascii=False)
    with open(os.path.join(HERE, "finalize_report.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
