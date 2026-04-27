"""Turn natural language ('I trade EU gas, want morning briefings…') into a profile."""

from crewai import Agent, Crew, Process, Task

from agentic_core.agents import BaseCrewWrapper, CrewRunContext

from .llm import default_llm

OUTPUT_SCHEMA = (
    '{"display_name": str|null, "commodities": [str], "regions": [str], '
    '"themes": [str], "risk_appetite": "low|medium|high", '
    '"alert_channels": [str], "briefing_cadence": "daily|weekly|none", '
    '"impact_threshold": float}'
)


class ProfileSetupCrew(BaseCrewWrapper):
    name = "profile_setup_crew"

    def build_crew(self, ctx: CrewRunContext) -> Crew:
        interpreter = _build_interpreter_agent()
        task = _build_setup_task(interpreter, ctx.inputs.get("text", ""))
        return Crew(agents=[interpreter], tasks=[task], process=Process.sequential, verbose=False)


def _build_interpreter_agent() -> Agent:
    return Agent(
        role="Trader Onboarding Interpreter",
        goal="Convert free-form trader self-description into a structured profile.",
        backstory="You speak the language of commodity desks and never invent preferences.",
        llm=default_llm(),
        allow_delegation=False,
    )


def _build_setup_task(agent: Agent, text: str) -> Task:
    return Task(
        description=(
            "Read the trader's description and emit ONE JSON object matching this schema:\n"
            f"{OUTPUT_SCHEMA}\n\n"
            "Only include explicit or strongly-implied values. Use 'medium' if risk is unstated, "
            "['web'] if no channel is mentioned, 'daily' if cadence is unstated, 0.6 if threshold is unstated. "
            "Commodities use lowercase tokens (power, gas, lng, coal, carbon).\n\n"
            f"DESCRIPTION:\n{text}"
        ),
        expected_output="A single JSON object — no commentary, no markdown.",
        agent=agent,
    )
