"""Ticket triage helpers for guest rescue workflows."""

from __future__ import annotations

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
