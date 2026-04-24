"""Discovery crew: finds fresh external market information."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm


class DiscoveryCrew(BaseCrewWrapper):
    name = "discovery_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        scout = _build_scout_agent()
        task = _build_discovery_task(scout, ctx.inputs)
        return Crew(agents=[scout], tasks=[task], process=Process.sequential, verbose=False)


def _build_scout_agent() -> Agent:
    return Agent(
        role="Market Scout",
        goal="Identify recent, credible developments affecting commodity markets.",
        backstory="You monitor wires, filings, and industry publications for anything tradable.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_discovery_task(agent: Agent, inputs: dict) -> Task:
    commodity = inputs.get("commodity", "power")
    region = inputs.get("region", "Europe")
    return Task(
        description=(
            f"List 5 recent, credible developments affecting {commodity} markets in {region}. "
            "For each: headline, one-sentence summary, why it matters."
        ),
        expected_output="Bulleted list with headline, summary, and rationale.",
        agent=agent,
    )
