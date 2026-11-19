# AI Guest Rescue System

Python project for triaging stranded-guest tickets and enforcing safety-first handling.

## What it does

- Detects safety signals in guest messages (`injury_or_medical_need`, `threat_or_violence`, `nowhere_safe_to_wait`, `unaccompanied_minor`, `stated_fear_of_person`).
- Defines ticket types and maps each to the responsible agent and allowed booking tools.
- Sorts all 60 Lisbon stranded-guest tickets into one ticket type so normal tickets show what kind of problem they are and which agent/tools apply.

## Ticket types

`TICKET_TYPES = ["rebooking", "refund", "safety"]` (in `src/ai_guest_rescue_system/triage.py`).

| Ticket type | Problem | Agent | Allowed booking tools | Forbidden before hand-off |
|---|---|---|---|---|
| `safety` | Safety condition in `guest_message` (injury/medical need, threat/violence, nowhere safe to wait, unaccompanied minor, stated fear of a person). | Live Trust & Safety agent | `handoff_to_safety_agent` | `issue_refund`, `hold_booking` |
| `rebooking` | Needs a comparable home for the remaining stay (AirCover rebooking support). | Rebooking support agent | `hold_booking` | — |
| `refund` | Guest declines rebooking or no comparable home passes; refund due (one remedy per stay). | Refund support agent | `issue_refund` | — |

Safety is read from `guest_message` and takes priority over the requested action (even money-only/callback requests). Before handoff, only `handoff_to_safety_agent` is allowed (no `issue_refund` / `hold_booking`).

## 60 Lisbon tickets sorted

- Input: `data/lisbon_stranded_guest_tickets_2026-11-16.csv`
- **Assignments (each ticket ID -> one type):** `data/ticket_type_assignments.csv`
- Detailed sorted output (with agent/tools): `data/lisbon_tickets_sorted.csv`
- Counts: `rebooking` 34, `refund` 20, `safety` 6
- Details: `docs/ticket-types.md`

Regenerate:
```bash
PYTHONPATH=src python3 scripts/sort_lisbon_tickets.py
```

## Project layout

- `src/ai_guest_rescue_system/` — package source (`triage.py` defines `TICKET_TYPES`, `ticket_types.py` has metadata)
- `scripts/sort_lisbon_tickets.py` — sorts the 60 tickets into ticket types
- `data/` — input tickets, `ticket_type_assignments.csv`, `lisbon_tickets_sorted.csv`
- `docs/ticket-types.md` — ticket type definitions and routing
- `tests/` — tests
- `pyproject.toml` — packaging/config

## Quick start

```bash
python3 -m pip install -e .[dev]
python3 -m pytest
```
