"""Extracts structured events from a raw document."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm


class DocumentIntelligenceCrew(BaseCrewWrapper):
    name = "document_intelligence_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        analyst = _build_analyst_agent()
        task = _build_extraction_task(analyst, ctx.inputs)
        return Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=False)


def _build_analyst_agent() -> Agent:
    return Agent(
        role="Document Intelligence Analyst",
        goal="Convert unstructured text into structured market events.",
        backstory="You extract tradable facts from prose without inventing anything.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_extraction_task(agent: Agent, inputs: dict) -> Task:
    text = inputs.get("text", "")
    return Task(
        description=(
            "Extract structured events from the following text. "
            "For each event emit JSON with: category, commodity, region, summary, "
            "occurred_at (ISO8601 or null), impact_score (0-1).\n\n"
            f"TEXT:\n{text}"
        ),
        expected_output="A JSON array of event objects.",
        agent=agent,
    )
