from hallucination_detector.models import Claim, Label


def score_claims(claims: list[Claim]) -> list[Claim]:
    out = []
    for c in claims:
        s = 0.5
        lb = Label.UNCERTAIN
        if c.evidence:
            ev = c.evidence.lower()
            ct = c.text.lower()
            words = set(ct.split())
            ev_words = set(ev.split())
            overlap = len(words & ev_words) / max(len(words), 1)
            s = 1.0 - overlap
            lb = Label.HALLUCINATED if s > 0.6 else Label.VERIFIED if s < 0.4 else Label.UNCERTAIN
        out.append(c.model_copy(update={"score": round(s, 4), "label": lb}))
    return out
