"""Compose a daily/weekly trader briefing from signals and events."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm


class BriefingCrew(BaseCrewWrapper):
    name = "briefing_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        editor = _build_editor_agent()
        task = _build_briefing_task(editor, ctx.inputs)
        return Crew(agents=[editor], tasks=[task], process=Process.sequential, verbose=False)


def _build_editor_agent() -> Agent:
    return Agent(
        role="Trader Briefing Editor",
        goal="Write a tight, scannable briefing tailored to the trader profile.",
        backstory="Every sentence either changes a decision or gets cut.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_briefing_task(agent: Agent, inputs: dict) -> Task:
    return Task(
        description=(
            f"Trader profile:\n{inputs.get('profile', {})}\n\n"
            f"Signals (last {inputs.get('window_hours', 24)}h):\n{inputs.get('signals', [])}\n\n"
            f"Notable events:\n{inputs.get('events', [])}\n\n"
            "Write a briefing with:\n"
            "1) One-sentence headline.\n"
            "2) 3-5 bullets, each starting with commodity tag, then the actionable point.\n"
            "3) One closing 'watchlist' line.\n"
            "Stay grounded — no claims absent from the inputs."
        ),
        expected_output="Plain text briefing.",
        agent=agent,
    )
