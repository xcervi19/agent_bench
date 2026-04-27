"""Periodic jobs for the Signal Gather app."""

from uuid import UUID

from agentic_core.scheduler import JobSpec

from ..services.discovery import FEEDS_BY_COMMODITY


def build_jobs(tenant_id: UUID, regions: list[str] | None = None) -> list[JobSpec]:
    target_regions = regions or ["Europe"]
    return [
        *_discovery_jobs(tenant_id, target_regions),
        _signal_sweep_job(tenant_id),
    ]


def _discovery_jobs(tenant_id: UUID, regions: list[str]) -> list[JobSpec]:
    specs: list[JobSpec] = []
    for commodity in FEEDS_BY_COMMODITY:
        for region in regions:
            specs.append(
                JobSpec(
                    name=f"discovery_{commodity}_{region.lower()}",
                    task_name="signal_gather.discover_market",
                    tenant_id=tenant_id,
                    interval_seconds=60 * 30,
                    payload={"commodity": commodity, "region": region},
                )
            )
    return specs


def _signal_sweep_job(tenant_id: UUID) -> JobSpec:
    return JobSpec(
        name="signal_sweep",
        task_name="signal_gather.detect_signals",
        tenant_id=tenant_id,
        interval_seconds=60 * 15,
        payload={"window_hours": 12},
    )
