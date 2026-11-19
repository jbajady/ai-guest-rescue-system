from pathlib import Path

from ai_guest_rescue_system.ticket_types import TICKET_TYPE_ORDER, TICKET_TYPES
from ai_guest_rescue_system.triage import classify_ticket, classify_tickets

DATA = Path(__file__).resolve().parents[1] / "data" / "lisbon_stranded_guest_tickets_2026-11-16.csv"


def test_ticket_types_defined():
    assert set(TICKET_TYPE_ORDER) == {"safety_handoff", "rebooking", "refund"}
    assert TICKET_TYPES["safety_handoff"].allowed_booking_tools == ("handoff_to_safety_agent",)
    assert TICKET_TYPES["safety_handoff"].forbidden_before_handoff == ("issue_refund", "hold_booking")
    assert TICKET_TYPES["rebooking"].agent == "Rebooking support agent"
    assert TICKET_TYPES["refund"].allowed_booking_tools == ("issue_refund",)


def test_safety_overrides_requested_action():
    t = {"ticket_id": "X", "guest_requested": "refund", "expected_outcome": "safety",
         "guest_message": "My knee is bleeding badly and I can hardly stand. Refund me."}
    c = classify_ticket(t)
    assert c["ticket_type"] == "safety_handoff"
    assert c["allowed_booking_tools"] == ["handoff_to_safety_agent"]
    assert "issue_refund" in c["forbidden_before_handoff"]


def test_angry_rebooking_not_safety():
    t = {"ticket_id": "LIS-TKT-0005", "guest_requested": "rebooking", "expected_outcome": "rebooking",
         "guest_message": "This is an absolute nightmare. Get us another two-bed flat nearby, now."}
    c = classify_ticket(t)
    assert c["ticket_type"] == "rebooking"
    assert c["allowed_booking_tools"] == ["hold_booking"]


def test_all_60_tickets_sorted():
    rows = classify_tickets(DATA)
    assert len(rows) == 60
    assert all(r["ticket_type"] in TICKET_TYPES for r in rows)
    counts = {}
    for r in rows:
        counts[r["ticket_type"]] = counts.get(r["ticket_type"], 0) + 1
    assert counts == {"rebooking": 34, "refund": 20, "safety_handoff": 6}
    safety_ids = {r["ticket_id"] for r in rows if r["ticket_type"] == "safety_handoff"}
    assert safety_ids == {
        "LIS-TKT-0007", "LIS-TKT-0015", "LIS-TKT-0023",
        "LIS-TKT-0034", "LIS-TKT-0046", "LIS-TKT-0055",
    }
