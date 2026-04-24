"""Periodic jobs for the Signal Gather app."""

from uuid import UUID

from agentic_core.scheduler import JobSpec


def build_jobs(tenant_id: UUID) -> list[JobSpec]:
    return [
        JobSpec(
            name="commodity_discovery_power_eu",
            task_name="signal_gather.discover_market",
            tenant_id=tenant_id,
            interval_seconds=60 * 30,
            payload={"commodity": "power", "region": "Europe"},
        ),
        JobSpec(
            name="commodity_discovery_gas_eu",
            task_name="signal_gather.discover_market",
            tenant_id=tenant_id,
            interval_seconds=60 * 30,
            payload={"commodity": "gas", "region": "Europe"},
        ),
    ]
