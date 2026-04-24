"""Personalized trader crew: turns relevant events into a tailored insight."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm


class PersonalizedTraderCrew(BaseCrewWrapper):
    name = "personalized_trader_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        strategist = _build_strategist_agent()
        writer = _build_writer_agent()

        reasoning = _build_reasoning_task(strategist, ctx.inputs)
        briefing = _build_briefing_task(writer, reasoning)

        return Crew(
            agents=[strategist, writer],
            tasks=[reasoning, briefing],
            process=Process.sequential,
            verbose=False,
        )


def _build_strategist_agent() -> Agent:
    return Agent(
        role="Commodity Strategist",
        goal="Turn events into a concise directional view aligned to the trader profile.",
        backstory="You weigh signals, expose trade-offs, and commit to a clear stance.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_writer_agent() -> Agent:
    return Agent(
        role="Trader Briefing Writer",
        goal="Write a focused briefing a trader can read in 90 seconds.",
        backstory="You compress complex reasoning into clean, scannable prose.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_reasoning_task(agent: Agent, inputs: dict) -> Task:
    query = inputs.get("query", "")
    profile = inputs.get("profile", {})
    evidence = inputs.get("evidence", [])
    return Task(
        description=(
            f"User question: {query}\n"
            f"Trader profile: {profile}\n"
            f"Evidence events: {evidence}\n\n"
            "Produce a short directional view (bullish/bearish/neutral), a confidence 0-1, "
            "and the 2-3 strongest reasons."
        ),
        expected_output="JSON: {direction, confidence, reasons[]}",
        agent=agent,
    )


def _build_briefing_task(agent: Agent, context_task: Task) -> Task:
    return Task(
        description="Write a 3-4 sentence briefing grounded strictly in the strategist's output.",
        expected_output="Plain text briefing.",
        agent=agent,
        context=[context_task],
    )
