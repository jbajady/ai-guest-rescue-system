"""Ticket type definitions for the Lisbon stranded-guest incident."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TicketTypeInfo:
    key: str
    label: str
    problem: str
    agent: str
    allowed_booking_tools: tuple[str, ...]
    forbidden_before_handoff: tuple[str, ...]
    notes: str


# Canonical ticket types (also listed as TICKET_TYPES in triage.py).
TICKET_TYPE_ORDER = ("rebooking", "refund", "safety")
TICKET_TYPE_LIST = list(TICKET_TYPE_ORDER)

TICKET_TYPES: dict[str, TicketTypeInfo] = {
    "safety": TicketTypeInfo(
        key="safety",
        label="Safety handoff",
        problem=(
            "Safety condition described in guest message (injury/medical need, threat or "
            "violence, nowhere safe to wait, unaccompanied minor, or stated fear of a person)."
        ),
        agent="Live Trust & Safety agent",
        allowed_booking_tools=("handoff_to_safety_agent",),
        forbidden_before_handoff=("issue_refund", "hold_booking"),
        notes=(
            "Read safety from guest_message regardless of requested action; guest need not say "
            "'safety'. After handoff, the live safety agent decides any refund or booking."
        ),
    ),
    "rebooking": TicketTypeInfo(
        key="rebooking",
        label="Rebooking",
        problem=(
            "Guest qualifies for AirCover rebooking support and needs a comparable home for the "
            "remaining stay (no refund for the same nights when rebooked)."
        ),
        agent="Rebooking support agent",
        allowed_booking_tools=("hold_booking",),
        forbidden_before_handoff=(),
        notes=(
            "Hold/offer a comparable listing that passes all tests (dates, party size, bedrooms, "
            "status available, nightly_price <= 120% of original). issue_refund is not combined "
            "with a rebooking for the same nights; if no comparable home or guest declines, "
            "handle as refund."
        ),
    ),
    "refund": TicketTypeInfo(
        key="refund",
        label="Refund",
        problem=(
            "Guest is due/refuses rebooking and needs refund handling for the stay (e.g. declines "
            "rebooking offer or no comparable home)."
        ),
        agent="Refund support agent",
        allowed_booking_tools=("issue_refund",),
        forbidden_before_handoff=(),
        notes=(
            "Refund never exceeds total_paid. Full total_paid when no comparable home passes or "
            "guest declines rebooking. One remedy per stay (no rebooking for same nights)."
        ),
    ),
}
