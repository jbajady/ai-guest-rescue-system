# Ticket Types (Lisbon stranded-guest incident)

Each ticket is sorted into exactly one ticket type. Safety is read from `guest_message` and takes priority over the requested action.

| Ticket type | Problem | Agent | Allowed booking tools | Forbidden before hand-off |
|---|---|---|---|---|
| `safety_handoff` | Safety condition in message: injury/medical need, threat or violence, nowhere safe to wait, unaccompanied minor, or stated fear of a person. | Live Trust & Safety agent | `handoff_to_safety_agent` | `issue_refund`, `hold_booking` |
| `rebooking` | Qualifies for AirCover rebooking support and needs a comparable home for the remaining stay (no refund for the same nights when rebooked). | Rebooking support agent | `hold_booking` | — |
| `refund` | Guest declines rebooking or no comparable home passes; refund handling due (one remedy per stay). | Refund support agent | `issue_refund` | — |

## Notes
- A money-only/refund request still gets `safety_handoff` if a safety signal is present; guest need not say "safety".
- After handoff, the live safety agent decides any refund or booking.
- Rebooking holds must satisfy comparable-home tests (dates, party size, bedrooms, `status=available`, `nightly_price <= 120%` of original). If no comparable home or guest declines, handle as `refund`.
- Refund never exceeds `total_paid`.

## Sorted tickets (all 60)
- Input: `data/lisbon_stranded_guest_tickets_2026-11-16.csv` (60 tickets)
- Output: `data/lisbon_tickets_sorted.csv` (all 60 sorted into one ticket type with agent and allowed booking tools)
- Counts: `rebooking` 34, `refund` 20, `safety_handoff` 6
- Regenerate: `PYTHONPATH=src python3 scripts/sort_lisbon_tickets.py`
