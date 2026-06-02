"""CLI: python scripts/utils/replay_session.py --session-id <uuid> --tenant-id <uuid>."""

import argparse
import asyncio
import json
from uuid import UUID

from agentic_core.logging import configure_logging
from agentic_core.testing import load_session


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay a recorded agent session.")
    parser.add_argument("--session-id", required=True, type=UUID)
    parser.add_argument("--tenant-id", required=True, type=UUID)
    return parser.parse_args()


async def run(session_id: UUID, tenant_id: UUID) -> None:
    replayed = await load_session(session_id, tenant_id=tenant_id)
    _print_header(replayed)
    _print_events(replayed.events)


def _print_header(r) -> None:
    print(f"session  : {r.id}")
    print(f"tenant   : {r.tenant_id}")
    print(f"crew     : {r.crew}")
    print(f"status   : {r.status}")
    print(f"inputs   : {json.dumps(r.inputs, indent=2)}")
    print(f"output   : {json.dumps(r.output, indent=2) if r.output else '—'}")
    print(f"error    : {r.error or '—'}")
    print("─" * 60)


def _print_events(events: list[dict]) -> None:
    for idx, event in enumerate(events, start=1):
        print(f"[{idx:03}] {event['kind']}")
        print(f"      {json.dumps(event['payload'], indent=2)}")


def main() -> None:
    configure_logging()
    args = parse_args()
    asyncio.run(run(args.session_id, args.tenant_id))


if __name__ == "__main__":
    main()
