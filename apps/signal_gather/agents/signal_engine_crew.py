"""Aggregate clustered events into a market signal narrative."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm


class SignalEngineCrew(BaseCrewWrapper):
    name = "signal_engine_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        analyst = _build_analyst_agent()
        task = _build_signal_task(analyst, ctx.inputs)
        return Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=False)


def _build_analyst_agent() -> Agent:
    return Agent(
        role="Signal Analyst",
        goal="Turn clusters of related events into one tradable signal narrative.",
        backstory="You weigh evidence, expose conflicts, and refuse to overstate confidence.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_signal_task(agent: Agent, inputs: dict) -> Task:
    return Task(
        description=(
            "Cluster of events:\n"
            f"{inputs.get('events', [])}\n\n"
            "Rule-engine proposal (may be wrong):\n"
            f"{inputs.get('rule_proposal', {})}\n\n"
            "Emit a JSON object: {direction: bullish|bearish|neutral, confidence: 0..1, "
            "rationale: str, kind: short_label}. Adjust the rule proposal only when the "
            "evidence justifies it; otherwise reuse it."
        ),
        expected_output="JSON object only.",
        agent=agent,
    )
