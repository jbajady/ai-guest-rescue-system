"""AI Guest Rescue System."""

from .ticket_types import TICKET_TYPE_ORDER, TICKET_TYPES, TicketTypeInfo
from .triage import (
    SAFETY_SIGNALS,
    classify_ticket,
    classify_tickets,
    detect_safety_signals,
    load_tickets,
    requires_human_handoff,
    write_sorted_tickets,
)

__all__ = [
    "__version__",
    "SAFETY_SIGNALS",
    "TICKET_TYPES",
    "TICKET_TYPE_ORDER",
    "TicketTypeInfo",
    "detect_safety_signals",
    "requires_human_handoff",
    "classify_ticket",
    "classify_tickets",
    "load_tickets",
    "write_sorted_tickets",
]
__version__ = "0.1.0"
