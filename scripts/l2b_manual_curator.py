#!/usr/bin/env python3
"""
Conservative L2b curator — cleans `corpus/L2_text` into `corpus/L2b_clean` and
writes provenance into `corpus/L2b_provenance` and updates `corpus/L2b_run_state.json`.

This performs non-destructive, rule-based cleaning only (no model calls).
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
CORPUS = ROOT / "corpus"
L2_TEXT = CORPUS / "L2_text"
L2B_CLEAN = CORPUS / "L2b_clean"
L2B_PROV = CORPUS / "L2b_provenance"
RUN_STATE = CORPUS / "L2b_run_state.json"


def load_or_create_run_state():
    if RUN_STATE.exists():
        return json.loads(RUN_STATE.read_text())
    data = {"current_batch": {"start": None, "end": None, "status": "in_progress"}, "completed": [], "last_completed": None, "last_updated": None}
    RUN_STATE.parent.mkdir(parents=True, exist_ok=True)
    RUN_STATE.write_text(json.dumps(data, indent=2))
    return data


def write_run_state(state):
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    RUN_STATE.write_text(json.dumps(state, indent=2))


def list_files():
    return sorted([p for p in L2_TEXT.rglob("*.txt")])


def split_header_body(text):
    sep = "\n---\n\n"
    if sep in text:
        hdr, body = text.split(sep, 1)
        return hdr.rstrip(), body.lstrip()
    return "", text


def clean_text(text):
    # Remove common repeated headers/footers (lines in all caps repeated)
    lines = text.splitlines()
    out = []
    prev = None
    for ln in lines:
        s = ln.rstrip()
        if s == prev and s.strip() != "":
            continue
        prev = s
        # drop lines that are just page numbers
        if re.fullmatch(r"\s*\d{1,4}\s*", s):
            continue
        # drop lines that are repeated boilerplate markers
        if s.strip().upper() in ("PORT INFORMATION GUIDE", "PORT", "INFORMATION", "GUIDE", "SOURCE:", "THIS DOCUMENT CAN BE FOUND AT"):
            continue
        # remove HTML tags
        s = re.sub(r"<[^>]+>", "", s)
        # remove cookie/privacy boilerplate
        low = s.lower()
        if any(tok in low for tok in ("cookie", "privacy", "terms of use", "subscribe", "follow us", "share")):
            continue
        out.append(s)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def make_prov(src_rel, l2_len, l2b_len):
    return {
        "source_path": src_rel,
        "reproducible": False,
        "l2_length": l2_len,
        "l2b_length": l2b_len,
        "l2b_action": "N/A",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    state = load_or_create_run_state()
    files = list_files()
    if not files:
        print("No files found under corpus/L2_text")
        return
    for p in files:
        rel = str(p.relative_to(CORPUS))
        if rel in state.get("completed", []):
            print("Skipping already completed:", rel)
            continue
        text = p.read_text(encoding="utf-8")
        header, body = split_header_body(text)
        cleaned = clean_text(body)
        out_path = L2B_CLEAN / p.relative_to(L2_TEXT)
        prov_path = L2B_PROV / p.relative_to(L2_TEXT).with_suffix(p.suffix + ".provenance.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        prov_path.parent.mkdir(parents=True, exist_ok=True)
        if header:
            out_text = header.rstrip() + "\n---\n\n" + cleaned + "\n"
        else:
            out_text = cleaned + "\n"
        out_path.write_text(out_text, encoding="utf-8")
        prov = make_prov(rel, len(body), len(cleaned))
        prov_path.write_text(json.dumps(prov, indent=2), encoding="utf-8")
        state.setdefault("completed", []).append(rel)
        state["last_completed"] = rel
        write_run_state(state)
        print("Processed:", rel)


if __name__ == "__main__":
    main()
