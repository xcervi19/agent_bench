"""Stage runners for the topic pipeline.

Each runner is a single ``async`` function that:

* loads inputs (from earlier stages' artifacts),
* writes its own artifact set under ``state/news/<topic_id_hash>/runs/<run_id>/``,
* returns a ``StageResult`` (status + artifact paths + key fields for events).

The orchestrator (:mod:`apps.claude_agent.topics.orchestrator`) is responsible
for state transitions and event emission; runners stay focused on doing work
and persisting artifacts.
"""

from .types import StageResult

__all__ = ["StageResult"]
