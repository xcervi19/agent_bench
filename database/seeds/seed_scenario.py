"""CLI: `python -m database.seeds.seed_scenario signal_gather_commodity_trading`."""

import asyncio
import sys

from apps.signal_gather.scenarios import seed as seed_commodity_trading

SCENARIOS = {
    "signal_gather_commodity_trading": seed_commodity_trading,
}


async def run(name: str) -> None:
    handler = SCENARIOS[name]
    await handler()
    print(f"scenario '{name}' seeded")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: seed_scenario <{'|'.join(SCENARIOS)}>")
        sys.exit(2)
    asyncio.run(run(sys.argv[1]))


if __name__ == "__main__":
    main()
