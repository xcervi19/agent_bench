"""Uvicorn target: `uvicorn apps.signal_gather.entrypoints.api:app`."""

from agentic_core.api import build_auth_routers, create_app

from ..routers import ALL_ROUTERS

app = create_app(title="Signal Gather API", routers=[*build_auth_routers(), *ALL_ROUTERS])
