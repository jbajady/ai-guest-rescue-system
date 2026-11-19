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

from ai_guest_rescue_system.triage import write_sorted_tickets, write_ticket_type_assignments  # noqa: E402


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
    parser.add_argument(
        "--assignments",
        default=str(ROOT / "data" / "ticket_type_assignments.csv"),
        help="Path to write ticket_id -> ticket_type assignments",
    )
    args = parser.parse_args()

    rows = write_sorted_tickets(args.input, args.output)
    write_ticket_type_assignments(args.input, args.assignments)
    counts = Counter(r["ticket_type"] for r in rows)
    summary = {
        "total": len(rows),
        "by_ticket_type": dict(counts),
        "output": str(Path(args.output)),
        "assignments": str(Path(args.assignments)),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
