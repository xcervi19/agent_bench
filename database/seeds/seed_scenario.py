"""CLI: `python -m database.seeds.seed_scenario <name>`.

Demo scenarios for the legacy signal_gather stack live on branch
`archive/signal_gather-platform` (tag `archive/pre-slim-2026`).
"""

import sys

SCENARIOS: dict[str, str] = {}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in SCENARIOS:
        print(
            "No seed scenarios on slim main. "
            "Use branch archive/signal_gather-platform for signal_gather demos."
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
