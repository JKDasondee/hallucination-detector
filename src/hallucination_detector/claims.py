from hallucination_detector.models import Claim


def extract_claims(text: str) -> list[Claim]:
    sents = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    return [Claim(text=s) for s in sents]
