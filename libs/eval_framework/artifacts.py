"""Loader for a frozen Newsfind run's business output.

The evaluator judges artifacts, never live API state, so a run is reproducible
against a directory. A run directory typically looks like::

    <run_dir>/
      evaluation.json
      business_output/
        parsed.json      (plan: topic framing, queries, entities)
        intro.md
        news.json        (sources with scores, source_class, published_at)
        report.json      (key_findings, scenarios, thesis)
        report.md        (cited markdown)

Both ``<run_dir>`` and ``<run_dir>/business_output`` are accepted as the path.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    raw = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


class RunArtifacts(BaseModel):
    """Normalized view over one run's business output + metric hints."""

    label: str = "run"
    run_dir: str | None = None
    topic: str = ""
    parsed: dict[str, Any] = Field(default_factory=dict)
    news: dict[str, Any] = Field(default_factory=dict)
    report: dict[str, Any] = Field(default_factory=dict)
    report_md: str = ""
    intro_md: str = ""
    evaluation: dict[str, Any] = Field(default_factory=dict)
    run_timestamp: str | None = None

    # ---- convenience accessors over the raw artifacts ----

    @property
    def sources(self) -> list[dict[str, Any]]:
        return list(self.news.get("sources", []) or [])

    @property
    def queries(self) -> list[dict[str, Any]]:
        return list(self.parsed.get("queries", []) or [])

    @property
    def key_findings(self) -> list[dict[str, Any]]:
        return list(self.report.get("key_findings", []) or [])

    @property
    def scenarios(self) -> list[dict[str, Any]]:
        return list(self.report.get("scenarios", []) or [])

    @property
    def rag_refs(self) -> list[dict[str, Any]]:
        return list(self.parsed.get("rag_context_refs", []) or [])

    @property
    def entities(self) -> list[dict[str, Any]]:
        """Flatten parsed.entities (a dict of lists) into a single list."""
        ent = self.parsed.get("entities", {}) or {}
        out: list[dict[str, Any]] = []
        if isinstance(ent, dict):
            for group, items in ent.items():
                for item in items or []:
                    if isinstance(item, dict):
                        out.append({"group": group, **item})
                    else:
                        out.append({"group": group, "name": str(item)})
        elif isinstance(ent, list):
            for item in ent:
                out.append(item if isinstance(item, dict) else {"name": str(item)})
        return out

    @property
    def report_text(self) -> str:
        """All natural-language report content, for keyword/causal heuristics."""
        chunks = [
            self.report_md,
            self.report.get("summary_md", "") or "",
            self.report.get("thesis_update_md", "") or "",
            self.parsed.get("working_thesis", "") or "",
            self.parsed.get("topic_restated", "") or "",
        ]
        for f in self.key_findings:
            chunks.append(str(f.get("finding", "")))
        return "\n".join(c for c in chunks if c)

    @property
    def run_dt(self) -> datetime | None:
        return parse_dt(self.run_timestamp)


def _resolve_business_dir(run_dir: Path) -> Path:
    bo = run_dir / "business_output"
    return bo if bo.is_dir() else run_dir


def load_run(run_dir: str | Path, label: str | None = None) -> RunArtifacts:
    """Load a run directory into :class:`RunArtifacts`."""
    root = Path(run_dir)
    business = _resolve_business_dir(root)
    evaluation = _read_json(root / "evaluation.json")
    if not evaluation:
        evaluation = _read_json(business / "evaluation.json")

    parsed = _read_json(business / "parsed.json")
    return RunArtifacts(
        label=label or root.name or "run",
        run_dir=str(root),
        topic=(
            evaluation.get("topic")
            or parsed.get("topic_restated")
            or parsed.get("topic_id")
            or ""
        ),
        parsed=parsed,
        news=_read_json(business / "news.json"),
        report=_read_json(business / "report.json"),
        report_md=_read_text(business / "report.md"),
        intro_md=_read_text(business / "intro.md"),
        evaluation=evaluation,
        run_timestamp=evaluation.get("timestamp"),
    )
