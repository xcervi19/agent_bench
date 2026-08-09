from __future__ import annotations

import pytest

from apps.claude_agent.config import ClaudeAgentSettings


def paths(routers) -> set[str]:
    return {route.path for router in routers for route in router.routes}


@pytest.fixture
def build():
    from agentic_core.api.auth_routes import build_auth_routers

    return build_auth_routers


def test_registration_is_closed_by_default():
    assert ClaudeAgentSettings().allow_public_registration is False


def test_register_route_absent_when_closed(build):
    assert not any("/auth/register" in p for p in paths(build(public_registration=False)))


def test_register_route_present_when_open(build):
    assert any("/auth/register" in p for p in paths(build(public_registration=True)))


@pytest.mark.parametrize("public", [True, False])
def test_login_and_users_survive_either_way(build, public):
    served = paths(build(public_registration=public))
    assert any("/auth/jwt/login" in p for p in served)
    assert any("/users/me" in p for p in served)


def test_default_keeps_registration_for_library_callers(build):
    assert any("/auth/register" in p for p in paths(build()))


@pytest.mark.parametrize("public", [True, False])
def test_a_session_can_be_renewed_and_ended_without_signing_in_again(build, public):
    """Login alone leaves a user stranded when the access token expires."""
    served = paths(build(public_registration=public))
    assert any("/auth/jwt/refresh" in p for p in served)
    assert any("/auth/jwt/logout" in p for p in served)
