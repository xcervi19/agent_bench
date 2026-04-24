"""Run: `python -m apps.signal_gather.entrypoints.worker`."""

from agentic_core.logging import configure_logging
from agentic_core.workers import run_worker

from .. import tasks  # noqa: F401  (import registers task handlers)


def main() -> None:
    configure_logging()
    run_worker()


if __name__ == "__main__":
    main()
