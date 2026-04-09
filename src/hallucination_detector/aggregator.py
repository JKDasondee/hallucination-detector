from hallucination_detector.models import Claim


def aggregate(claims: list[Claim]) -> float:
    if not claims:
        return 0.0
    return round(sum(c.score for c in claims) / len(claims), 4)
