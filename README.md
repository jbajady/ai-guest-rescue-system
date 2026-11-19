# AI Guest Rescue System

Python project scaffold for triaging stranded-guest tickets and enforcing safety-first handling.

## What it does (starter)

- Detects safety signals in guest messages (`injury_or_medical_need`, `threat_or_violence`, `nowhere_safe_to_wait`, `unaccompanied_minor`, `stated_fear_of_person`).
- Flags tickets that require immediate human handoff (`handoff_to_safety_agent`) before any refund/hold action.

## Project layout

- `src/ai_guest_rescue_system/` — package source
- `tests/` — pytest tests
- `pyproject.toml` — packaging/config

## Quick start

```bash
python3 -m pip install -e .[dev]
python3 -m pytest
```

## Notes

Safety conditions must be read from the guest message, even when the guest only asks for money or a callback. Before handoff, only `handoff_to_safety_agent` is allowed (no `issue_refund` / `hold_booking`).
