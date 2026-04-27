"""Importing this package registers all task handlers in the core registry."""

from . import (  # noqa: F401
    detect_signals,
    discovery,
    extract_events,
    generate_briefing,
    insights,
    setup_profile,
)
