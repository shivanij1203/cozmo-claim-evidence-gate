from .agent import Claim, Photo, evaluate_claim


def scenarios():
    return [
        (
            "clean evidence",
            Claim("kitchen", 6.0, [Photo("p1", "kitchen", "wet baseboard", .94, 6.0)]),
            "ready_for_estimate",
        ),
        (
            "room mismatch",
            Claim("kitchen", 6.0, [Photo("p1", "hall", "wet floor", .91, None)]),
            "human_review",
        ),
        (
            "conflicting measurement",
            Claim("kitchen", 6.0, [Photo("p1", "kitchen", "damage", .92, 9.0)]),
            "human_review",
        ),
        (
            "low confidence",
            Claim("kitchen", 6.0, [Photo("p1", "kitchen", "unclear damage", .41, 6.0)]),
            "human_review",
        ),
        (
            "duplicate and irrelevant",
            Claim(
                "kitchen",
                None,
                [
                    Photo("p1", "kitchen", "damage", .88),
                    Photo("p2", "kitchen", "same frame", .88, duplicate_of="p1"),
                    Photo("p3", "bedroom", "person", .98, relevant=False),
                ],
            ),
            "ready_for_estimate",
        ),
        (
            "tool outage",
            Claim("kitchen", 6.0, [Photo("p1", "kitchen", "wet baseboard", .94, 6.0)], False),
            "human_review",
        ),
    ]


def run():
    rows = []
    for name, claim, expected in scenarios():
        result = evaluate_claim(claim)
        rows.append(
            {
                "scenario": name,
                "expected": expected,
                "actual": result.decision,
                "pass": result.decision == expected,
                "reasons": result.reasons,
            }
        )
    return rows
