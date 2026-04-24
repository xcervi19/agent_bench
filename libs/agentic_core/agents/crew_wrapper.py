"""Base class that turns a CrewAI crew into a framework-aware unit."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ..logging import get_logger
from .replay import SessionRecorder

log = get_logger(__name__)


@dataclass
class CrewRunContext:
    tenant_id: UUID
    session_id: UUID = field(default_factory=uuid4)
    inputs: dict[str, Any] = field(default_factory=dict)


@dataclass
class CrewRunResult:
    session_id: UUID
    output: dict[str, Any]


class BaseCrewWrapper(ABC):
    """Subclass per crew. Keep orchestration here; keep agents/tasks pure."""

    name: str = "unnamed_crew"

    @abstractmethod
    def build_crew(self, ctx: CrewRunContext) -> Any:
        """Return a configured `crewai.Crew` instance for this run."""

    async def run(self, ctx: CrewRunContext) -> CrewRunResult:
        recorder = SessionRecorder(ctx.session_id, ctx.tenant_id, self.name)
        await recorder.start(ctx.inputs)
        recorder.record("crew.build", crew=self.name, inputs=ctx.inputs)

        crew = self.build_crew(ctx)
        raw = crew.kickoff(inputs=ctx.inputs)
        output = self._normalize_output(raw)

        recorder.record("crew.output", output=output)
        await recorder.finish(output=output)
        log.info("crew.done", crew=self.name, session_id=str(ctx.session_id))
        return CrewRunResult(session_id=ctx.session_id, output=output)

    @staticmethod
    def _normalize_output(raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        return {"result": str(raw)}
