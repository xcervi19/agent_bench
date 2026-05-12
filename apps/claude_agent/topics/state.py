"""Topic state machine + stage names + transition rules.

States are stored as plain text in Postgres so adding a new state is a
prompt-only change (no migration). The transition table here is the
single source of truth at runtime.
"""

from __future__ import annotations

from enum import StrEnum


class TopicState(StrEnum):
    CREATED = "created"
    PLANNING = "planning"                          # Stage 1 running
    PLANNED_AWAITING_REVIEW = "planned_awaiting_review"  # gate after Stage 1+2
    SEARCHING = "searching"                        # Stage 3 running
    SEARCHED = "searched"                          # Stage 3 done, Stage 4 about to start
    REPORTING = "reporting"                        # Stage 4 running
    REPORTED = "reported"                          # terminal-success
    FAILED = "failed"                              # terminal-error
    CANCELLED = "cancelled"                        # terminal-user
    ARCHIVED = "archived"                          # terminal-user


class Stage(StrEnum):
    QUERIES = "queries"
    INTRO = "intro"
    SEARCH = "search"
    REPORT = "report"


TERMINAL_STATES: frozenset[TopicState] = frozenset(
    {TopicState.FAILED, TopicState.CANCELLED, TopicState.ARCHIVED, TopicState.REPORTED}
)

RESUMABLE_STATES: frozenset[TopicState] = frozenset(
    {TopicState.PLANNING, TopicState.SEARCHING, TopicState.REPORTING}
)

# Allowed transitions. Used by the orchestrator and the API to refuse
# nonsensical jumps (e.g. POST /proceed from `searching`).
ALLOWED_TRANSITIONS: dict[TopicState, frozenset[TopicState]] = {
    TopicState.CREATED: frozenset({TopicState.PLANNING, TopicState.CANCELLED}),
    TopicState.PLANNING: frozenset(
        {TopicState.PLANNED_AWAITING_REVIEW, TopicState.FAILED, TopicState.CANCELLED}
    ),
    TopicState.PLANNED_AWAITING_REVIEW: frozenset(
        {TopicState.SEARCHING, TopicState.CANCELLED, TopicState.ARCHIVED}
    ),
    TopicState.SEARCHING: frozenset(
        {TopicState.SEARCHED, TopicState.FAILED, TopicState.CANCELLED}
    ),
    TopicState.SEARCHED: frozenset(
        {TopicState.REPORTING, TopicState.CANCELLED}
    ),
    TopicState.REPORTING: frozenset(
        {TopicState.REPORTED, TopicState.FAILED, TopicState.CANCELLED}
    ),
    TopicState.REPORTED: frozenset({TopicState.ARCHIVED}),
    TopicState.FAILED: frozenset({TopicState.ARCHIVED}),
    TopicState.CANCELLED: frozenset({TopicState.ARCHIVED}),
    TopicState.ARCHIVED: frozenset(),
}


def can_transition(src: TopicState, dst: TopicState) -> bool:
    return dst in ALLOWED_TRANSITIONS.get(src, frozenset())


def available_actions(state: TopicState) -> list[str]:
    actions: list[str] = []
    if state == TopicState.PLANNED_AWAITING_REVIEW:
        actions.append("proceed")
    if state not in TERMINAL_STATES:
        actions.append("cancel")
        actions.append("input")
    if state in {TopicState.REPORTED, TopicState.FAILED, TopicState.CANCELLED}:
        actions.append("archive")
    return actions
