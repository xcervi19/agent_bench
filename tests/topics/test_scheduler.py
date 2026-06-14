"""Unit tests for the in-app topic refresh scheduler (#22)."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import pytest

from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import scheduler as sched

NOW = datetime(2026, 6, 13, 8, 0, 0, tzinfo=UTC)


# ---- pure helpers ----------------------------------------------------------


def test_normalize_interval_clamps():
    assert sched.normalize_interval(6, lo=1, hi=168) == 6
    assert sched.normalize_interval(0, lo=1, hi=168) == 1
    assert sched.normalize_interval(999, lo=1, hi=168) == 168
    assert sched.normalize_interval(None, lo=1, hi=168) is None


def test_compute_next_refresh_at():
    assert sched.compute_next_refresh_at(NOW, 6) == NOW + timedelta(hours=6)
    assert sched.compute_next_refresh_at(NOW, None) is None
    assert sched.compute_next_refresh_at(NOW, 0) is None


def test_is_due():
    assert sched.is_due(NOW - timedelta(seconds=1), NOW) is True
    assert sched.is_due(NOW, NOW) is True
    assert sched.is_due(NOW + timedelta(hours=1), NOW) is False
    assert sched.is_due(None, NOW) is False


def test_eight_to_eight_window_yields_hourly_cadence():
    """Sanity check the product scenario: 1h interval over 12h => 12 fire times."""
    interval = 1
    fire = sched.compute_next_refresh_at(NOW, interval)
    fires = []
    end = NOW + timedelta(hours=12)
    while fire <= end:
        fires.append(fire)
        fire = sched.compute_next_refresh_at(fire, interval)
    assert len(fires) == 12


# ---- dispatch loop ---------------------------------------------------------


def _settings(**over) -> ClaudeAgentSettings:
    base = dict(
        database_url="postgresql+asyncpg://x/y",
        scheduler_enabled=True,
        scheduler_max_concurrent_refreshes=2,
    )
    base.update(over)
    return ClaudeAgentSettings(**base)


@pytest.fixture
def stub_run_refresh(monkeypatch):
    calls: list[dict] = []

    async def _fake(topic_id, subscription_id, settings, *, trigger="manual"):
        calls.append({"topic_id": topic_id, "subscription_id": subscription_id, "trigger": trigger})

    monkeypatch.setattr(sched, "run_refresh", _fake)
    return calls


async def test_tick_dispatches_claimed(monkeypatch, stub_run_refresh):
    claimed = [(uuid.uuid4(), 1), (uuid.uuid4(), 2)]

    async def _fake_claim(now, limit):
        assert limit == 2  # full budget on first pass
        return claimed

    monkeypatch.setattr(sched, "claim_due_subscriptions", _fake_claim)

    scheduler = sched.RefreshScheduler(_settings())
    dispatched = await scheduler.tick(now=NOW)
    await asyncio.sleep(0)  # let dispatched tasks run

    assert dispatched == 2
    assert len(stub_run_refresh) == 2
    assert {c["trigger"] for c in stub_run_refresh} == {"scheduled"}


async def test_tick_respects_concurrency_budget(monkeypatch, stub_run_refresh):
    claim_calls: list[int] = []

    async def _fake_claim(now, limit):
        claim_calls.append(limit)
        return []

    monkeypatch.setattr(sched, "claim_due_subscriptions", _fake_claim)

    scheduler = sched.RefreshScheduler(_settings(scheduler_max_concurrent_refreshes=2))

    # Saturate in-flight set with two long-running stand-ins.
    gate = asyncio.Event()

    async def _block():
        await gate.wait()

    t1 = asyncio.create_task(_block())
    t2 = asyncio.create_task(_block())
    scheduler._inflight.update({t1, t2})

    dispatched = await scheduler.tick(now=NOW)
    assert dispatched == 0
    assert claim_calls == []  # budget exhausted -> claim never queried

    gate.set()
    await asyncio.gather(t1, t2)


async def test_tick_uses_remaining_budget(monkeypatch, stub_run_refresh):
    seen_limits: list[int] = []

    async def _fake_claim(now, limit):
        seen_limits.append(limit)
        return []

    monkeypatch.setattr(sched, "claim_due_subscriptions", _fake_claim)

    scheduler = sched.RefreshScheduler(_settings(scheduler_max_concurrent_refreshes=3))
    gate = asyncio.Event()

    async def _block():
        await gate.wait()

    t1 = asyncio.create_task(_block())
    scheduler._inflight.add(t1)

    await scheduler.tick(now=NOW)
    assert seen_limits == [2]  # 3 max - 1 in-flight

    gate.set()
    await asyncio.gather(t1)


async def test_claim_failure_does_not_crash_tick(monkeypatch, stub_run_refresh):
    async def _boom(now, limit):
        raise RuntimeError("db down")

    monkeypatch.setattr(sched, "claim_due_subscriptions", _boom)
    scheduler = sched.RefreshScheduler(_settings())
    assert await scheduler.tick(now=NOW) == 0
