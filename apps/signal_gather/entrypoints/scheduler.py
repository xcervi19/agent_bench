"""Run: `python -m apps.signal_gather.entrypoints.scheduler`."""

from agentic_core.logging import configure_logging
from agentic_core.scheduler import Scheduler

from ..scenarios.commodity_trading import DEMO_TENANT_ID
from ..scheduler_jobs import (
    build_jobs,
    dispatch_daily_briefings,
    dispatch_weekly_briefings,
)


def main() -> None:
    configure_logging()
    scheduler = Scheduler()
    scheduler.register_many(build_jobs(DEMO_TENANT_ID))
    scheduler.register_fn(
        name="daily_briefings",
        fn=dispatch_daily_briefings,
        cron="0 6 * * *",
        args=[DEMO_TENANT_ID],
    )
    scheduler.register_fn(
        name="weekly_briefings",
        fn=dispatch_weekly_briefings,
        cron="0 6 * * 1",
        args=[DEMO_TENANT_ID],
    )
    scheduler.run()


if __name__ == "__main__":
    main()
