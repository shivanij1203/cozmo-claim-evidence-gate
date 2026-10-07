from app.agent import Claim, Photo, evaluate_claim


def test_clean_claim_can_reach_estimate():
    claim = Claim("kitchen", 6.0, [Photo("p1", "kitchen", "wet baseboard", .94, 6.0)])
    result = evaluate_claim(claim)
    assert result.decision == "ready_for_estimate"
    assert result.trace[-1] == "act_or_estimate"


def test_transcript_measurement_without_visual_support_escalates():
    claim = Claim("kitchen", 6.0, [Photo("p1", "kitchen", "wet baseboard", .94)])
    result = evaluate_claim(claim)
    assert result.decision == "human_review"
    assert "measurement is reported by transcript but not visually supported" in result.reasons


def test_conflicting_measurement_escalates():
    claim = Claim("kitchen", 6.0, [Photo("p1", "kitchen", "damage", .92, 9.0)])
    result = evaluate_claim(claim)
    assert result.decision == "human_review"
    assert "transcript measurement conflicts with photo measurement" in result.reasons


def test_duplicate_does_not_count_as_new_evidence():
    claim = Claim(
        "kitchen",
        None,
        [
            Photo("p1", "kitchen", "damage", .88),
            Photo("p2", "kitchen", "same frame", .88, duplicate_of="p1"),
        ],
    )
    result = evaluate_claim(claim)
    assert result.decision == "ready_for_estimate"


def test_tool_failure_does_not_execute_estimate():
    claim = Claim("kitchen", 6.0, [Photo("p1", "kitchen", "wet baseboard", .94, 6.0)], False)
    result = evaluate_claim(claim)
    assert result.decision == "human_review"
    assert result.trace[-2:] == ["tool_failure", "escalate_human"]
