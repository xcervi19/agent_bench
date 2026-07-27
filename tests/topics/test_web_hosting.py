"""CORS + bundled-SPA hosting on claude_agent (#16a). No DB, no Claude CLI."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.claude_agent.app import _mount_cors, _mount_web, _warn_on_open_topic_api
from apps.claude_agent.config import ClaudeAgentSettings

INDEX = "<!doctype html><title>SignalGather</title>"


def _settings(**over) -> ClaudeAgentSettings:
    return ClaudeAgentSettings(**over)


def _app(**over) -> FastAPI:
    app = FastAPI()

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    settings = _settings(**over)
    _mount_cors(app, settings)
    _mount_web(app, settings)
    return app


@pytest.fixture
def dist(tmp_path):
    root = tmp_path / "dist"
    (root / "assets").mkdir(parents=True)
    (root / "index.html").write_text(INDEX, encoding="utf-8")
    (root / "assets" / "app.js").write_text("export default 1;\n", encoding="utf-8")
    (root / "favicon.svg").write_text("<svg/>", encoding="utf-8")
    return root


# ---- cors ------------------------------------------------------------------


def test_cors_origins_accept_comma_separated_env_string():
    settings = _settings(cors_origins="http://localhost:5173, https://app.example.com")
    assert settings.cors_origins == ["http://localhost:5173", "https://app.example.com"]


def test_cors_origins_still_accept_json_list():
    assert _settings(cors_origins='["http://a"]').cors_origins == ["http://a"]


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("http://localhost:5173", ["http://localhost:5173"]),
        ("http://a, http://b", ["http://a", "http://b"]),
        ('["http://a"]', ["http://a"]),
        ("", []),
    ],
)
def test_cors_origins_parsed_from_env(monkeypatch, raw, expected):
    """The env source must not JSON-decode this field before the validator runs —
    a bare `host:port` in .env has to boot the app, not crash it."""
    monkeypatch.setenv("CLAUDE_AGENT_CORS_ORIGINS", raw)
    assert ClaudeAgentSettings().cors_origins == expected


def test_cors_origins_default_empty_and_no_header():
    client = TestClient(_app())
    res = client.get("/healthz", headers={"Origin": "http://localhost:5173"})
    assert res.status_code == 200
    assert "access-control-allow-origin" not in res.headers


def test_cors_allows_configured_origin():
    client = TestClient(_app(cors_origins="http://localhost:5173"))
    res = client.get("/healthz", headers={"Origin": "http://localhost:5173"})
    assert res.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unconfigured_origin():
    client = TestClient(_app(cors_origins="http://localhost:5173"))
    res = client.get("/healthz", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in res.headers


def test_cors_preflight_allows_authorization_header():
    client = TestClient(_app(cors_origins="http://localhost:5173"))
    res = client.options(
        "/healthz",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )
    assert res.status_code == 200
    assert res.headers["access-control-allow-origin"] == "http://localhost:5173"


# ---- spa mount -------------------------------------------------------------


def test_web_dist_unset_leaves_app_unmounted():
    assert TestClient(_app()).get("/app").status_code == 404


def test_missing_index_is_skipped_not_fatal(tmp_path):
    empty = tmp_path / "nope"
    empty.mkdir()
    assert TestClient(_app(web_dist=str(empty))).get("/app").status_code == 404


def test_spa_index_served_at_app_root(dist):
    res = TestClient(_app(web_dist=str(dist))).get("/app")
    assert res.status_code == 200
    assert INDEX in res.text


def test_client_route_falls_back_to_index(dist):
    res = TestClient(_app(web_dist=str(dist))).get("/app/topics/1234-abcd")
    assert res.status_code == 200
    assert INDEX in res.text


def test_hashed_assets_served_from_disk(dist):
    res = TestClient(_app(web_dist=str(dist))).get("/app/assets/app.js")
    assert res.status_code == 200
    assert "export default 1;" in res.text


def test_root_level_static_file_served(dist):
    res = TestClient(_app(web_dist=str(dist))).get("/app/favicon.svg")
    assert res.status_code == 200
    assert res.text == "<svg/>"


def test_traversal_outside_dist_falls_back_to_index(dist, tmp_path):
    """`..` survives the client only when percent-encoded — the route must still
    refuse to read outside dist."""
    (tmp_path / "secret.txt").write_text("classified", encoding="utf-8")
    res = TestClient(_app(web_dist=str(dist))).get("/app/%2e%2e/secret.txt")
    assert res.status_code == 200
    assert "classified" not in res.text
    assert INDEX in res.text


def test_api_routes_unaffected_by_spa_mount(dist):
    assert TestClient(_app(web_dist=str(dist))).get("/healthz").json() == {"status": "ok"}


# ---- open-topic-API guard --------------------------------------------------
#
# Regression guard for a live prod exposure: docker-compose's `environment:`
# overrode CLAUDE_AGENT_API_KEY from env_file with "", and an empty key plus the
# default bypass made every anonymous caller the service principal.


def _emitted(capsys, **over) -> str:
    """structlog here uses PrintLoggerFactory, so the record lands on stdout."""
    capsys.readouterr()
    _warn_on_open_topic_api(_settings(**over))
    return capsys.readouterr().out


def test_warns_when_key_empty_and_bypass_on(capsys):
    out = _emitted(capsys, database_url="postgresql+asyncpg://x/y", api_key="")
    assert "topic_api_unauthenticated" in out


def test_silent_when_a_key_is_set(capsys):
    out = _emitted(capsys, database_url="postgresql+asyncpg://x/y", api_key="secret")
    assert "topic_api_unauthenticated" not in out


def test_silent_when_bypass_is_off(capsys):
    out = _emitted(
        capsys,
        database_url="postgresql+asyncpg://x/y",
        api_key="",
        allow_service_key_bypass=False,
    )
    assert "topic_api_unauthenticated" not in out


def test_silent_when_topic_api_is_not_mounted(capsys):
    """No database_url means /v1/topics/* never mounts — nothing to expose."""
    out = _emitted(capsys, database_url="", api_key="")
    assert "topic_api_unauthenticated" not in out
