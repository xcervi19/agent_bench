#!/usr/bin/env python3
"""Deterministic multi-agent catalog merge (no LLM, no review gate).

Reads every agents/*/catalog.json, groups entries by normalized domain
(fallback: normalized entity name), votes across agents, and writes:
  - catalog_merged.json   (everything, annotated)
  - review_later.json      (only rows needing later human check)
  - merge_report.json      (summary stats)

Later human review only touches review_later.json.
"""
import json
import glob
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS_GLOB = os.path.join(HERE, "..", "agents", "*", "catalog.json")

STATUS_RANK = {"empty": 0, "unverified": 1, "proposed": 2}


def norm_domain(d):
    if not d:
        return None
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = re.sub(r"^www\.", "", d)
    return d.rstrip("/") or None


def norm_entity(e):
    if not e:
        return None
    return re.sub(r"\s+", " ", e.strip().lower())


def strongest(statuses):
    return max(statuses, key=lambda s: STATUS_RANK.get(s, 0))


def main():
    paths = sorted(glob.glob(AGENTS_GLOB))
    groups = defaultdict(lambda: {
        "keys": set(), "agents": set(), "entities": {}, "domains": set(),
        "statuses": [], "signals": set(), "categories": set(), "types": set(),
        "countries": set(), "notes": [], "sample": None,
    })

    total_entries = 0
    for p in paths:
        agent = os.path.basename(os.path.dirname(p))
        with open(p) as f:
            data = json.load(f)
        for e in data.get("entries", []):
            dom = norm_domain(e.get("domain"))
            ent = norm_entity(e.get("entity"))
            if not dom and not ent:
                continue  # pure-empty slot, nothing to merge
            total_entries += 1
            key = ("d:" + dom) if dom else ("e:" + ent)
            g = groups[key]
            g["agents"].add(agent)
            if dom:
                g["domains"].add(dom)
            if ent:
                g["entities"][ent] = e.get("entity")
            st = e.get("status") or "empty"
            g["statuses"].append(st)
            for s in (e.get("signals") or []):
                g["signals"].add(s)
            if e.get("category"):
                g["categories"].add(e["category"])
            if e.get("type"):
                g["types"].add(e["type"])
            if e.get("country"):
                g["countries"].add(e["country"])
            if e.get("notes"):
                g["notes"].append(f"[{agent}] {e['notes']}")
            if g["sample"] is None:
                g["sample"] = e

    merged = []
    review = []
    for key, g in groups.items():
        agreement = len(g["agents"])
        status_final = strongest(g["statuses"])
        proposed_votes = sum(1 for s in g["statuses"] if s == "proposed")
        entity_conflict = len(g["entities"]) > 1  # one domain, many names
        accepted = proposed_votes >= 2

        rec = {
            "key": key,
            "domain": sorted(g["domains"])[0] if g["domains"] else None,
            "domains_all": sorted(g["domains"]),
            "entity": (list(g["entities"].values())[0] if g["entities"] else None),
            "entities_all": sorted(g["entities"].values()),
            "category": sorted(g["categories"])[0] if g["categories"] else None,
            "type": sorted(g["types"])[0] if g["types"] else None,
            "countries": sorted(g["countries"]),
            "signals": sorted(g["signals"]),
            "status_final": "accepted" if accepted else status_final,
            "agreement_count": agreement,
            "proposed_votes": proposed_votes,
            "agent_sources": sorted(g["agents"]),
            "conflict": entity_conflict,
            "notes": g["notes"],
        }
        merged.append(rec)
        if rec["conflict"] or agreement == 1 or not accepted:
            review.append(rec)

    merged.sort(key=lambda r: (-r["agreement_count"], -r["proposed_votes"], r["key"]))
    review.sort(key=lambda r: (r["conflict"] is False, -r["agreement_count"], r["key"]))

    report = {
        "input_catalogs": [os.path.relpath(p, HERE) for p in paths],
        "agents": [os.path.basename(os.path.dirname(p)) for p in paths],
        "raw_entries_considered": total_entries,
        "unique_keys": len(merged),
        "accepted": sum(1 for r in merged if r["status_final"] == "accepted"),
        "needs_review": len(review),
        "conflicts": sum(1 for r in merged if r["conflict"]),
    }

    with open(os.path.join(HERE, "catalog_merged.json"), "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    with open(os.path.join(HERE, "review_later.json"), "w") as f:
        json.dump(review, f, indent=2, ensure_ascii=False)
    with open(os.path.join(HERE, "merge_report.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
