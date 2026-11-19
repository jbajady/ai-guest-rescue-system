"""Ticket triage helpers for guest rescue workflows."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .ticket_types import TICKET_TYPES

SAFETY_SIGNALS = {
    "injury_or_medical_need": (
        "injury",
        "bleeding",
        "hurt",
        "medical",
        "doctor",
        "medication",
        "diabetic",
        "unwell",
    ),
    "threat_or_violence": (
        "threat",
        "threatened",
        "followed",
        "shouted",
        "harmed",
        "smash",
        "violence",
    ),
    "nowhere_safe_to_wait": (
        "nowhere to go",
        "nowhere safe",
        "street",
        "phone is on",
        "phone on",
        "luggage",
        "cold",
        "asked me to leave",
    ),
    "unaccompanied_minor": (
        "16 and travelling",
        "under 18",
        "minor",
        "on my own to meet",
    ),
    "stated_fear_of_person": (
        "scared",
        "afraid",
        "fear",
    ),
}


def detect_safety_signals(message: str) -> list[str]:
    """Return matching safety signal categories found in a guest message."""
    text = (message or "").lower()
    matches: list[str] = []
    for signal, keywords in SAFETY_SIGNALS.items():
        if any(keyword in text for keyword in keywords):
            matches.append(signal)
    return matches


def requires_human_handoff(message: str) -> bool:
    """True when any safety signal is present and a human must take over."""
    return bool(detect_safety_signals(message))


def classify_ticket(ticket: dict[str, Any]) -> dict[str, Any]:
    """Classify a ticket into a ticket type with agent and allowed booking tools.

    Safety is read from guest_message and takes priority. Non-safety tickets are
    sorted by expected_outcome (rebooking/refund).
    """
    message = str(ticket.get("guest_message", "") or "")
    signals = detect_safety_signals(message)
    safety = bool(signals) or str(ticket.get("expected_outcome", "")).strip().lower() == "safety"

    if safety:
        type_key = "safety_handoff"
    else:
        outcome = str(ticket.get("expected_outcome", "")).strip().lower()
        if outcome == "refund":
            type_key = "refund"
        else:
            type_key = "rebooking"

    info = TICKET_TYPES[type_key]
    return {
        "ticket_id": ticket.get("ticket_id", ""),
        "guest_requested": ticket.get("guest_requested", ""),
        "expected_outcome": ticket.get("expected_outcome", ""),
        "ticket_type": info.key,
        "ticket_type_label": info.label,
        "agent": info.agent,
        "allowed_booking_tools": list(info.allowed_booking_tools),
        "forbidden_before_handoff": list(info.forbidden_before_handoff),
        "safety_signals_detected": signals,
    }


def load_tickets(csv_path: str | Path) -> list[dict[str, str]]:
    """Load ticket rows from a CSV file."""
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_tickets(csv_path: str | Path) -> list[dict[str, Any]]:
    """Classify all tickets from a CSV file."""
    return [classify_ticket(row) for row in load_tickets(csv_path)]


def write_sorted_tickets(csv_path: str | Path, output_csv_path: str | Path) -> list[dict[str, Any]]:
    """Write a CSV with all tickets sorted/classified by ticket type."""
    rows = classify_tickets(csv_path)
    out_path = Path(output_csv_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "ticket_id",
        "guest_requested",
        "expected_outcome",
        "ticket_type",
        "ticket_type_label",
        "agent",
        "allowed_booking_tools",
        "forbidden_before_handoff",
        "safety_signals_detected",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "allowed_booking_tools": ";".join(row["allowed_booking_tools"]),
                    "forbidden_before_handoff": ";".join(row["forbidden_before_handoff"]),
                    "safety_signals_detected": ";".join(row["safety_signals_detected"]),
                }
            )
    return rows
