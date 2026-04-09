from hallucination_detector.aggregator import aggregate
from hallucination_detector.claims import extract_claims
from hallucination_detector.models import DetectionResult
from hallucination_detector.retriever import retrieve_evidence
from hallucination_detector.scorer import score_claims


class Detector:
    def __init__(self, **kwargs: object) -> None:
        self.cfg = kwargs

    def run(self, text: str, context: str | None = None) -> DetectionResult:
        claims = extract_claims(text)
        if context:
            claims = [c.model_copy(update={"evidence": context}) for c in claims]
        else:
            claims = retrieve_evidence(claims)
        claims = score_claims(claims)
        sc = aggregate(claims)
        return DetectionResult(text=text, claims=claims, score=sc)


_default: Detector | None = None


def detect(text: str, context: str | None = None, **kwargs: object) -> DetectionResult:
    global _default
    if _default is None:
        _default = Detector(**kwargs)
    return _default.run(text, context)
