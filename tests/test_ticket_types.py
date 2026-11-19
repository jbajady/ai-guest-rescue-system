from pathlib import Path

from ai_guest_rescue_system.ticket_types import TICKET_TYPE_ORDER, TICKET_TYPES as TICKET_TYPE_INFO
from ai_guest_rescue_system.triage import TICKET_TYPES, classify_ticket, classify_tickets

DATA = Path(__file__).resolve().parents[1] / "data" / "lisbon_stranded_guest_tickets_2026-11-16.csv"
ASSIGNMENTS = Path(__file__).resolve().parents[1] / "data" / "ticket_type_assignments.csv"


def test_ticket_types_defined():
    assert TICKET_TYPES == ["rebooking", "refund", "safety"]
    assert set(TICKET_TYPE_ORDER) == {"rebooking", "refund", "safety"}
    assert TICKET_TYPE_INFO["safety"].allowed_booking_tools == ("handoff_to_safety_agent",)
    assert TICKET_TYPE_INFO["safety"].forbidden_before_handoff == ("issue_refund", "hold_booking")
    assert TICKET_TYPE_INFO["rebooking"].agent == "Rebooking support agent"
    assert TICKET_TYPE_INFO["refund"].allowed_booking_tools == ("issue_refund",)


def test_safety_overrides_requested_action():
    t = {"ticket_id": "X", "guest_requested": "refund", "expected_outcome": "safety",
         "guest_message": "My knee is bleeding badly and I can hardly stand. Refund me."}
    c = classify_ticket(t)
    assert c["ticket_type"] == "safety"
    assert c["allowed_booking_tools"] == ["handoff_to_safety_agent"]
    assert "issue_refund" in c["forbidden_before_handoff"]


def test_angry_rebooking_not_safety():
    t = {"ticket_id": "LIS-TKT-0005", "guest_requested": "rebooking", "expected_outcome": "rebooking",
         "guest_message": "This is an absolute nightmare. Get us another two-bed flat nearby, now."}
    c = classify_ticket(t)
    assert c["ticket_type"] == "rebooking"
    assert c["allowed_booking_tools"] == ["hold_booking"]


def test_all_60_tickets_sorted_and_assignments_file():
    rows = classify_tickets(DATA)
    assert len(rows) == 60
    assert all(r["ticket_type"] in TICKET_TYPES for r in rows)
    counts = {}
    for r in rows:
        counts[r["ticket_type"]] = counts.get(r["ticket_type"], 0) + 1
    assert counts == {"rebooking": 34, "refund": 20, "safety": 6}
    safety_ids = {r["ticket_id"] for r in rows if r["ticket_type"] == "safety"}
    assert safety_ids == {
        "LIS-TKT-0007", "LIS-TKT-0015", "LIS-TKT-0023",
        "LIS-TKT-0034", "LIS-TKT-0046", "LIS-TKT-0055",
    }

    assert ASSIGNMENTS.exists()
    lines = ASSIGNMENTS.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0].strip() == "ticket_id,ticket_type"
    assert len(lines) == 61
    pairs = dict(line.split(",", 1) for line in lines[1:])
    assert len(pairs) == 60
    assert pairs["LIS-TKT-0007"] == "safety"
    assert sum(1 for v in pairs.values() if v == "rebooking") == 34
    assert sum(1 for v in pairs.values() if v == "refund") == 20
    assert sum(1 for v in pairs.values() if v == "safety") == 6
