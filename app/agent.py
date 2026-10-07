from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Photo:
    id: str
    room: str
    observation: str
    confidence: float
    measurement: Optional[float] = None
    duplicate_of: Optional[str] = None
    relevant: bool = True


@dataclass
class Claim:
    transcript_room: str
    transcript_measurement: Optional[float]
    photos: List[Photo]
    estimate_tool_available: bool = True


@dataclass
class Result:
    decision: str
    reasons: List[str]
    trace: List[str]


THRESHOLD = 0.60


def evaluate_claim(claim: Claim) -> Result:
    """Apply a small deterministic evidence policy before an estimate action."""
    trace = ["extract", "retrieve_evidence", "validate"]
    reasons = []

    # Do not let duplicate or irrelevant frames count as independent evidence.
    relevant = [p for p in claim.photos if p.relevant and not p.duplicate_of]

    if not relevant:
        reasons.append("no usable visual evidence")

    room_matches = [p for p in relevant if p.room == claim.transcript_room]
    if not room_matches:
        reasons.append("transcript room has no matching usable photo evidence")

    if any(p.confidence < THRESHOLD for p in room_matches):
        reasons.append("matching visual evidence is below confidence threshold")

    if claim.transcript_measurement is not None:
        measured = [p.measurement for p in room_matches if p.measurement is not None]
        if not measured:
            reasons.append("measurement is reported by transcript but not visually supported")
        elif min(abs(m - claim.transcript_measurement) for m in measured) > 0.25:
            reasons.append("transcript measurement conflicts with photo measurement")

    trace.append("decide")
    if reasons:
        trace.append("escalate_human")
        return Result("human_review", reasons, trace)

    if not claim.estimate_tool_available:
        trace.extend(["tool_failure", "escalate_human"])
        return Result("human_review", ["estimate tool unavailable"], trace)

    trace.append("act_or_estimate")
    return Result("ready_for_estimate", [], trace)
