from ai_guest_rescue_system.triage import detect_safety_signals, requires_human_handoff


def test_refund_request_with_injury_requires_handoff():
    msg = "I slipped and my knee is bleeding badly, I can hardly stand. Refund me."
    assert requires_human_handoff(msg)
    assert "injury_or_medical_need" in detect_safety_signals(msg)


def test_angry_message_without_safety_does_not_require_handoff():
    msg = "This is an absolute nightmare. Get us another two-bed flat nearby, now."
    assert not requires_human_handoff(msg)
    assert detect_safety_signals(msg) == []
