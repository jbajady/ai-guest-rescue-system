# Ticket Types (Lisbon stranded-guest incident)

Ticket types: **rebooking, refund, safety** (see `TICKET_TYPES` in `src/ai_guest_rescue_system/triage.py`).

Each of the 60 tickets is assigned one type in `data/ticket_type_assignments.csv` (`ticket_id`, `ticket_type`). Safety is read from `guest_message` and takes priority over the requested action.

| Ticket type | Problem | Agent | Allowed booking tools | Forbidden before hand-off |
|---|---|---|---|---|
| `safety` | Safety condition in message: injury/medical need, threat or violence, nowhere safe to wait, unaccompanied minor, or stated fear of a person. | Live Trust & Safety agent | `handoff_to_safety_agent` | `issue_refund`, `hold_booking` |
| `rebooking` | Qualifies for AirCover rebooking support and needs a comparable home for the remaining stay (no refund for the same nights when rebooked). | Rebooking support agent | `hold_booking` | — |
| `refund` | Guest declines rebooking or no comparable home passes; refund handling due (one remedy per stay). | Refund support agent | `issue_refund` | — |

## Notes
- A money-only/refund request still gets `safety` if a safety signal is present; guest need not say "safety".
- After handoff, the live safety agent decides any refund or booking.
- Rebooking holds must satisfy comparable-home tests (dates, party size, bedrooms, `status=available`, `nightly_price <= 120%` of original). If no comparable home or guest declines, handle as `refund`.
- Refund never exceeds `total_paid`.

## Sorted tickets (all 60)
- Input: `data/lisbon_stranded_guest_tickets_2026-11-16.csv` (60 tickets)
- Assignments (each ticket ID -> type): `data/ticket_type_assignments.csv`
- Detailed sort (with agent/tools): `data/lisbon_tickets_sorted.csv`
- Counts: `rebooking` 34, `refund` 20, `safety` 6
- Safety tickets: `LIS-TKT-0007`, `LIS-TKT-0015`, `LIS-TKT-0023`, `LIS-TKT-0034`, `LIS-TKT-0046`, `LIS-TKT-0055`
- Regenerate: `PYTHONPATH=src python3 scripts/sort_lisbon_tickets.py`
