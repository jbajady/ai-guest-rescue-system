#!/usr/bin/env python3
"""Sort the 60 Lisbon stranded-guest tickets into ticket types."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_guest_rescue_system.triage import classify_tickets, write_sorted_tickets  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=str(ROOT / "data" / "lisbon_stranded_guest_tickets_2026-11-16.csv"),
        help="Path to the input tickets CSV",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "data" / "lisbon_tickets_sorted.csv"),
        help="Path to write the sorted tickets CSV",
    )
    args = parser.parse_args()

    rows = write_sorted_tickets(args.input, args.output)
    counts = Counter(r["ticket_type"] for r in rows)
    summary = {
        "total": len(rows),
        "by_ticket_type": dict(counts),
        "output": str(Path(args.output)),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
